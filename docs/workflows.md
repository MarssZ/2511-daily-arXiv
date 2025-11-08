# 核心工作流

> **导航**: [← 返回主文档](../CLAUDE.md) | [数据结构](data-structures.md) | [v2.0 设计](v2-design.md) | [AI 模块](../ai/README.md)

本文档详细说明项目的数据处理流程。

## v1.0 工作流（当前版本）

```
爬虫 → AI 增强 → Markdown 转换 → GitHub Pages
```

### 步骤详解

#### 1. Scrapy 爬虫（`daily_arxiv/`）

**功能：** 从 arXiv 网站抓取最新论文

**流程：**
1. 访问 `https://arxiv.org/list/{category}/new`
2. 解析 HTML 提取论文信息
3. 调用 arXiv API 获取详细信息
4. 输出到 `data/{date}.jsonl`

**使用示例：**
```bash
cd daily_arxiv
export CATEGORIES="cs.AI, cs.CL"
scrapy crawl arxiv -o "../data/$(date +%Y-%m-%d).jsonl"
cd ..
```

**输出字段：**
- `id`: arXiv ID
- `title`: 标题
- `authors`: 作者列表
- `categories`: 分类
- `summary`: 摘要
- `abs`: 论文链接

#### 2. AI 增强（`ai/enhance.py`）

**功能：** 使用 LLM 生成结构化中文摘要

**流程：**
1. 读取 JSONL 文件
2. 去重（基于 arXiv ID）
3. 并发调用 LLM（ThreadPoolExecutor）
4. 生成 5 个字段的摘要：
   - **TLDR**: 一句话总结
   - **动机**: 研究动机和背景
   - **方法**: 技术方案
   - **结果**: 实验结果
   - **结论**: 结论和未来工作
5. 敏感词检查
6. 输出到 `data/{date}_AI_enhanced_{language}.jsonl`

**使用示例：**
```bash
# 使用便捷脚本
.\run_ai_enhance.ps1

# 或手动运行
cd ai
python enhance.py --data ../data/2025-11-08.jsonl --max_workers 10
cd ..
```

**配置：**
- `OPENAI_API_KEY`: API 密钥
- `OPENAI_BASE_URL`: API 地址
- `MODEL_NAME`: 模型名称（如 qwen-plus）
- `LANGUAGE`: 输出语言（Chinese/English）
- `MAX_WORKERS`: 并发数

#### 3. Markdown 转换（`to_md/convert.py`）

**功能：** 将 JSONL 转换为可读的 Markdown 文档

**流程：**
1. 读取 AI 增强后的 JSONL
2. 按类别分组
3. 使用模板格式化
4. 生成目录（TOC）
5. 输出到 `data/{date}.md`

**使用示例：**
```bash
cd to_md
python convert.py --data ../data/2025-11-08_AI_enhanced_Chinese.jsonl
cd ..
```

#### 4. README 更新（`update_readme.py`）

**功能：** 生成主页索引

**流程：**
1. 扫描 `data/` 目录
2. 按日期排序
3. 生成链接列表
4. 更新 `README.md`

**使用示例：**
```bash
python update_readme.py
```

#### 5. GitHub Actions 自动化

**功能：** 每日自动运行全流程

**流程：**
1. 定时触发（cron）
2. 执行步骤 1-4
3. Git commit + push
4. GitHub Pages 自动发布

**配置位置：** `.github/workflows/run.yml`

## v1.0 的局限

- ❌ 对**所有论文**生成摘要，成本较高（约 ¥0.2/天）
- ❌ 用户需要手动浏览大量论文
- ❌ 没有个性化筛选

## 完整流程示例

```bash
# 1. 爬取今天的论文
cd daily_arxiv
export CATEGORIES="cs.AI"
scrapy crawl arxiv -o "../data/$(date +%Y-%m-%d).jsonl"
cd ..

# 2. AI 增强
.\run_ai_enhance.ps1

# 3. 转换为 Markdown
cd to_md
python convert.py --data "../data/$(date +%Y-%m-%d)_AI_enhanced_Chinese.jsonl"
cd ..

# 4. 更新索引
python update_readme.py

# 5. 查看结果
ls data/*.md | tail -1
```

## 性能指标

- **爬取速度**: ~3秒/篇（礼貌爬取）
- **AI 增强**: ~2-5秒/篇（取决于并发数）
- **总耗时**: ~5-10分钟（100篇论文）
- **成本**: ~¥0.2/天（使用阿里百炼 qwen-plus）

## 相关文档

- [数据结构](data-structures.md) - 了解各阶段的数据格式
- [v2.0 设计](v2-design.md) - 母题筛选功能（降低 80% 成本）
- [AI 模块](../ai/README.md) - AI 增强的详细配置
