# NeurIPS 论文爬取与 AI 增强 - 使用指南

> **快速开始**：一条龙完成 NeurIPS 论文的抓取、AI 分析和发布

---

## 📋 目录

- [快速开始](#快速开始)
- [完整流程](#完整流程)
- [查看结果](#查看结果)
- [故障排除](#故障排除)
- [技术说明](#技术说明)

---

## 🚀 快速开始

### 前置条件

1. **已配置好 `.env` 文件**（包含 API 密钥）
2. **已激活虚拟环境**：`.venv\Scripts\Activate.ps1`

### 一键运行（测试版）

```powershell
# 测试流程：爬取 5 篇论文
cd daily_arxiv
../.venv/Scripts/python.exe -m scrapy crawl neurips -o test.jsonl -s CLOSESPIDER_ITEMCOUNT=5

# AI 增强
cd ../ai
../.venv/Scripts/python.exe enhance.py --data ../daily_arxiv/test.jsonl --max_workers 2

# 转换为 Markdown
cd ../to_md
python convert.py --data ../daily_arxiv/test_AI_enhanced_Chinese.jsonl
```

---

## 📖 完整流程

### 步骤 1：爬取 NeurIPS 2024 Oral 论文

```powershell
cd daily_arxiv
../.venv/Scripts/python.exe -m scrapy crawl neurips -o ../data/neurips-2024-oral.jsonl
```

**预期输出**：
- 文件：`data/neurips-2024-oral.jsonl`
- 内容：50-80 篇 NeurIPS 2024 Oral 论文
- 耗时：5-10 分钟（礼貌爬取，1 秒/请求）

**验证爬取结果**：
```powershell
# 查看爬取的论文数量
cd ..
python -c "import json; papers = [json.loads(line) for line in open('data/neurips-2024-oral.jsonl')]; print(f'成功爬取 {len(papers)} 篇论文')"
```

---

### 步骤 2：AI 增强（生成中文结构化摘要）

```powershell
cd ai
../.venv/Scripts/python.exe enhance.py --data ../data/neurips-2024-oral.jsonl --max_workers 10
```

**参数说明**：
- `--max_workers 10`：并发数（根据 API 限流调整，建议 5-10）
- `--language Chinese`：输出语言（默认中文，已在 `.env` 配置）

**预期输出**：
- 文件：`data/neurips-2024-oral_AI_enhanced_Chinese.jsonl`
- 内容：包含 11 个 AI 字段（核心问题、方法、发现、大白话总结等）
- 耗时：10-20 分钟（取决于论文数量和并发数）

**验证 AI 增强结果**：
```powershell
# 检查 AI 增强成功率
python -c "import json; papers = [json.loads(line) for line in open('data/neurips-2024-oral_AI_enhanced_Chinese.jsonl')]; success = sum(1 for p in papers if 'AI' in p and 'core_problem' in p['AI']); print(f'AI 增强成功率: {success}/{len(papers)} ({success/len(papers)*100:.1f}%)')"
```

---

### 步骤 3：转换为 Markdown

```powershell
cd to_md
python convert.py --data ../data/neurips-2024-oral_AI_enhanced_Chinese.jsonl
```

**预期输出**：
- 文件：`data/neurips-2024-oral.md`
- 内容：格式化的 Markdown 文档，包含目录、AI 增强字段
- 耗时：< 1 秒

---

### 步骤 4：发布到 GitHub Pages（可选）

```powershell
# 提交到 Git
git add data/neurips-2024-oral.md data/neurips-2024-oral*.jsonl
git commit -m "Add NeurIPS 2024 Oral papers with AI enhancement"
git push

# GitHub Actions 自动构建并发布到 GitHub Pages
```

---

## 👀 查看结果

### 本地查看

**Markdown 文件**（最佳体验）：
```powershell
# 用 Markdown 编辑器打开
code data/neurips-2024-oral.md  # VSCode
# 或用浏览器打开预览版
```

**JSONL 原始数据**：
```powershell
# 查看第一篇论文（格式化）
python -c "import json; paper = json.loads(open('data/neurips-2024-oral_AI_enhanced_Chinese.jsonl').readline()); import pprint; pprint.pprint(paper)"
```

### GitHub Pages 在线查看

1. **等待 GitHub Actions 构建完成**（~2-5 分钟）
   - 访问：`https://github.com/你的用户名/2511-daily-arXiv/actions`
   - 确认 "pages build and deployment" 成功

2. **访问在线页面**：
   - URL：`https://你的用户名.github.io/2511-daily-arXiv/`
   - 在目录中找到 "NeurIPS 2024 Oral" 部分

---

## 🛠️ 故障排除

### 问题 1：爬虫返回 0 篇论文

**可能原因**：网页结构变化，CSS 选择器失效

**解决方法**：
```powershell
# 交互式调试
cd daily_arxiv
scrapy shell "https://neurips.cc/virtual/2024/events/oral"

# 在 shell 中测试选择器
>>> response.css('div.displaycards').getall()
```

### 问题 2：AI 增强失败率高

**可能原因**：
1. API 限流（429 错误）
2. 网络问题
3. API 密钥失效

**解决方法**：
```powershell
# 减少并发数
python enhance.py --data ../data/neurips-2024-oral.jsonl --max_workers 2

# 检查 API 配置
echo $env:OPENAI_API_KEY
echo $env:OPENAI_BASE_URL
```

### 问题 3：部分论文缺少 PDF 链接

**这是正常现象！** 部分 NeurIPS 论文详情页可能不包含 OpenReview 链接。

**验证统计**：
```python
import json
papers = [json.loads(line) for line in open('data/neurips-2024-oral.jsonl')]
no_pdf = sum(1 for p in papers if not p.get('pdf'))
print(f"缺少 PDF: {no_pdf}/{len(papers)} ({no_pdf/len(papers)*100:.1f}%)")
```

爬虫会优雅降级：缺少 PDF 的论文仍会输出完整的标题、作者、摘要等信息。

### 问题 4：代理问题（国内 API）

访问阿里百炼等国内 API 时需禁用代理：

```powershell
# 临时禁用代理（在运行 AI 增强前执行）
$env:HTTP_PROXY=""
$env:HTTPS_PROXY=""
$env:ALL_PROXY=""

# 然后运行 AI 增强
cd ai
python enhance.py --data ../data/neurips-2024-oral.jsonl --max_workers 10
```

---

## 🔧 技术说明

### 数据格式

**爬取输出（JSONL）**：
```json
{
  "id": "neurips2024_oral_97958",
  "title": "论文标题",
  "authors": ["作者1", "作者2"],
  "summary": "摘要文本",
  "abs": "https://neurips.cc/virtual/2024/oral/97958",
  "pdf": "https://openreview.net/pdf?id=ABC123",
  "categories": ["NeurIPS 2024 Oral"],
  "comment": null,
  "source": "neurips"
}
```

**AI 增强输出（JSONL）**：
```json
{
  // 原始字段...
  "AI": {
    "core_problem": "核心问题描述",
    "key_insight": "关键洞察",
    "method": "方法描述",
    "method_formula": "方法公式",
    "core_finding": "核心发现",
    "mechanism_insight": "机制洞察",
    "action_value": "行动价值",
    "transferability": "可迁移性",
    "value_score": "高价值",
    "summary_core": "核心总结",
    "summary_layman": "大白话总结"
  }
}
```

### 爬虫配置

**当前配置**（`neurips.py`）：
- **年份**：2024（可通过 `-a year=2023` 修改）
- **类别**：oral（可通过 `-a category=spotlight` 修改）
- **请求间隔**：1 秒（礼貌爬取）
- **并发**：1（单线程）
- **重试次数**：3 次

**扩展示例**：
```powershell
# 爬取 2023 年 Spotlight 论文
scrapy crawl neurips -a year=2023 -a category=spotlight -o neurips-2023-spotlight.jsonl
```

### 与 arXiv 爬虫的区别

| 特性 | arXiv 爬虫 | NeurIPS 爬虫 |
|------|-----------|--------------|
| **数据源** | arXiv API | NeurIPS 网页 |
| **Pipeline** | 启用（需 API 补全） | 禁用（直接输出） |
| **PDF 来源** | `arxiv.org/pdf/` | `openreview.net/pdf` |
| **运行频率** | 每日自动 | 年度手动 |
| **ID 格式** | `2024.12345` | `neurips2024_oral_97958` |

### 文件命名规范

**建议命名**：
- 原始数据：`neurips-{year}-{category}.jsonl`
- AI 增强：`neurips-{year}-{category}_AI_enhanced_Chinese.jsonl`
- Markdown：`neurips-{year}-{category}.md`

**示例**：
- `neurips-2024-oral.jsonl`
- `neurips-2024-oral_AI_enhanced_Chinese.jsonl`
- `neurips-2024-oral.md`

---

## 🎨 前端修改指南

### 数据流

```
爬虫 (neurips.py)
  ↓
JSONL 文件 (neurips-2024-oral_AI_enhanced_Chinese.jsonl)
  ↓
js/app.js (parseJSONL函数) - 数据映射
  ↓
paper 对象 - 内存中的论文数据
  ↓
renderPapers函数 - 生成卡片HTML
  ↓
浏览器显示
```

### 修改卡片显示的关键位置

**文件**：`js/app.js`

#### 1. 添加新字段（~740行）

在 `parseJSONL()` 函数中映射新字段：

```javascript
result[primaryCategory].push({
  title: paper.title,
  source: paper.source || 'arxiv',  // 添加来源字段
  core_finding: paper.AI && paper.AI.core_finding ? paper.AI.core_finding : '',
  // ... 其他字段
});
```

#### 2. 修改卡片内容（~1165行）

在 `renderPapers()` 函数中自定义卡片HTML：

```javascript
paperCard.innerHTML = `
  <div class="paper-card-header">
    <h3>${highlightedTitle}</h3>
    <p>${paper.summary_layman}</p>  <!-- 显示一句话总结 -->
    <span>📄 ${sourceDisplay}</span>  <!-- 显示来源 -->
  </div>
  <div class="paper-card-body">
    <p>${paper.core_finding}</p>  <!-- 显示核心发现 -->
  </div>
`;
```

#### 3. 本地测试

```powershell
python -m http.server 8000
# 访问 http://localhost:8000
```

### 常见修改场景

| 需求 | 修改位置 | 行号 |
|------|---------|------|
| 卡片显示新字段 | `parseJSONL()` + `renderPapers()` | ~740 + ~1165 |
| 修改详情弹窗 | `showPaperDetails()` | ~1200 |
| 修改搜索范围 | `performTextSearch()` | ~900 |

详细说明参见：`specs/neurips-paper-crawler/tasks.md#前端修改经验总结`

---

## 📚 相关文档

- **需求文档**：`specs/neurips-paper-crawler/requirements.md`
- **设计文档**：`specs/neurips-paper-crawler/design.md`
- **任务清单**：`specs/neurips-paper-crawler/tasks.md`（含前端修改经验）
- **项目说明**：`CLAUDE.md`（项目总体架构）

---

## 💡 最佳实践

### 首次运行建议

1. **先测试 5 篇**：使用 `-s CLOSESPIDER_ITEMCOUNT=5` 快速验证流程
2. **检查 API 配额**：确保 API 额度足够处理 50-80 篇论文
3. **调整并发数**：根据 API 限流情况调整 `--max_workers`
4. **保存原始数据**：在 AI 增强前备份 JSONL 文件

### 数据备份

```powershell
# 创建备份
mkdir -p backup
cp data/neurips-2024-oral*.jsonl backup/
```

### 性能优化

**加速爬取**（不推荐，可能被封禁）：
```python
# 修改 neurips.py 中的 custom_settings
'DOWNLOAD_DELAY': 0.5,  # 从 1 秒改为 0.5 秒
'CONCURRENT_REQUESTS': 2,  # 从 1 改为 2
```

**加速 AI 增强**：
```powershell
# 增加并发数（注意 API 限流）
python enhance.py --data ../data/neurips-2024-oral.jsonl --max_workers 20
```

---

## ✨ 总结

**完整流程三步走**：
1. 🕷️ **爬取**：`scrapy crawl neurips -o data/neurips-2024-oral.jsonl`
2. 🤖 **AI 增强**：`python ai/enhance.py --data data/neurips-2024-oral.jsonl --max_workers 10`
3. 📝 **转 Markdown**：`python to_md/convert.py --data data/neurips-2024-oral_AI_enhanced_Chinese.jsonl`

**查看结果**：
- 本地：`data/neurips-2024-oral.md`
- 在线：`https://你的用户名.github.io/2511-daily-arXiv/`

**预计耗时**：15-30 分钟（含 AI 增强）

---

*最后更新：2025-11-09*
