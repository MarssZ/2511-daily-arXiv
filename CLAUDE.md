# 项目：daily-arXiv - AI驱动的 arXiv 论文增强工具

## 项目定位

**一句话描述：**
基于 AI 的 arXiv 论文自动抓取、结构化摘要和 Markdown 发布工具，使用 LLM 生成高质量论文摘要。**v2.0 将增加母题筛选功能，实现零漏报 + 80% 降噪。**

**当前版本 (v1.0) 特点：**
- **零基础设施**：基于 GitHub Actions + Pages，无需服务器
- **AI 驱动摘要**：使用 DeepSeek 生成结构化论文摘要（TLDR、动机、方法、结果、结论）
- **成本极低**：约 ¥0.2/天
- **完全自动化**：每日自动运行，自动发布到 GitHub Pages

**升级计划 (v2.0)：**
- **母题筛选**：使用 LLM 理解用户关心的研究母题（Research Topics）
- **成本优化**：只对相关论文生成摘要，成本降低 80%
- **精准推送**：零漏报（语义理解） + 80% 降噪（过滤无关论文）
- **个性化**：每个用户可配置自己的研究母题列表

**目标用户：**
- 科研人员（需要追踪特定研究方向，而非整个类别）
- 技术团队（需要监控特定技术趋势）
- 个人学习者（需要高质量论文摘要 + 个性化筛选）

**项目来源：**
本项目基于 [dw-dengwei/daily-arXiv-ai-enhanced](https://github.com/dw-dengwei/daily-arXiv-ai-enhanced) 进行定制化开发。

---

## 技术栈

**实用主义：Production-Ready**

- **语言**：Python 3.12+
- **核心依赖 (v1.0)**：
  - `scrapy` - 网页爬虫框架
  - `langchain` + `langchain-openai` - LLM 集成和结构化输出
  - `python-dotenv` - 环境变量管理
  - `tqdm` - 进度条显示
- **新增依赖 (v2.0 母题筛选)**：
  - `feedparser` - 可选的轻量级爬取方案
  - `openai` - 直接调用 OpenAI 兼容 API（用于筛选）
  - `pytest` - 单元测试

---

## 本地环境

- **操作系统**：Windows 11
- **工作目录**：`E:\MarssPython\2511-daily-arXiv`
- **Python 版本**：3.12+ (实际使用 3.12.9，由 uv 管理)
- **包管理器**：uv (快速、现代的 Python 包管理器)
- **虚拟环境**：`.venv` (由 uv 自动创建和管理)

---

## 📁 项目结构

### 实际项目结构

```
E:\MarssPython\2511-daily-arXiv/
├── daily_arxiv/                # Scrapy 爬虫项目 (v1.0)
│   └── daily_arxiv/
│       ├── spiders/
│       │   └── arxiv.py       # arXiv 爬虫（从网页抓取论文）
│       ├── items.py           # 数据结构定义
│       ├── pipelines.py       # 数据处理管道
│       ├── settings.py        # Scrapy 配置
│       └── check_stats.py     # 统计检查
├── ai/                         # AI 增强模块 (v1.0)
│   ├── structure.py           # 结构化输出定义（Pydantic）
│   └── enhance.py             # LLM 摘要生成（LangChain）
├── to_md/                      # Markdown 转换 (v1.0)
│   └── convert.py             # JSONL → Markdown 转换
├── src/                        # 🆕 v2.0 母题筛选功能模块
│   ├── models.py              # ✅ 数据结构（Paper, FilteredPaper, SummarizedPaper）
│   ├── config.py              # ✅ 配置管理（.env + research_topics.txt）
│   ├── fetcher.py             # ✅ 基于 feedparser 的轻量级爬取（可选）
│   ├── filter.py              # ⏳ 母题筛选（核心新功能，未实现）
│   ├── summarizer.py          # ⏳ 可能不需要（已有 ai/enhance.py）
│   └── formatter.py           # ⏳ 可能不需要（已有 to_md/convert.py）
├── config/                     # 配置文件
│   └── research_topics.txt    # 🆕 研究母题列表（v2.0 使用）
├── output/                     # 输出结果
│   └── archive/               # 历史归档（.jsonl 和 .md 文件）
├── data/                       # 发布的 Markdown 文件（GitHub Pages）
├── main.py                     # ⏳ 主程序（框架，待实现 v2.0 集成）
├── update_readme.py            # README 自动生成
├── pyproject.toml             # 项目配置和依赖
├── CLAUDE.md                  # 本文件（项目文档，给 AI 和开发者）
├── README.md                  # 用户说明（自动生成）
└── .github/workflows/         # GitHub Actions 配置
```

**说明**：
- ✅ = 已实现
- ⏳ = 计划中/部分实现
- 🆕 = v2.0 新增功能

**架构演进：**
- **v1.0（当前）**：Scrapy 爬虫 → AI 增强（所有论文） → Markdown 转换 → GitHub Pages
- **v2.0（升级）**：Scrapy 爬虫 → **母题筛选（src/filter.py）** → AI 增强（仅相关论文） → Markdown 转换 → GitHub Pages

**设计原则：**
- 向后兼容：v2.0 不破坏 v1.0 的功能
- 模块化：母题筛选作为可选插件，不影响现有流程
- 成本优化：筛选后再调用 LLM，降低 80% 成本
- 个性化：每个用户配置自己的 research_topics.txt

---

## 核心工作流

### v1.0 工作流（当前版本）

```
1. Scrapy 爬虫 [daily_arxiv/]
   ├── 访问 https://arxiv.org/list/{category}/new
   ├── 解析 HTML 提取论文信息
   ├── 字段：id, title, authors, categories, summary, abs (URL)
   └── 输出：output/{date}.jsonl（原始数据）

   示例：
   CATEGORIES="cs.CV, cs.CL, cs.AI" scrapy crawl arxiv -o output/2025-11-08.jsonl

2. AI 增强 [ai/enhance.py]
   ├── 读取 JSONL 文件
   ├── 去重（基于 arXiv ID）
   ├── 对**所有论文**使用 LangChain + DeepSeek 生成结构化摘要：
   │   - tldr: Too Long; Didn't Read 摘要
   │   - motivation: 论文动机
   │   - method: 方法描述
   │   - result: 实验结果
   │   - conclusion: 结论
   ├── 并发处理（ThreadPoolExecutor）
   ├── 敏感词检查（调用外部 API）
   └── 输出：output/{date}_AI_enhanced_{language}.jsonl

   示例：
   LANGUAGE="Chinese" MODEL_NAME="deepseek-chat" \
   python ai/enhance.py --data output/2025-11-08.jsonl --max_workers 10

3. Markdown 转换 [to_md/convert.py]
   ├── 读取增强后的 JSONL
   ├── 按类别分组（cs.CV, cs.CL 等）
   ├── 使用 paper_template.md 模板格式化
   ├── 生成目录（Table of Contents）
   └── 输出：output/{date}.md

   示例：
   CATEGORIES="cs.CV, cs.CL" python to_md/convert.py \
   --data output/2025-11-08_AI_enhanced_Chinese.jsonl

4. README 更新 [update_readme.py]
   ├── 扫描 data/ 目录中的所有 .md 文件
   ├── 按日期排序
   ├── 使用 template.md 和 readme_content_template.md 生成
   └── 输出：README.md（主页索引）

5. GitHub Actions 自动化
   ├── 每日定时运行（cron）
   ├── 执行上述步骤 1-4
   ├── 将生成的 .md 文件移动到 data/ 目录
   ├── Git commit + push
   └── GitHub Pages 自动发布
```

**v1.0 的问题**：
- 对所有论文生成摘要，成本较高
- 用户需要手动浏览大量论文
- 没有个性化筛选功能

---

### v2.0 工作流（升级版，计划中）

```
1. Scrapy 爬虫 [daily_arxiv/]
   （与 v1.0 相同）
   └── 输出：output/{date}.jsonl（原始数据）

2. 🆕 母题筛选 [src/filter.py]
   ├── 读取 JSONL 文件
   ├── 加载 config/research_topics.txt（用户配置的研究母题）
   ├── 对每篇论文使用 LLM 判断：是否匹配任一研究母题
   ├── Prompt 设计：
   │   "论文标题：{title}
   │    论文摘要：{abstract}
   │    用户研究母题：{topics}
   │    判断：这篇论文是否直接解决上述任一母题？
   │    只回答：是/否 + 匹配的母题编号 + 匹配原因"
   ├── 筛选逻辑：
   │   - 使用轻量级 LLM 调用（成本低）
   │   - 只需判断"相关"或"不相关"
   │   - 保留 matched_topics 和 match_reason
   └── 输出：output/{date}_filtered.jsonl（仅包含相关论文）

   示例：
   python src/filter.py --data output/2025-11-08.jsonl \
                        --topics config/research_topics.txt \
                        --output output/2025-11-08_filtered.jsonl

3. AI 增强 [ai/enhance.py]
   ├── 读取筛选后的 JSONL（仅相关论文）
   ├── 生成结构化摘要（与 v1.0 相同）
   └── 输出：output/{date}_AI_enhanced_{language}.jsonl

   ⚠️ 成本对比：
   - v1.0：100 篇论文 × 摘要成本 = ¥0.2
   - v2.0：20 篇相关论文 × (筛选成本 + 摘要成本) ≈ ¥0.05
   - 节省 75%！

4-5. Markdown 转换 + GitHub Actions
   （与 v1.0 相同）
```

**v2.0 的优势**：
- ✅ **成本降低 75-80%**：只对相关论文生成摘要
- ✅ **零漏报**：LLM 语义理解，不会遗漏相关论文
- ✅ **80% 降噪**：过滤掉不相关论文
- ✅ **个性化**：每个用户配置自己的研究母题

---

### v2.0 核心模块：filter.py 设计

```python
# src/filter.py（待实现）

from typing import List
from openai import OpenAI
from .models import Paper, FilteredPaper
from .config import Config

def filter_papers_by_topics(
    papers: List[Paper],
    topics: List[str],
    llm_client: OpenAI
) -> List[FilteredPaper]:
    """
    使用 LLM 根据研究母题筛选论文

    Args:
        papers: 原始论文列表（来自 Scrapy）
        topics: 研究母题列表（来自 research_topics.txt）
        llm_client: OpenAI 兼容 API 客户端

    Returns:
        筛选后的论文列表（包含匹配原因）
    """
    filtered = []

    for paper in papers:
        # 构建 prompt
        prompt = _build_filter_prompt(paper, topics)

        # 调用 LLM 判断
        response = llm_client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,  # 确保结果稳定
        )

        # 解析结果
        result = _parse_filter_response(response.choices[0].message.content)

        if result["is_matched"]:
            filtered_paper = FilteredPaper(
                **paper.__dict__,
                matched_topics=result["matched_topics"],
                match_reason=result["match_reason"],
                filter_tokens=response.usage.total_tokens
            )
            filtered.append(filtered_paper)

    return filtered

def _build_filter_prompt(paper: Paper, topics: List[str]) -> str:
    """构建母题筛选的 Prompt"""
    topics_str = "\n".join([f"{i+1}. {t}" for i, t in enumerate(topics)])

    return f"""你是一个学术论文筛选助手。请判断以下论文是否与用户的研究母题相关。

论文标题：{paper.title}

论文摘要：
{paper.abstract}

用户研究母题：
{topics_str}

请回答：
1. 这篇论文是否直接解决上述任一母题？（是/否）
2. 如果是，匹配哪个/哪些母题？（编号）
3. 匹配原因（一句话）

格式：
是/否
匹配母题：[编号列表]
原因：[一句话说明]
"""
```

---

## 数据结构设计

### 生产方案数据结构

#### 1. Scrapy 输出（JSONL）

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

#### 2. AI 增强输出（JSONL）

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

#### 3. Structure 定义（Pydantic）

```python
# ai/structure.py
class Structure(BaseModel):
    tldr: str = Field(description="generate a too long; didn't read summary")
    motivation: str = Field(description="describe the motivation in this paper")
    method: str = Field(description="method of this paper")
    result: str = Field(description="result of this paper")
    conclusion: str = Field(description="conclusion of this paper")
```

### v2.0 数据结构（升级）

#### 数据流演进

```
v1.0：Scrapy JSONL → AI Enhanced JSONL → Markdown

v2.0：Scrapy JSONL → 🆕 Filtered JSONL → AI Enhanced JSONL → Markdown
```

#### 🆕 Filtered JSONL（母题筛选后）

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

#### Python 数据模型（src/models.py）

```python
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

**设计说明**：
- v2.0 的数据结构**继承自 v1.0**，向后兼容
- 在 Scrapy 输出和 AI 增强之间插入"筛选"步骤
- FilteredPaper 只是在原始数据基础上增加筛选元数据

---

## 核心模块设计

### v1.0 核心模块（已实现）

#### 1. Scrapy 爬虫 (daily_arxiv/spiders/arxiv.py)

```python
class ArxivSpider(scrapy.Spider):
    name = "arxiv"

    def __init__(self):
        # 从环境变量读取类别配置
        categories = os.environ.get("CATEGORIES", "cs.CV").split(",")
        self.target_categories = set(map(str.strip, categories))
        self.start_urls = [
            f"https://arxiv.org/list/{cat}/new"
            for cat in self.target_categories
        ]

    def parse(self, response):
        # 解析 HTML，提取论文信息
        # 字段：id, title, authors, categories, summary, abs
        pass
```

#### 2. AI 增强 (ai/enhance.py)

```python
def process_single_item(chain, item: Dict, language: str) -> Dict:
    """
    处理单个论文，生成结构化摘要

    Args:
        chain: LangChain chain (prompt + LLM + structured output)
        item: 论文数据（JSONL 格式）
        language: 摘要语言（Chinese/English）

    Returns:
        增强后的论文数据（包含 AI 字段）
    """
    # 敏感词检查
    if is_sensitive(item.get("summary", "")):
        return None

    # 调用 LLM
    response: Structure = chain.invoke({
        "language": language,
        "content": item['summary']
    })
    item['AI'] = response.model_dump()
    return item

def process_all_items(data: List[Dict], model_name: str,
                     language: str, max_workers: int) -> List[Dict]:
    """
    并发处理所有论文

    使用 ThreadPoolExecutor 并发调用 LLM
    """
    pass
```

#### 3. Markdown 转换 (to_md/convert.py)

```python
def convert_to_markdown(jsonl_file: str, categories: list[str]) -> str:
    """
    将 JSONL 转换为 Markdown

    Args:
        jsonl_file: AI 增强后的 JSONL 文件
        categories: 类别列表（用于排序和分组）

    Returns:
        Markdown 内容
    """
    # 1. 读取 JSONL
    # 2. 按类别分组
    # 3. 使用 paper_template.md 格式化
    # 4. 生成目录
    pass
```

### v2.0 核心模块（src/，升级功能）

#### 🆕 filter.py - 母题筛选（核心新功能）⏳ 待实现

**功能**：在 Scrapy 爬虫和 AI 增强之间插入筛选步骤

```python
# src/filter.py

def filter_papers_by_topics(
    papers: list[Paper],
    topics: list[str],
    llm_client: OpenAI
) -> list[FilteredPaper]:
    """
    使用 LLM 根据研究母题筛选论文

    Args:
        papers: 原始论文列表（来自 Scrapy JSONL）
        topics: 研究母题列表（来自 research_topics.txt）
        llm_client: OpenAI 兼容 API 客户端

    Returns:
        筛选后的论文列表
    """
    filtered = []

    for paper in papers:
        # 构建提示词
        prompt = _build_filter_prompt(paper, topics)

        # 调用 LLM 判断
        response = llm_client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0  # 确保结果稳定
        )

        # 解析结果
        result = _parse_filter_response(response.choices[0].message.content)

        if result["is_matched"]:
            filtered_paper = FilteredPaper(
                **paper.__dict__,
                matched_topics=result["matched_topics"],
                match_reason=result["match_reason"],
                filter_tokens=response.usage.total_tokens
            )
            filtered.append(filtered_paper)

    return filtered
```

**集成方式**：
```bash
# v2.0 工作流
1. scrapy crawl arxiv -o output/2025-11-08.jsonl
2. python src/filter.py --data output/2025-11-08.jsonl \
                        --output output/2025-11-08_filtered.jsonl  # 新增步骤
3. python ai/enhance.py --data output/2025-11-08_filtered.jsonl \  # 修改：读取筛选后的数据
                        --max_workers 10
4. python to_md/convert.py --data output/2025-11-08_AI_enhanced_Chinese.jsonl
```

#### fetcher.py - 可选的轻量级爬取 ✅ 已实现

```python
def fetch_arxiv_papers(categories: list[str], max_results: int = 50) -> List[Paper]:
    """
    从 arXiv API 获取指定类别的论文（可选方案）

    使用 feedparser 解析 RSS/Atom feed
    实现位置：src/fetcher.py:10-101

    注：v2.0 主要还是使用 Scrapy，这个是可选的轻量级方案
    """
    pass
```

#### summarizer.py 和 formatter.py - 可能不需要

- **summarizer.py**：已有 ai/enhance.py，无需重复实现
- **formatter.py**：已有 to_md/convert.py，无需重复实现
- **v2.0 重点**：只需实现 filter.py，其余模块复用现有代码

---

## 开发约定

### 1. **实用主义：Production-Ready 优先**
- 生产方案：已实现完整的自动化流程（Scrapy + LangChain + GitHub Actions）
- 简化方案：为更轻量、可定制的场景设计（基于 feedparser 和母题筛选）
- 代码可读性优先：清晰的函数命名、完善的错误处理

### 2. **模块化设计**
- 每个模块职责单一：爬虫、AI 增强、格式转换各司其职
- 数据格式统一：JSONL 作为中间格式
- 配置外置：所有配置通过环境变量或配置文件管理

### 3. **向后兼容**
- 数据结构设计为"只增不改"
- JSONL 格式向后兼容
- API 接口保持稳定

### 4. **错误处理与容错**
- LLM 调用失败：提供默认值，避免中断整个流程
- 敏感词检查：自动过滤不合规内容
- 并发控制：使用 ThreadPoolExecutor 提高效率
- 日志记录：stderr 输出详细的错误信息

### 5. **成本控制**
- 使用 DeepSeek API（成本约 ¥0.2/天）
- 并发控制：通过 max_workers 参数限制并发数
- 去重机制：避免重复处理相同论文

---

## 配置管理

### 生产方案配置

#### 环境变量（.env）

```bash
# OpenAI 兼容 API 配置
OPENAI_API_KEY=sk-xxxxxxxx
OPENAI_BASE_URL=https://api.deepseek.com
MODEL_NAME=deepseek-chat

# arXiv 类别配置（逗号分隔）
CATEGORIES=cs.CV, cs.CL, cs.AI, cs.GR

# AI 增强配置
LANGUAGE=Chinese  # 或 English
MAX_WORKERS=10    # 并发数

# GitHub 配置（用于 GitHub Actions）
EMAIL=your-email@example.com
NAME=Your Name
```

#### GitHub Actions Secrets & Variables

在 GitHub 仓库设置中配置：

**Secrets**（加密）：
- `OPENAI_API_KEY`: API 密钥
- `OPENAI_BASE_URL`: API 基础 URL
- `ACCESS_PASSWORD`（可选）：页面访问密码

**Variables**（明文）：
- `CATEGORIES`: arXiv 类别
- `LANGUAGE`: 摘要语言
- `MODEL_NAME`: 模型名称
- `EMAIL`: Git 提交邮箱
- `NAME`: Git 提交用户名

### 简化方案配置

#### .env 文件

```bash
# OpenAI API 配置（或兼容的 API，如 DeepSeek）
OPENAI_API_KEY=sk-xxxxxxxx
OPENAI_BASE_URL=https://api.deepseek.com
MODEL_NAME=deepseek-chat

# arXiv 配置
ARXIV_CATEGORIES=cs.CV,cs.CL,cs.AI,cs.LG
MAX_PAPERS_PER_CATEGORY=50

# 输出配置
OUTPUT_DIR=output
OUTPUT_LANGUAGE=zh  # zh（中文）或 en（英文）
```

#### research_topics.txt 文件

```
# 研究母题配置文件
# 每行一个母题，支持中英文混合
# 空行和 # 开头的行会被忽略

# AI Agent 相关
AI Agent 的工具调用优化
AI Agent 的规划能力提升

# 视频理解相关
长视频理解的效率问题
视频生成的质量提升

# RAG 相关
RAG 中的知识图谱应用
RAG 的检索效率优化

# 可解释性相关
Sparse Autoencoder 在可解释性中的应用
神经网络的机制可解释性
```

**格式要求**：
- 每行一个母题
- 支持中英文混合
- 空行和 `#` 开头的行会被忽略
- 当前未在生产方案中使用，为简化方案预留

---

## 验收标准

### ✅ 生产方案（已实现）
- [x] 能成功爬取指定类别的 arXiv 论文（每日最新论文）
- [x] AI 生成的结构化摘要质量高（TLDR、动机、方法、结果、结论）
- [x] 输出格式：Markdown，支持目录和分类浏览
- [x] GitHub Actions 自动化：每日定时运行
- [x] GitHub Pages 发布：零服务器成本
- [x] 成本控制：约 ¥0.2/天

### ⏳ 简化方案（计划中）
- [ ] 能成功使用 feedparser 爬取论文
- [ ] 母题筛选功能实现（filter.py）
- [ ] 摘要生成功能实现（summarizer.py）
- [ ] 输出格式化功能实现（formatter.py）
- [ ] 运行时间 < 5 分钟（100 篇论文）
- [ ] 配置简单：只需修改 `research_topics.txt` 和 `.env`

---

## 性能特点

### 已实现的优化

1. **并发处理**：
   - 使用 `ThreadPoolExecutor` 并发调用 LLM
   - 可通过 `--max_workers` 参数调整并发数

2. **错误容错**：
   - LLM 调用失败时提供默认值
   - 敏感词自动过滤
   - 详细的错误日志

3. **成本控制**：
   - 使用 DeepSeek API（成本极低）
   - 去重机制避免重复处理
   - 并发数可控

4. **数据持久化**：
   - JSONL 中间格式，便于调试和复用
   - 历史数据归档到 output/archive/

### 未来优化方向

1. **缓存机制**：已处理的论文缓存，避免重复调用 LLM
2. **增量更新**：只处理新增论文
3. **成本统计**：实时显示 token 消耗和成本

---

## 未来扩展

### 生产方案扩展
1. **多语言支持**：支持更多摘要语言
2. **更多类别**：支持更多 arXiv 类别
3. **智能推荐**：基于用户兴趣的个性化推荐
4. **邮件订阅**：每日摘要邮件推送

### 简化方案扩展
1. **母题筛选**：实现基于研究母题的智能筛选
2. **本地运行**：无需 GitHub Actions，本地定时运行
3. **自定义提示词**：支持用户自定义 LLM 提示词
4. **知识图谱集成**：与 Obsidian 等工具集成

### 扩展原则
- ✅ **要**：保持两套方案的独立性和兼容性
- ✅ **要**：每次只加一个功能，充分测试
- ❌ **不要**：破坏现有功能的稳定性

---

## 测试策略

### 当前测试方法

1. **手动测试**：
   - 运行完整流程，检查输出质量
   - 验证 GitHub Pages 发布效果

2. **错误处理测试**：
   - 测试 API 失败场景
   - 测试敏感词过滤功能

### 未来测试计划

```python
# tests/test_fetcher.py
def test_fetch_arxiv_papers():
    """测试 feedparser 爬取功能"""
    pass

# tests/test_filter.py
def test_filter_papers_by_topics():
    """测试母题筛选功能"""
    pass

# tests/test_integration.py
def test_full_pipeline():
    """测试完整流程"""
    pass
```

---

## 使用指南

### 🚀 快速开始（本地运行 v1.0）

#### 1. 环境准备

```bash
# 克隆仓库
git clone <your-repo-url>
cd 2511-daily-arXiv

# 使用 uv 安装依赖（推荐）
uv sync

# 激活虚拟环境
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Windows (CMD)
.venv\Scripts\activate.bat
# Git Bash / Linux / macOS
source .venv/bin/activate
```

**为什么选择 uv？**
- ⚡ **快速**：比 pip 快 10-100 倍
- 🔒 **可靠**：自动创建和管理虚拟环境
- 📦 **现代**：支持 pyproject.toml，无需 requirements.txt
- 🎯 **精确**：使用 uv.lock 确保依赖版本一致

#### 2. 配置环境变量

```bash
# 创建 .env 文件（基于示例）
cp config/.env.example config/.env

# 编辑 config/.env，填入你的 API 密钥
# OPENAI_API_KEY=sk-xxxxxxxx
# OPENAI_BASE_URL=https://api.deepseek.com
# MODEL_NAME=deepseek-chat
```

或者直接设置环境变量：

```bash
# Windows (PowerShell)
$env:OPENAI_API_KEY="sk-xxxxxxxx"
$env:OPENAI_BASE_URL="https://api.deepseek.com"
$env:CATEGORIES="cs.CV, cs.CL, cs.AI"
$env:LANGUAGE="Chinese"
$env:MODEL_NAME="deepseek-chat"

# Git Bash / Linux / macOS
export OPENAI_API_KEY="sk-xxxxxxxx"
export OPENAI_BASE_URL="https://api.deepseek.com"
export CATEGORIES="cs.CV, cs.CL, cs.AI"
export LANGUAGE="Chinese"
export MODEL_NAME="deepseek-chat"
```

#### 3. 运行完整流程（v1.0）

**方式一：使用 run.sh 脚本（推荐）**

```bash
# 需要 Git Bash 或 WSL（Windows 上）
bash run.sh
```

**方式二：手动执行各步骤**

```bash
# 获取今天的日期
$today = (Get-Date).ToString("yyyy-MM-dd")  # PowerShell
# 或
today=$(date -u "+%Y-%m-%d")  # Git Bash

# 步骤 1：爬取论文
cd daily_arxiv
scrapy crawl arxiv -o "../data/${today}.jsonl"
cd ..

# 步骤 2：AI 增强（生成摘要）
cd ai
python enhance.py --data "../data/${today}.jsonl" --max_workers 10
cd ..

# 步骤 3：转换为 Markdown
cd to_md
python convert.py --data "../data/${today}_AI_enhanced_Chinese.jsonl"
cd ..

# 步骤 4：更新 README（可选）
python update_readme.py
```

#### 4. 查看结果

生成的文件在 `data/` 目录：
- `{date}.jsonl` - 原始爬取数据
- `{date}_AI_enhanced_Chinese.jsonl` - AI 增强后的数据
- `{date}.md` - 最终的 Markdown 文档

### 生产方案使用（GitHub Actions 自动化）

详见 [README.md](README.md)，主要步骤：
1. Fork 本仓库
2. 配置 GitHub Secrets 和 Variables
3. 启用 GitHub Actions
4. 配置 GitHub Pages
5. 访问 `https://<username>.github.io/daily-arXiv-ai-enhanced/`

### v2.0 简化方案使用（开发中）

```bash
# 1. 配置环境变量
cp config/.env.example config/.env
# 编辑 config/.env，填入 API 密钥

# 2. 配置研究母题
# 编辑 config/research_topics.txt

# 3. 运行（待实现）
python main.py
```

---

## 相关资源

- **原项目**：[dw-dengwei/daily-arXiv-ai-enhanced](https://github.com/dw-dengwei/daily-arXiv-ai-enhanced)
- **README.md**：用户使用指南
- **pyproject.toml**：项目依赖和配置

---

## 总结

这是一个**实用主义 + Production-Ready** 的 AI 工具：

### 生产方案
- **核心价值**：零基础设施，完全自动化的 arXiv 论文摘要生成
- **技术栈**：Scrapy + LangChain + GitHub Actions + Pages
- **成本**：约 ¥0.2/天，完全免费部署

### 简化方案（计划中）
- **核心价值**：轻量级、可定制的母题筛选工具
- **技术栈**：feedparser + 简单 LLM 调用
- **特点**：本地运行，灵活配置

**两套方案并存，满足不同场景需求。**
