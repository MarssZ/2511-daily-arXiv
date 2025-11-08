"""数据结构定义"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Paper:
    """arXiv 论文的原始数据"""

    title: str              # 论文标题
    abstract: str           # 论文摘要（英文原文）
    authors: list[str]      # 作者列表
    arxiv_id: str           # arXiv ID（如 2401.12345）
    arxiv_url: str          # arXiv 链接
    published_date: datetime # 发布日期
    categories: list[str]   # 类别标签（如 ["cs.CV", "cs.AI"]）

    def __str__(self) -> str:
        return f"{self.title} ({self.arxiv_id})"


@dataclass
class FilteredPaper(Paper):
    """通过母题筛选的论文"""

    matched_topics: list[str]  # 匹配的母题列表
    match_reason: str          # 匹配原因（LLM 生成）
    filter_tokens: int         # 筛选消耗的 token 数

    def __str__(self) -> str:
        topics = ", ".join(self.matched_topics)
        return f"{self.title} (匹配: {topics})"


@dataclass
class SummarizedPaper(FilteredPaper):
    """包含 AI 生成摘要的论文"""

    summary_zh: str         # 中文摘要
    summary_tokens: int     # 摘要消耗的 token 数

    @property
    def total_tokens(self) -> int:
        """总 token 消耗（筛选 + 摘要）"""
        return self.filter_tokens + self.summary_tokens
