# v2.0 设计：母题筛选功能

> **导航**: [← 返回主文档](../CLAUDE.md) | [数据结构](data-structures.md) | [核心工作流](workflows.md) | [AI 模块](../ai/README.md)

> **状态：** 计划中，未实现

## 核心思想

在爬虫和 AI 增强之间插入**母题筛选**步骤，只对相关论文生成摘要。

```
v1.0: 爬虫 → AI 增强（所有论文） → Markdown

v2.0: 爬虫 → 母题筛选 → AI 增强（仅相关论文） → Markdown
              ↑
        config/research_topics.txt
```

## 价值主张

- ✅ **成本降低 75-80%** - 只处理相关论文
- ✅ **零漏报** - LLM 语义理解，不遗漏相关内容
- ✅ **个性化** - 每个用户配置自己的研究母题
- ✅ **高效** - 减少阅读负担

## 工作流

1. **爬虫抓取** → `data/{date}.jsonl`（100篇论文）
2. **母题筛选** → `data/{date}_filtered.jsonl`（20篇相关论文）
3. **AI 增强** → `data/{date}_AI_enhanced.jsonl`（仅20篇）
4. **Markdown** → `data/{date}.md`

## 核心模块：src/filter.py

### 功能设计

```python
def filter_papers_by_topics(
    papers: list[Paper],
    topics: list[str],
    llm_client: OpenAI
) -> list[FilteredPaper]:
    """使用 LLM 根据研究母题筛选论文"""

    for paper in papers:
        prompt = build_filter_prompt(paper, topics)
        result = llm_client.chat.completions.create(
            model="qwen-turbo",  # 使用轻量级模型
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )

        if is_matched(result):
            yield FilteredPaper(
                **paper.__dict__,
                matched_topics=...,
                match_reason=...,
                filter_tokens=...
            )
```

### Prompt 设计

```
你是一个学术论文筛选助手。

论文标题：{title}
论文摘要：{abstract}

用户研究母题：
1. AI Agent 的工具调用优化
2. 视频生成的质量提升
3. ...

判断：这篇论文是否直接解决上述任一母题？

回答格式：
是/否
匹配母题：[编号]
原因：[一句话]
```

## 配置文件

### research_topics.txt

```
# 研究母题配置
# 每行一个母题

AI Agent 的工具调用优化
AI Agent 的规划能力提升
长视频理解的效率问题
RAG 中的知识图谱应用
```

## 成本对比

| 方案 | 论文数 | 筛选成本 | 摘要成本 | 总成本 |
|------|--------|----------|----------|---------|
| v1.0 | 100篇  | ¥0       | ¥0.20    | **¥0.20** |
| v2.0 | 100篇  | ¥0.02    | ¥0.04    | **¥0.06** |

**节省：70%**

## 实现计划

- [ ] 实现 `src/filter.py`
- [ ] 设计 filter prompt
- [ ] 集成到 main.py
- [ ] 测试筛选准确率
- [ ] 优化成本

## 相关文档

- [数据结构](data-structures.md) - FilteredPaper 定义
- [工作流](workflows.md) - v1.0 当前实现
