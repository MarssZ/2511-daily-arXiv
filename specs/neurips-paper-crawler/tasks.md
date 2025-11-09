# 任务清单：NeurIPS 会议论文爬取与增强

> **实用主义原则**：合并细碎任务，关注可交付成果

---

## 阶段 1：核心爬虫实现（P0）✅ **已完成**

- [x] **任务 1：实现 NeurIPS 爬虫核心功能**
  - 文件：`daily_arxiv/daily_arxiv/spiders/neurips.py`
  - 完成内容：
    - ✅ Spider 骨架（支持 `year` 和 `category` 参数）
    - ✅ 列表页解析（提取 title, authors, summary）
    - ✅ 详情页解析（提取 OpenReview 链接，生成 PDF URL）
    - ✅ ID 生成逻辑（`neurips2024_oral_{id}`）
    - ✅ 数据标准化输出（JSONL 格式，与 arXiv 兼容）
    - ✅ 优雅降级（缺 PDF 时仍输出基本信息）
    - ✅ 必需字段验证（title/summary 缺失则跳过）
    - ✅ 错误处理和统计（失败计数、PDF 缺失统计）
  - 验证结果：
    - ✅ 成功爬取 72 篇 NeurIPS 2024 Oral 论文列表
    - ✅ 测试数据（6 篇）全部通过字段验证
    - ✅ 优雅降级生效（2 篇缺 PDF 但仍输出）
    - ✅ 统计信息正常显示
  - 耗时：约 2 小时

---

## 阶段 2：AI 增强集成验证（P1）✅ **已完成**

- [x] **任务 2：测试 AI 增强流程兼容性**
  - 需求：REQ-4.1, REQ-4.2, REQ-4.3
  - 执行命令：
    ```powershell
    cd ai
    ../.venv/Scripts/python.exe enhance.py --data ../daily_arxiv/test-5.jsonl --max_workers 2
    ```
  - 验证结果：
    - ✅ 生成 `test-5_AI_enhanced_Chinese.jsonl`（35KB）
    - ✅ 所有 6 篇论文 AI 增强 100% 成功
    - ✅ 包含全部 11 个 AI 结构化字段（由 `structure.py` 定义）
    - ✅ `source: "neurips"` 字段正确透传
  - 实际耗时：1分03秒

- [x] **任务 3：测试 Markdown 转换兼容性**
  - 需求：REQ-5.1, REQ-5.5
  - 执行命令：
    ```powershell
    cd to_md
    python convert.py --data ../daily_arxiv/test-5_AI_enhanced_Chinese.jsonl
    ```
  - 验证结果：
    - ✅ 生成 `daily.md`（包含 6 篇 NeurIPS 论文）
    - ✅ 格式完整（标题、作者、摘要、AI 增强字段可见）
    - ✅ 无乱码，中文显示正常
  - 实际耗时：< 1秒
  - **备注**：输出文件名由输入路径决定，`../daily_arxiv/test-5_...` → `daily.md`

---

## 阶段 3：完整流程测试（P1）

- [ ] **任务 4：完整爬取所有 NeurIPS 2024 Oral 论文**
  - 需求：REQ-1 至 REQ-7（所有需求）
  - 执行：
    ```powershell
    cd daily_arxiv
    ../.venv/Scripts/python.exe -m scrapy crawl neurips -o ../data/neurips-2024-oral.jsonl
    ```
  - 验证目标：
    - [ ] 成功爬取 50+ 篇论文
    - [ ] 失败率 < 10%
    - [ ] 手动抽查 3 篇数据质量
  - 预计耗时：5-10 分钟

- [ ] **任务 5：完整 AI 增强流程**
  - 需求：REQ-4
  - 执行：
    ```powershell
    cd ai
    ../.venv/Scripts/python.exe enhance.py --data ../data/neurips-2024-oral.jsonl --max_workers 10
    ```
  - 验证目标：
    - [ ] 生成 `neurips-2024-oral_AI_enhanced_Chinese.jsonl`
    - [ ] AI 增强成功率 > 90%
  - 预计耗时：10-20 分钟

- [ ] **任务 6：生成最终 Markdown 文件**
  - 需求：REQ-5
  - 执行：
    ```powershell
    cd to_md
    python convert.py --data ../data/neurips-2024-oral_AI_enhanced_Chinese.jsonl
    ```
  - 验证目标：
    - [ ] 生成 `neurips-2024-oral.md`
    - [ ] 目录包含 "NeurIPS 2024 Oral"
    - [ ] 随机抽查 3 篇格式正确
  - 预计耗时：~30 秒

---

## 阶段 4：发布与文档（P2）✅ **已完成**

- [x] **任务 7：更新项目文档**
  - 文件：`README.md`, `CLAUDE.md`
  - 完成内容：
    - ✅ 添加 NeurIPS 爬虫使用说明（README.md）
    - ✅ 添加示例命令和三步走流程
    - ✅ 更新 CLAUDE.md 项目架构说明
    - ✅ 创建 NeurIPS 爬虫专用 README（specs/neurips-paper-crawler/README.md）
  - 实际耗时：10 分钟

- [x] **任务 8：Conference Papers 功能实现**
  - 需求：解决 NeurIPS 论文展示问题（选项C：扩展index.html支持会议分类）
  - 执行：
    - ✅ 实现双视图导航（Daily Papers ↔ Conference Papers）
    - ✅ 添加 View Mode 切换 UI（Daily/Conference 按钮）
    - ✅ 创建 Conference Selector 和 Modal Picker
    - ✅ 实现 conference-list.json 数据加载
    - ✅ 新增 js/conference.js 模块（221行）
    - ✅ 添加 CSS 样式（200+行）
    - ✅ 创建测试清单（conference-mode-test.md）
  - 验证结果：
    - ✅ 本地测试通过（http://localhost:8000）
    - ✅ 6篇NeurIPS测试论文可在Conference模式查看
    - ✅ Daily模式功能零影响
    - ✅ 已推送到 GitHub
  - 实际耗时：1 小时

- [x] **任务 9：理解数据流和展示逻辑**
  - 完成内容：
    - ✅ 梳理完整数据流（爬虫→AI增强→index.html）
    - ✅ 发现 file-list.txt 未更新导致日期选择器问题
    - ✅ 修复并推送 file-list.txt
    - ✅ 理解 index.html 只读取 JSONL 不读取 Markdown
  - 实际耗时：30 分钟

- [ ] **任务 10：清理测试文件**
  - 执行：
    - [ ] 删除或归档测试文件：
      - `daily_arxiv/test.jsonl`
      - `daily_arxiv/test-5.jsonl`
      - 相关 AI 增强输出
    - [ ] 移除验证脚本 `verify_neurips_output.py`（或移到 `tools/`）
  - 预计耗时：< 1 分钟

---

## 阶段 5：前端数据结构适配（P1）⚠️ **新增任务**

### **问题描述**

**当前状态**：前端 `index.html` 和后端 AI 增强使用的数据结构不一致

| 组件 | 使用的字段 | 定义位置 |
|------|-----------|----------|
| **后端 AI 增强** | 11个字段 | `ai/structure.py` |
| **前端展示** | 5个旧字段 | `js/app.js` (硬编码) |

**具体不一致**：

**后端输出（structure.py）**：
```python
class Structure(BaseModel):
    core_problem: str      # 根本问题
    key_insight: str       # 切入视角
    method: str            # 关键方法
    method_formula: str    # 方法公式化
    core_finding: str      # 核心发现
    mechanism_insight: str # 机制洞察
    action_value: str      # 行动启发
    transferability: str   # 可迁移性
    value_score: str       # 价值评分
    summary_core: str      # 一句话总结（核心价值）
    summary_layman: str    # 一句话总结（大白话版）
```

**前端期待（js/app.js:729-743）**：
```javascript
const summary = paper.AI && paper.AI.tldr ? paper.AI.tldr : paper.summary;  // ❌ 不存在
motivation: paper.AI && paper.AI.motivation ? paper.AI.motivation : '',    // ❌ 不存在
method: paper.AI && paper.AI.method ? paper.AI.method : '',                // ✅ 存在但含义不同
result: paper.AI && paper.AI.result ? paper.AI.result : '',                // ❌ 不存在
conclusion: paper.AI && paper.AI.conclusion ? paper.AI.conclusion : ''     // ❌ 不存在
```

**Modal 展示（js/app.js:1237-1240）**：
```javascript
${paper.motivation ? `<div class="paper-section"><h4>Motivation</h4><p>${highlightedMotivation}</p></div>` : ''}
${paper.method ? `<div class="paper-section"><h4>Method</h4><p>${highlightedMethod}</p></div>` : ''}
${paper.result ? `<div class="paper-section"><h4>Result</h4><p>${highlightedResult}</p></div>` : ''}
${paper.conclusion ? `<div class="paper-section"><h4>Conclusion</h4><p>${highlightedConclusion}</p></div>` : ''}
```

**影响**：
- ❌ 详情弹窗中 AI 增强字段**全部显示为空**
- ❌ 浪费了 AI 增强的所有结构化数据
- ❌ 用户只能看到原始 summary，看不到 11 个高价值字段

---

- [x] **任务 11：修改前端以支持 structure.py 定义的 11 个 AI 字段**
  - 需求：前端展示与后端数据结构保持一致
  - 执行文件：
    - [x] `js/app.js` - 修改数据映射逻辑（Line 729-751）
    - [x] `js/app.js` - 修改 Modal 展示逻辑（Line 1210-1283）
    - [x] `js/app.js` - 修改文本搜索字段引用（Line 877-945）
  - 验证结果：
    - ✅ 数据映射：11个字段正确映射
    - ✅ Modal展示：带emoji图标，按逻辑分组
    - ✅ 文本搜索：覆盖所有新字段
    - ✅ 本地测试：http://localhost:8000 显示正常
  - 实际耗时：20 分钟

- [x] **任务 12：优化主页卡片展示内容**
  - 需求：卡片显示高信息量内容，而非低价值的大白话
  - 执行文件：
    - [x] `js/app.js` - 添加 `source` 字段映射（Line 740）
    - [x] `js/app.js` - 修改卡片布局逻辑（Line 1149-1189）
  - 修改内容：
    - ✅ `paper-card-authors` → 显示 `summary_layman`（一句话总结）
    - ✅ `paper-card-categories` → 显示来源标识（📄 NeurIPS/arXiv）
    - ✅ `paper-card-body` → 优先显示 `core_finding` + `mechanism_insight`
    - ✅ `footer` → 显示日期 + 分类标签 + ⭐ value_score
  - 验证结果：
    - ✅ 卡片立即显示核心发现和机制洞察
    - ✅ 来源标识（NeurIPS红色/arXiv蓝色）显著可见
    - ✅ 价值评分在footer右侧突出显示
    - ✅ 本地测试：http://localhost:8000 显示正常
  - 实际耗时：10 分钟

---

## 任务统计

### 按阶段
- **阶段 1（P0 核心功能）**：✅ 已完成（1 个任务，耗时 2 小时）
- **阶段 2（P1 集成测试）**：✅ 已完成（2 个任务，耗时 1 分钟）
- **阶段 3（P1 完整流程）**：⏳ 待开始（3 个任务）
- **阶段 4（P2 发布文档）**：✅ 大部分完成（3/4 个任务，耗时 1.5 小时）
- **阶段 5（P1 前端适配）**：✅ 已完成（2 个任务，耗时 30 分钟）

### 实际总时间
- **核心实现（P0）**：✅ 2 小时
- **集成测试（P1）**：✅ 1 分钟
- **Conference Papers 功能**：✅ 1.5 小时
- **前端适配（P1）**：✅ 30 分钟（任务11+12）
- **完整流程（P1）**：⏳ 15-30 分钟（待执行）
- **总计已完成**：约 4 小时
- **总计预估**：约 4.5 小时

---

## 🎯 前端修改经验总结

### 数据流理解

```
爬虫 → JSONL → js/app.js (parseJSONL) → paper 对象 → renderPapers → 卡片HTML
```

**关键文件**：`js/app.js`（~1500行）

### 修改卡片展示的关键位置

#### 1. 数据映射（~731行）

**位置**：`parseJSONL()` 函数中的 `result[primaryCategory].push({...})`

**作用**：将 JSONL 中的字段映射到前端 paper 对象

**示例**：
```javascript
// 添加新字段
result[primaryCategory].push({
  title: paper.title,
  source: paper.source || 'arxiv',  // ← 新增字段
  core_finding: paper.AI && paper.AI.core_finding ? paper.AI.core_finding : '',
  // ...
});
```

#### 2. 卡片渲染（~1165行）

**位置**：`renderPapers()` 函数中的 `paperCard.innerHTML = ...`

**作用**：生成每个卡片的 HTML 结构

**关键变量**：
- `highlightedTitle`：高亮后的标题
- `highlightedSummary`：高亮后的摘要
- `categoryTags`：分类标签HTML

**示例修改**：
```javascript
// 自定义卡片内容
const cardContent = paper.core_finding || paper.mechanism_insight
  ? `核心发现：${paper.core_finding}<br>机制洞察：${paper.mechanism_insight}`
  : highlightedSummary;

paperCard.innerHTML = `
  <div class="paper-card-header">
    <h3>${highlightedTitle}</h3>
    <p>${paper.summary_layman}</p>  <!-- 替换作者为一句话总结 -->
    <span>📄 ${sourceDisplay}</span>  <!-- 添加来源标识 -->
  </div>
  <div class="paper-card-body">
    <p>${cardContent}</p>  <!-- 使用自定义内容 -->
  </div>
`;
```

#### 3. Modal 弹窗（~1200行）

**位置**：`showPaperDetails()` 函数

**作用**：生成详情弹窗内容

### 典型修改场景

| 需求 | 修改位置 | 代码行数 |
|------|---------|---------|
| 添加新字段到 paper 对象 | `parseJSONL()` | ~740 |
| 修改卡片显示内容 | `renderPapers()` | ~1165 |
| 修改详情弹窗内容 | `showPaperDetails()` | ~1200 |
| 修改搜索字段 | `performTextSearch()` | ~900 |

### 调试技巧

1. **查看 paper 对象结构**
   ```javascript
   // 在浏览器控制台
   console.log(window.allPapers[0]);  // 查看第一篇论文的完整对象
   ```

2. **本地测试**
   ```powershell
   python -m http.server 8000
   # 访问 http://localhost:8000
   ```

3. **检查字段是否存在**
   ```javascript
   // 在卡片渲染前添加
   console.log('Available fields:', Object.keys(paper));
   ```

---

## 关键提示

### 调试技巧
1. **查看 Scrapy 日志**：添加 `-s LOG_LEVEL=DEBUG` 查看详细日志
2. **限制爬取数量**：使用 `-s CLOSESPIDER_ITEMCOUNT=N` 快速测试
3. **检查 HTML 结构**：使用 `scrapy shell "https://neurips.cc/virtual/2024/events/oral"` 交互式调试

### 常见问题
1. **CSS 选择器失效**：网页结构可能变化，需要调整选择器
2. **OpenReview 链接格式变化**：检查实际 URL 格式，调整正则表达式
3. **AI 增强超时**：减少 `--max_workers` 或增加超时时间

### 快速验证脚本

**验证 JSONL 数据质量**：
```python
import json
with open('data/neurips-2024-oral.jsonl') as f:
    items = [json.loads(line) for line in f]
    print(f"总计: {len(items)} 篇")
    required = ['id', 'title', 'authors', 'summary', 'abs', 'pdf', 'categories', 'source']
    for item in items[:3]:  # 抽查前3篇
        assert all(field in item for field in required)
        print(f"✓ {item['id']}: {item['title'][:60]}...")
    print("✅ 验证通过")
```

**检查 AI 增强完成率**：
```python
import json
with open('data/neurips-2024-oral_AI_enhanced_Chinese.jsonl') as f:
    items = [json.loads(line) for line in f]
    success = sum(1 for item in items if 'AI' in item and 'core_problem' in item['AI'])
    print(f"AI 增强成功率: {success}/{len(items)} ({success/len(items)*100:.1f}%)")
```

---

## 验收测试场景（对应需求文档）

### 场景 1：首次爬取 NeurIPS 2024 Oral ✅
- **覆盖任务**：1, 2, 3, 4, 5, 6
- **状态**：阶段 1 已完成，待执行阶段 2-3

### 场景 2：与 arXiv 爬虫并行（可选）
- **验证**：
  - 打开两个终端
  - 终端 1：`scrapy crawl arxiv -o test-arxiv.jsonl -s CLOSESPIDER_ITEMCOUNT=5`
  - 终端 2：`scrapy crawl neurips -o test-neurips.jsonl -s CLOSESPIDER_ITEMCOUNT=5`
  - 检查两个爬虫互不干扰
- **预计耗时**：~2 分钟

### 场景 3：网络异常恢复 ✅
- **状态**：已通过（优雅降级测试中 2 篇缺 PDF 仍成功输出）
