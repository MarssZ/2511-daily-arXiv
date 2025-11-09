# 需求文档：NeurIPS 会议论文爬取与增强

## 目标

扩展现有爬虫系统，支持 NeurIPS 会议论文的自动爬取，复用 AI 增强流程。

**当前范围**：NeurIPS 2024 Oral 论文（~70篇）
**未来扩展**：Spotlight 论文、历史年份、PDF 全文分析

---

## 核心需求

### REQ-1：爬取 NeurIPS 论文 ✅

- 从 `neurips.cc` 爬取 Oral 论文列表
- 提取字段：title, authors, summary, abs, pdf
- ID 格式：`neurips2024_oral_{id}`
- 礼貌爬取：1秒/请求

### REQ-2：数据标准化 ✅

输出 JSONL 格式，与 arXiv 兼容：

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

### REQ-3：AI 增强集成 ✅

- 直接使用 `ai/enhance.py`
- 输出包含 11 个 AI 字段（由 `ai/structure.py` 定义）
- `source` 字段透传

### REQ-4：前端展示 ✅

- Conference Papers 双视图模式
- 卡片显示：来源标识、核心发现、价值评分
- Modal 展示：完整的 11 个 AI 字段

### REQ-5：独立运行

- 独立爬虫命令：`scrapy crawl neurips`
- 不依赖 arXiv Pipeline
- 支持参数：`-a year=2024 -a category=oral`

---

## 实现状态

| 需求 | 状态 | 文件 |
|------|-----|------|
| 爬虫实现 | ✅ | `spiders/neurips.py` |
| AI 增强 | ✅ | 无需修改 |
| Markdown 转换 | ✅ | 无需修改 |
| Conference 模式 | ✅ | `js/conference.js` |
| 卡片优化 | ✅ | `js/app.js` (~740, ~1165) |

---

## 技术约束

- 必须使用 Scrapy（与现有系统一致）
- 输出 JSONL 格式（与 arXiv 一致）
- 零破坏性（不修改 arXiv 爬虫）
- 优雅降级（缺 PDF 时仍输出）
