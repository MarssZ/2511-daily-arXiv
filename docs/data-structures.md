# 数据结构设计

> **导航**: [← 返回主文档](../CLAUDE.md) | [核心工作流](workflows.md) | [v2.0 设计](v2-design.md) | [AI 模块](../ai/README.md)

本文档详细说明了项目中使用的所有数据结构。

## v1.0 数据结构（当前版本）

### 1. Scrapy 输出（JSONL）

爬虫抓取的原始论文数据：

```json
{
  "id": "2401.12345",
  "title": "Attention Is All You Need",
  "authors": ["Ashish Vaswani", "Noam Shazeer", ...],
  "categories": ["cs.CL", "cs.AI"],
  "summary": "The dominant sequence transduction models...",
  "abs": "https://arxiv.org/abs/2401.12345"
}
```

**字段说明：**
- `id`: arXiv 论文 ID
- `title`: 论文标题
- `authors`: 作者列表
- `categories`: 分类标签（如 cs.AI, cs.CL）
- `summary`: 论文摘要（英文原文）
- `abs`: arXiv 论文链接

### 2. AI 增强输出（JSONL）

经过 LLM 处理后的论文数据，包含 5 个结构化字段：

```json
{
  "id": "2401.12345",
  "title": "Attention Is All You Need",
  "authors": ["Ashish Vaswani", ...],
  "categories": ["cs.CL", "cs.AI"],
  "summary": "The dominant sequence transduction models...",
  "abs": "https://arxiv.org/abs/2401.12345",
  "AI": {
    "tldr": "提出了 Transformer 模型，完全基于注意力机制...",
    "motivation": "现有序列模型依赖 RNN，训练效率低...",
    "method": "使用自注意力机制和位置编码...",
    "result": "在 WMT 翻译任务上达到 SOTA...",
    "conclusion": "注意力机制可以完全替代循环网络..."
  }
}
```

**AI 字段说明：**
- `tldr`: Too Long; Didn't Read - 一句话总结
- `motivation`: 论文动机和研究背景
- `method`: 方法论和技术方案
- `result`: 实验结果和性能数据
- `conclusion`: 结论和未来工作

### 3. Structure 定义（Pydantic）

Python 代码中的数据结构定义（`ai/structure.py`）：

```python
from pydantic import BaseModel, Field

class Structure(BaseModel):
    tldr: str = Field(description="generate a too long; didn't read summary")
    motivation: str = Field(description="describe the motivation in this paper")
    method: str = Field(description="method of this paper")
    result: str = Field(description="result of this paper")
    conclusion: str = Field(description="conclusion of this paper")
```

## v2.0 数据结构（计划中）

### 数据流演进

```
v1.0：Scrapy JSONL → AI Enhanced JSONL → Markdown

v2.0：Scrapy JSONL → 🆕 Filtered JSONL → AI Enhanced JSONL → Markdown
```

v2.0 在爬虫和 AI 增强之间插入**母题筛选**步骤，只对相关论文生成摘要。

### Filtered JSONL（母题筛选后）

```json
{
  "id": "2401.12345",
  "title": "Attention Is All You Need",
  "authors": ["Ashish Vaswani", ...],
  "categories": ["cs.CL", "cs.AI"],
  "summary": "The dominant sequence transduction models...",
  "abs": "https://arxiv.org/abs/2401.12345",
  "filter": {
    "matched_topics": ["AI Agent 的工具调用优化"],
    "match_reason": "提出了基于注意力机制的新架构，可优化 Agent 的上下文理解能力",
    "filter_tokens": 500
  }
}
```

**filter 字段说明：**
- `matched_topics`: 匹配的研究母题列表
- `match_reason`: LLM 生成的匹配原因
- `filter_tokens`: 筛选过程消耗的 token 数

### Python 数据模型（src/models.py）

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Paper:
    """arXiv 论文的原始数据（对应 Scrapy 输出）"""
    title: str              # 论文标题
    abstract: str           # 论文摘要（英文原文）
    authors: list[str]      # 作者列表
    arxiv_id: str           # arXiv ID（如 2401.12345）
    arxiv_url: str          # arXiv 链接
    published_date: datetime # 发布日期
    categories: list[str]   # 类别标签（如 ["cs.CV", "cs.AI"]）

@dataclass
class FilteredPaper(Paper):
    """通过母题筛选的论文（v2.0 新增）"""
    matched_topics: list[str]  # 匹配的母题列表
    match_reason: str          # 匹配原因（LLM 生成）
    filter_tokens: int         # 筛选消耗的 token 数

@dataclass
class SummarizedPaper(FilteredPaper):
    """包含 AI 生成摘要的论文（v2.0 扩展）"""
    summary_zh: str         # 中文摘要
    summary_tokens: int     # 摘要消耗的 token 数

    @property
    def total_tokens(self) -> int:
        """总 token 消耗（筛选 + 摘要）"""
        return self.filter_tokens + self.summary_tokens
```

## 设计原则

1. **向后兼容** - v2.0 的数据结构继承自 v1.0
2. **增量扩展** - 通过添加字段而非修改现有字段
3. **元数据分离** - 将筛选和摘要的元数据（如 token 消耗）单独存储
4. **类型安全** - 使用 Pydantic 和 dataclass 确保类型正确

## 相关文档

- [核心工作流](workflows.md) - 了解数据如何在各个阶段流转
- [v2.0 设计](v2-design.md) - 母题筛选功能的详细设计
- [AI 模块](../ai/README.md) - AI 增强的实现细节
