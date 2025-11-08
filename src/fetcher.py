"""arXiv 论文爬取"""

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
        ConnectionError: 网络连接失败
    """
    papers = []

    for category in categories:
        print(f"📥 正在爬取类别：{category.strip()}")

        # 构建 arXiv API URL
        url = (
            f"http://export.arxiv.org/api/query?"
            f"search_query=cat:{category.strip()}&"
            f"max_results={max_results}&"
            f"sortBy=submittedDate&"
            f"sortOrder=descending"
        )

        try:
            # 获取并解析 RSS feed
            feed = feedparser.parse(url)

            # 检查是否成功
            if feed.bozo:
                print(f"  ⚠️  警告：解析类别 {category} 时出错，跳过")
                continue

            # 提取论文信息
            for entry in feed.entries:
                paper = _parse_entry(entry, category)
                if paper:
                    papers.append(paper)

            print(f"  ✅ 成功爬取 {len(feed.entries)} 篇论文")

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
        print(f"  ⚠️  警告：解析论文时出错，跳过。详细错误：{e}")
        return None
