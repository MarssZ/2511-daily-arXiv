# 设计文档：daily-arXiv - AI驱动的论文母题筛选器

## 系统架构

### 整体流程

```
┌─────────────────────────────────────────────────────────────┐
│                      main.py (主入口)                         │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│  1. 配置加载 (config.py)                                      │
│     ├── 读取 .env (API密钥、Base URL)                        │
│     └── 读取 research_topics.txt (研究母题)                  │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│  2. 论文爬取 (fetcher.py)                                    │
│     ├── 从 arXiv RSS 获取论文                                │
│     ├── 解析 XML 提取字段                                    │
│     └── 返回 List[Paper]                                     │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│  3. 母题筛选 (filter.py)                                     │
│     ├── 对每篇论文调用 LLM                                   │
│     ├── 判断是否匹配研究母题                                  │
│     └── 返回 List[FilteredPaper]                             │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│  4. 摘要生成 (summarizer.py)                                 │
│     ├── 对通过筛选的论文调用 LLM                              │
│     ├── 生成中文摘要                                          │
│     └── 返回 List[SummarizedPaper]                           │
└────────────┬────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│  5. 输出格式化 (formatter.py)                                │
│     ├── 生成 Markdown 格式                                   │
│     ├── 保存到 output/YYYY-MM-DD.md                          │
│     └── 显示统计信息                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 数据结构设计

### 1. Paper（原始论文）

```python
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
```

**设计要点**：
- 所有字段都是从 arXiv RSS 解析得到，无需额外计算
- `authors` 存储为列表，方便后续格式化
- `categories` 支持多标签（一篇论文可能属于多个类别）

---

### 2. FilteredPaper（筛选后的论文）

```python
@dataclass
class FilteredPaper(Paper):
    """通过母题筛选的论文"""

    matched_topics: list[str]  # 匹配的母题列表
    match_reason: str          # 匹配原因（LLM 生成）
    filter_tokens: int         # 筛选消耗的 token 数

    def __str__(self) -> str:
        topics = ", ".join(self.matched_topics)
        return f"{self.title} (匹配: {topics})"
```

**设计要点**：
- 继承自 `Paper`，只增加筛选相关字段（"只增不改"原则）
- `matched_topics` 支持一篇论文匹配多个母题
- `filter_tokens` 用于成本统计

---

### 3. SummarizedPaper（包含摘要的论文）

```python
@dataclass
class SummarizedPaper(FilteredPaper):
    """包含 AI 生成摘要的论文"""

    summary_zh: str         # 中文摘要
    summary_tokens: int     # 摘要消耗的 token 数

    @property
    def total_tokens(self) -> int:
        """总 token 消耗（筛选 + 摘要）"""
        return self.filter_tokens + self.summary_tokens
```

**设计要点**：
- 继承自 `FilteredPaper`，形成继承链：`Paper → FilteredPaper → SummarizedPaper`
- 使用 `@property` 提供计算属性（总 token 数）
- 未来扩展时，只需在此基础上添加字段（如被引量、代码链接等）

---

## 核心模块设计

### 1. config.py - 配置管理

```python
import os
from pathlib import Path
from dotenv import load_dotenv

class Config:
    """全局配置管理"""

    def __init__(self):
        # 加载 .env 文件
        load_dotenv()

        # API 配置
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.model_name = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

        # arXiv 配置
        self.arxiv_categories = os.getenv("ARXIV_CATEGORIES", "cs.AI").split(",")
        self.max_papers_per_category = int(os.getenv("MAX_PAPERS_PER_CATEGORY", "50"))

        # 输出配置
        self.output_dir = Path(os.getenv("OUTPUT_DIR", "output"))
        self.output_language = os.getenv("OUTPUT_LANGUAGE", "zh")

        # 研究母题
        self.research_topics = self._load_research_topics()

    def _load_research_topics(self) -> list[str]:
        """从 config/research_topics.txt 加载研究母题"""
        topics_file = Path("config/research_topics.txt")
        if not topics_file.exists():
            raise FileNotFoundError(
                "未找到 config/research_topics.txt，请先创建该文件并添加研究母题"
            )

        topics = []
        with open(topics_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # 忽略空行和注释
                if line and not line.startswith("#"):
                    topics.append(line)

        if not topics:
            raise ValueError(
                "研究母题列表为空，请在 config/research_topics.txt 中添加至少一个母题"
            )

        return topics

    def validate(self):
        """验证配置完整性"""
        if not self.api_key:
            raise ValueError("未找到 API 密钥，请在 .env 文件中设置 OPENAI_API_KEY")

        # 创建输出目录
        self.output_dir.mkdir(exist_ok=True)
        (self.output_dir / "archive").mkdir(exist_ok=True)
```

**设计要点**：
- 单一职责：只负责配置加载和验证
- 错误提示友好：指向具体的配置文件和字段
- 自动创建输出目录（避免运行时报错）

---

### 2. fetcher.py - 论文爬取

```python
import feedparser
import requests
from datetime import datetime
from typing import List
from .models import Paper

def fetch_arxiv_papers(categories: list[str], max_results: int = 50) -> List[Paper]:
    """
    从 arXiv RSS 获取指定类别的论文

    Args:
        categories: arXiv 类别列表（如 ["cs.CV", "cs.AI"]）
        max_results: 每个类别最多爬取的论文数

    Returns:
        论文列表

    Raises:
        requests.RequestException: 网络连接失败
    """
    papers = []

    for category in categories:
        # 构建 arXiv API URL
        # 示例：http://export.arxiv.org/api/query?search_query=cat:cs.CV&max_results=50&sortBy=submittedDate&sortOrder=descending
        url = f"http://export.arxiv.org/api/query?search_query=cat:{category.strip()}&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"

        try:
            # 获取并解析 RSS feed
            feed = feedparser.parse(url)

            # 检查是否成功
            if feed.bozo:
                print(f"⚠️  警告：解析类别 {category} 时出错，跳过")
                continue

            # 提取论文信息
            for entry in feed.entries:
                paper = _parse_entry(entry, category)
                if paper:
                    papers.append(paper)

        except requests.RequestException as e:
            raise ConnectionError(
                f"无法连接到 arXiv，请检查网络连接。详细错误：{e}"
            )

    return papers


def _parse_entry(entry, category: str) -> Paper | None:
    """
    解析单个 RSS entry

    Args:
        entry: feedparser.FeedParserDict
        category: arXiv 类别

    Returns:
        Paper 对象或 None（解析失败时）
    """
    try:
        # 提取 arXiv ID（从 entry.id 中解析）
        # entry.id 格式：http://arxiv.org/abs/2401.12345v1
        arxiv_id = entry.id.split("/abs/")[-1].split("v")[0]

        # 提取作者列表
        authors = [author.name for author in entry.authors]

        # 提取发布日期
        published_date = datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%SZ")

        # 提取类别标签
        categories = [tag.term for tag in entry.tags]

        return Paper(
            title=entry.title.replace("\n", " ").strip(),
            abstract=entry.summary.replace("\n", " ").strip(),
            authors=authors,
            arxiv_id=arxiv_id,
            arxiv_url=f"https://arxiv.org/abs/{arxiv_id}",
            published_date=published_date,
            categories=categories,
        )

    except Exception as e:
        print(f"⚠️  警告：解析论文时出错，跳过。详细错误：{e}")
        return None
```

**设计要点**：
- 使用 `feedparser` 解析 arXiv RSS（比手写 XML 解析简单）
- 错误处理：网络失败抛出异常，单篇解析失败跳过并记录
- 分离 `_parse_entry`：便于单元测试

---

### 3. filter.py - 母题筛选

```python
from openai import OpenAI
from typing import List
from .models import Paper, FilteredPaper

def filter_papers_by_topics(
    papers: List[Paper],
    topics: List[str],
    llm_client: OpenAI
) -> List[FilteredPaper]:
    """
    使用 LLM 根据研究母题筛选论文

    Args:
        papers: 原始论文列表
        topics: 研究母题列表
        llm_client: LLM API 客户端

    Returns:
        通过筛选的论文列表
    """
    filtered_papers = []

    for i, paper in enumerate(papers, 1):
        print(f"🔍 筛选进度：{i}/{len(papers)} - {paper.title[:50]}...")

        # 构建 Prompt
        prompt = _build_filter_prompt(paper, topics)

        try:
            # 调用 LLM
            response = llm_client.chat.completions.create(
                model="deepseek-chat",  # 或从配置读取
                messages=[{"role": "user", "content": prompt}],
                temperature=0,  # 降低随机性，保证一致性
            )

            # 解析结果
            result = response.choices[0].message.content.strip()
            tokens = response.usage.total_tokens

            # 判断是否匹配
            if result.startswith("是"):
                # 提取匹配的母题和原因
                matched_topics, reason = _parse_filter_result(result, topics)

                filtered_papers.append(
                    FilteredPaper(
                        **paper.__dict__,
                        matched_topics=matched_topics,
                        match_reason=reason,
                        filter_tokens=tokens,
                    )
                )
                print(f"  ✅ 匹配母题：{', '.join(matched_topics)}")

        except Exception as e:
            print(f"  ⚠️  LLM 调用失败，跳过。错误：{e}")
            continue

    return filtered_papers


def _build_filter_prompt(paper: Paper, topics: List[str]) -> str:
    """构建母题筛选的 Prompt"""
    topics_str = "\n".join([f"{i+1}. {t}" for i, t in enumerate(topics)])

    return f"""论文标题：{paper.title}
论文摘要：{paper.abstract}

用户研究母题：
{topics_str}

判断：这篇论文是否直接解决上述任一母题?
要求：
- 只回答"是"或"否"
- 如果是，说明匹配的母题编号和简短原因（20字内）
- 如果论文只是略微相关，也应回答"否"

输出格式：
是/否
匹配母题：[编号]
原因：[简短说明]
"""


def _parse_filter_result(result: str, topics: List[str]) -> tuple[List[str], str]:
    """
    解析 LLM 筛选结果

    Returns:
        (匹配的母题列表, 匹配原因)
    """
    lines = result.split("\n")

    # 提取匹配的母题编号
    matched_indices = []
    reason = ""

    for line in lines:
        if line.startswith("匹配母题"):
            # 提取编号（如 "匹配母题：1, 3" → [1, 3]）
            numbers_str = line.split("：")[-1].strip()
            matched_indices = [int(n.strip()) for n in numbers_str.split(",")]

        elif line.startswith("原因"):
            reason = line.split("：")[-1].strip()

    # 将编号转换为母题文本
    matched_topics = [topics[i - 1] for i in matched_indices if 0 < i <= len(topics)]

    return matched_topics, reason
```

**设计要点**：
- Prompt 设计：明确输出格式，降低解析难度
- 温度设置为 0：保证结果一致性（不需要创造性）
- 错误处理：单篇失败不影响整体流程

---

### 4. summarizer.py - 摘要生成

```python
from openai import OpenAI
from typing import List
from .models import FilteredPaper, SummarizedPaper

def generate_summaries(
    papers: List[FilteredPaper],
    llm_client: OpenAI
) -> List[SummarizedPaper]:
    """
    为通过筛选的论文生成中文摘要

    Args:
        papers: 通过筛选的论文列表
        llm_client: LLM API 客户端

    Returns:
        包含摘要的论文列表
    """
    summarized_papers = []

    for i, paper in enumerate(papers, 1):
        print(f"📝 摘要进度：{i}/{len(papers)} - {paper.title[:50]}...")

        # 构建 Prompt
        prompt = _build_summary_prompt(paper)

        try:
            # 调用 LLM
            response = llm_client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,  # 稍高温度，生成更流畅的文本
            )

            # 提取摘要
            summary = response.choices[0].message.content.strip()
            tokens = response.usage.total_tokens

            summarized_papers.append(
                SummarizedPaper(
                    **paper.__dict__,
                    summary_zh=summary,
                    summary_tokens=tokens,
                )
            )

        except Exception as e:
            print(f"  ⚠️  LLM 调用失败，跳过。错误：{e}")
            continue

    return summarized_papers


def _build_summary_prompt(paper: FilteredPaper) -> str:
    """构建摘要生成的 Prompt"""
    topics_str = ", ".join(paper.matched_topics)

    return f"""论文标题：{paper.title}
论文摘要：{paper.abstract}
匹配的研究母题：{topics_str}

请生成一段 100 字的中文摘要，包含：
1. 核心贡献（这篇论文解决了什么问题？）
2. 技术方法（用了什么方法？）
3. 与研究母题的关联（为什么匹配"{topics_str}"这个母题？）

要求：
- 语言简洁、通俗易懂
- 避免专业术语堆砌
- 突出亮点和创新点
"""
```

**设计要点**：
- 温度设置为 0.3：保证流畅性，同时避免过度发散
- Prompt 包含匹配母题：让摘要更有针对性

---

### 5. formatter.py - 输出格式化

```python
from datetime import datetime
from pathlib import Path
from typing import List
from .models import SummarizedPaper

def format_as_markdown(papers: List[SummarizedPaper], stats: dict) -> str:
    """
    将论文列表格式化为 Markdown

    Args:
        papers: 包含摘要的论文列表
        stats: 统计信息（爬取数、筛选数、成本等）

    Returns:
        Markdown 格式的字符串
    """
    # 标题
    date_str = datetime.now().strftime("%Y-%m-%d")
    md = f"# arXiv 每日精选 - {date_str}\n\n"

    # 统计信息
    md += "## 📊 统计信息\n\n"
    md += f"- **爬取论文**：{stats['total_papers']} 篇\n"
    md += f"- **筛选后**：{stats['filtered_papers']} 篇（筛选率：{stats['filter_rate']:.1f}%）\n"
    md += f"- **成本**：¥{stats['total_cost']:.2f}\n"
    md += f"- **运行时间**：{stats['runtime']}\n\n"
    md += "---\n\n"

    # 论文列表
    md += "## 📄 论文列表\n\n"

    for i, paper in enumerate(papers, 1):
        md += f"### {i}. [{paper.title}]({paper.arxiv_url})\n\n"
        md += f"**作者**：{', '.join(paper.authors[:3])}{'...' if len(paper.authors) > 3 else ''}\n\n"
        md += f"**匹配母题**：{', '.join(paper.matched_topics)}\n\n"
        md += f"**摘要**：\n{paper.summary_zh}\n\n"
        md += f"**arXiv**：[{paper.arxiv_id}]({paper.arxiv_url})  \n"
        md += f"**发布日期**：{paper.published_date.strftime('%Y-%m-%d')}\n\n"
        md += "---\n\n"

    return md


def save_to_file(content: str, output_dir: Path) -> str:
    """
    保存到文件

    Args:
        content: Markdown 内容
        output_dir: 输出目录

    Returns:
        保存的文件路径
    """
    # 生成文件名
    date_str = datetime.now().strftime("%Y-%m-%d")
    file_path = output_dir / f"{date_str}.md"

    # 保存
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return str(file_path)
```

**设计要点**：
- Markdown 格式适合导入 Obsidian
- 作者列表超过 3 人时省略（避免过长）
- 使用 `---` 分隔论文（提高可读性）

---

## 性能优化（二期）

**当前不做，但保留接口**：

### 1. 并发处理

```python
import asyncio
from openai import AsyncOpenAI

async def filter_papers_async(papers: List[Paper], topics: List[str]) -> List[FilteredPaper]:
    """异步筛选论文（并发调用 LLM）"""
    async with AsyncOpenAI() as client:
        tasks = [_filter_single_paper(p, topics, client) for p in papers]
        results = await asyncio.gather(*tasks)
    return [r for r in results if r is not None]
```

### 2. 缓存机制

```python
import sqlite3
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_cached_summary(arxiv_id: str) -> str | None:
    """从缓存中获取摘要（避免重复调用 LLM）"""
    conn = sqlite3.connect("cache.db")
    cursor = conn.execute("SELECT summary FROM papers WHERE arxiv_id = ?", (arxiv_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
```

---

## 错误处理策略

### 1. API 调用失败

```python
import time
from openai import OpenAIError

def call_llm_with_retry(prompt: str, max_retries: int = 3) -> str:
    """带重试的 LLM 调用"""
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(...)
            return response.choices[0].message.content

        except OpenAIError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 指数退避
                print(f"⚠️  LLM 调用失败，{wait_time}秒后重试...")
                time.sleep(wait_time)
            else:
                raise
```

### 2. 网络超时

```python
import requests

def fetch_with_timeout(url: str, timeout: int = 10) -> str:
    """带超时的 HTTP 请求"""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text

    except requests.Timeout:
        raise TimeoutError(f"请求超时（{timeout}秒），请检查网络连接")

    except requests.RequestException as e:
        raise ConnectionError(f"网络请求失败：{e}")
```

---

## 成本估算

### Token 计算

```python
def estimate_cost(papers: List[SummarizedPaper]) -> dict:
    """估算成本"""
    total_tokens = sum(p.total_tokens for p in papers)

    # DeepSeek 价格：¥0.001/1K tokens
    total_cost = (total_tokens / 1000) * 0.001

    return {
        "total_tokens": total_tokens,
        "total_cost": total_cost,
        "avg_tokens_per_paper": total_tokens / len(papers) if papers else 0,
    }
```

---

## 测试策略

### 单元测试

```python
# tests/test_filter.py
import pytest
from src.filter import _parse_filter_result

def test_parse_filter_result():
    """测试筛选结果解析"""
    topics = ["AI Agent 的工具调用优化", "长视频理解的效率问题"]
    result = """是
匹配母题：1
原因：提出了新的工具调用优化方法"""

    matched_topics, reason = _parse_filter_result(result, topics)

    assert matched_topics == ["AI Agent 的工具调用优化"]
    assert reason == "提出了新的工具调用优化方法"
```

### 集成测试

```python
# tests/test_integration.py
def test_full_pipeline(tmp_path):
    """测试完整流程"""
    # 1. 创建测试配置
    config = Config()
    config.output_dir = tmp_path

    # 2. 爬取论文（使用 mock）
    papers = fetch_arxiv_papers(["cs.AI"], max_results=10)
    assert len(papers) > 0

    # 3. 筛选
    filtered = filter_papers_by_topics(papers, ["AI Agent"], llm_client)
    assert len(filtered) > 0

    # 4. 摘要
    summarized = generate_summaries(filtered, llm_client)
    assert len(summarized) == len(filtered)

    # 5. 输出
    md = format_as_markdown(summarized, stats)
    file_path = save_to_file(md, tmp_path)

    assert Path(file_path).exists()
```

---

## 相关文档

- **[requirements.md](requirements.md)**：需求文档（用户故事、验收标准）
- **[../CLAUDE.md](../CLAUDE.md)**：项目总览（给 AI 和开发者看）
- **[../README.md](../README.md)**：用户使用指南
