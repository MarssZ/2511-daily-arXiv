# 设计文档：NeurIPS 会议论文爬取与增强

## 设计原则

1. **零破坏性**：不修改现有 arXiv 代码
2. **数据兼容**：输出与 arXiv 一致
3. **优雅降级**：缺 PDF 时仍输出基本信息

## 架构

```
NeurIPS 列表页
  ↓ parse()
提取：title, authors, summary
  ↓ 生成详情页 Request
详情页 parse_detail()
  ↓ 提取 OpenReview 链接
生成 PDF URL
  ↓
输出 JSONL
  ↓ ai/enhance.py
AI 增强 JSONL
  ↓ to_md/convert.py
Markdown 文件
  ↓ js/app.js
前端展示
```

**关键决策**：
- 禁用 Pipeline（避免 arXiv API 依赖）
- 两阶段爬取（列表页 + 详情页）
- 优雅降级（缺 PDF 时 pdf="" 但仍输出）

---

## 文件变更

**新增**：
- `spiders/neurips.py`（~200行）
- `js/conference.js`（Conference 模式）

**修改**：
- `js/app.js`（数据映射 + 卡片渲染）

**零修改**：
- `arxiv.py`, `pipelines.py`, `ai/enhance.py`, `to_md/convert.py`

---

## 核心组件

### neurips.py Spider

**职责**：
- 两阶段爬取：列表页 → 详情页
- 提取字段：title, authors, summary, abs, pdf
- 禁用 Pipeline（直接输出 JSONL）

**关键方法**：

```python
class NeuripsSpider(scrapy.Spider):
    name = "neurips"

    custom_settings = {
        'ITEM_PIPELINES': {},  # 禁用 Pipeline
        'DOWNLOAD_DELAY': 1,
    }

    def parse(self, response):
        """列表页：提取基本信息 + 生成详情页请求"""

    def parse_detail(self, response):
        """详情页：提取 OpenReview 链接 → PDF URL"""
```

**错误处理**：
- 缺 title/summary → 跳过
- 缺 OpenReview 链接 → pdf="" 仍输出
- 详情页失败 → 记录警告，继续

---

### 前端展示（js/app.js）

**关键位置**：

1. **数据映射（~740行）**
   ```javascript
   // parseJSONL() 函数
   result[category].push({
     source: paper.source || 'arxiv',
     core_finding: paper.AI?.core_finding || '',
     // ...
   });
   ```

2. **卡片渲染（~1165行）**
   ```javascript
   // renderPapers() 函数
   paperCard.innerHTML = `
     <h3>${title}</h3>
     <p>${summary_layman}</p>
     <span>📄 ${sourceDisplay}</span>
     <p>${core_finding}</p>
   `;
   ```

---

## 数据格式

### 爬取输出（JSONL）

```json
{
  "id": "neurips2024_oral_97958",
  "title": "...",
  "authors": ["...", "..."],
  "summary": "...",
  "abs": "https://neurips.cc/virtual/2024/oral/97958",
  "pdf": "https://openreview.net/pdf?id=...",
  "categories": ["NeurIPS 2024 Oral"],
  "source": "neurips"
}
```

### AI 增强输出（JSONL）

增加 11 个字段（由 `ai/structure.py` 定义）：

```json
{
  // ... 原始字段
  "AI": {
    "core_problem": "...",
    "key_insight": "...",
    "core_finding": "...",
    "mechanism_insight": "...",
    "value_score": "...",
    "summary_layman": "...",
    // ... 其他 5 个字段
  }
}
```

---

## 关键决策

### 决策 1：禁用 Pipeline

**选择**：NeurIPS Spider 禁用 Pipeline，直接输出

**理由**：
- ✅ 零破坏性（不改现有代码）
- ✅ arXiv 需要 API 补全，NeurIPS 不需要

### 决策 2：优雅降级

**选择**：缺 PDF 时仍输出基本信息

**理由**：
- ✅ 至少能拿到 title/summary 用于 AI 分析
- ✅ 减少网络失败导致的数据丢失

---

## 前端修改经验

详见 `tasks.md#前端修改经验总结`

**核心要点**：
- 数据映射：`parseJSONL()` ~740行
- 卡片渲染：`renderPapers()` ~1165行
- Modal弹窗：`showPaperDetails()` ~1200行

**典型修改场景**：

| 需求 | 修改位置 | 行号 |
|------|---------|------|
| 添加新字段到 paper 对象 | `parseJSONL()` | ~740 |
| 修改卡片显示内容 | `renderPapers()` | ~1165 |
| 修改详情弹窗内容 | `showPaperDetails()` | ~1200 |

---

## 测试验证

### 快速验证

```bash
# 爬取 5 篇测试
cd daily_arxiv
scrapy crawl neurips -o test.jsonl -s CLOSESPIDER_ITEMCOUNT=5

# AI 增强
cd ../ai
python enhance.py --data ../daily_arxiv/test.jsonl --max_workers 2

# 转 Markdown
cd ../to_md
python convert.py --data ../daily_arxiv/test_AI_enhanced_Chinese.jsonl
```

### 错误处理验证

| 场景 | 验证方法 | 预期结果 |
|------|---------|---------|
| 缺 PDF | 检查 JSONL 中 pdf="" | ✅ 仍输出基本信息 |
| 网络失败 | 模拟 HTTP 404 | ✅ 记录警告，继续 |
| 缺必需字段 | 修改 HTML 删除 title | ✅ 跳过该论文 |

---

## 总结

**核心原则**：
1. **零破坏性**：禁用 Pipeline 实现完全独立
2. **简单优先**：使用 Scrapy 标准模式
3. **优雅降级**：缺字段时仍输出有价值数据

**关键风险**：
- 网页结构变化 → CSS 选择器失效（通过多候选选择器缓解）
- OpenReview 链接缺失 → 优雅降级处理

**实际完成时间**：约 4 小时（含前端适配）
