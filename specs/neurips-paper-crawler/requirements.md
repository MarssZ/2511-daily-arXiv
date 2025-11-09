# 需求文档：NeurIPS 会议论文爬取与增强

## 介绍

### 背景
当前系统已实现 arXiv 论文的自动爬取、AI 增强摘要生成和 GitHub Pages 发布。用户需要将 NeurIPS 等顶级会议论文纳入论文库，但手工处理耗时数十天（需逐篇复制到大模型提取信息），严重影响效率。

### 目标
扩展现有爬虫系统，支持 NeurIPS 会议论文的自动爬取，复用现有 AI 增强流程，实现会议论文的批量处理。

### 范围
- **包含**：NeurIPS 2024 Oral 论文爬取、数据标准化、AI 增强、独立发布
- **不包含**：Poster/Workshop 论文、历史年份（2023及以前）、领域过滤、PDF 全文下载
- **未来扩展**：Spotlight 论文、PDF 全文分析（3个月内）

---

## 需求

### 需求 1：爬取 NeurIPS 2024 Oral 论文基本信息

**用户故事：** 作为研究人员，我希望自动爬取 NeurIPS 2024 Oral 论文的基本信息，以便批量处理而不是手动复制粘贴。

#### 验收标准

1. WHEN 用户运行 NeurIPS 爬虫命令 THEN 系统 SHALL 从 `https://neurips.cc/virtual/2024/events/oral` 爬取所有 Oral 论文
2. FOR EACH 论文条目，系统 SHALL 提取以下字段：
   - 论文标题（title）
   - 作者列表（authors）
   - 摘要文本（summary）
   - 详情页链接（abs）
3. 系统 SHALL 为每篇论文生成唯一标识符，格式为 `neurips2024_oral_{id}`
4. IF 某篇论文缺少必需字段（标题或摘要）THEN 系统 SHALL 记录警告并跳过该论文
5. 爬取过程 SHALL 遵循礼貌爬取原则，请求间隔不少于 1 秒

---

### 需求 2：获取 OpenReview 论文链接

**用户故事：** 作为研究人员，我希望保留论文的 OpenReview 链接和 PDF 下载地址，以便未来进行全文分析。

#### 验收标准

1. FOR EACH 论文详情页 `https://neurips.cc/virtual/2024/oral/{id}`，系统 SHALL 提取 OpenReview 论坛链接
2. IF OpenReview 链接存在，系统 SHALL 生成对应的 PDF 链接，格式为 `https://openreview.net/pdf?id={openreview_id}`
3. IF OpenReview 链接不存在，系统 SHALL 将 PDF 字段设为空字符串
4. 系统 SHALL 将详情页链接存储在 `abs` 字段
5. WHEN 爬取详情页失败 THEN 系统 SHALL 记录错误并继续处理下一篇论文

---

### 需求 3：输出标准化 JSONL 格式

**用户故事：** 作为系统维护者，我希望 NeurIPS 论文数据与 arXiv 论文格式一致，以便复用现有的 AI 增强流程。

#### 验收标准

1. 系统 SHALL 输出 JSONL 格式文件，每行一个 JSON 对象
2. EACH JSON 对象 SHALL 包含以下字段：
   ```json
   {
     "id": "neurips2024_oral_{id}",
     "title": "论文标题",
     "authors": ["作者1", "作者2"],
     "summary": "摘要文本",
     "abs": "https://neurips.cc/virtual/2024/oral/{id}",
     "pdf": "https://openreview.net/pdf?id={openreview_id}",
     "categories": ["NeurIPS 2024 Oral"],
     "comment": null,
     "source": "neurips"
   }
   ```
3. 字段类型 SHALL 与 arXiv 输出保持一致：
   - `authors`: 字符串数组
   - `categories`: 字符串数组
   - `comment`: null 或字符串
4. 输出文件命名格式 SHALL 为 `neurips-2024-oral.jsonl`
5. IF 输出文件已存在 THEN 系统 SHALL 覆盖（默认行为）或提示用户（可选）

---

### 需求 4：与现有 AI 增强流程集成

**用户故事：** 作为用户，我希望 NeurIPS 论文能走相同的 AI 增强流程，以便生成结构化摘要。

#### 验收标准

1. NeurIPS 爬取输出的 JSONL 文件 SHALL 可被 `ai/enhance.py` 直接处理
2. AI 增强脚本 SHALL 正确识别 `source: "neurips"` 字段但不改变处理逻辑
3. WHEN 运行 AI 增强 THEN 系统 SHALL 生成 `neurips-2024-oral_AI_enhanced_Chinese.jsonl`
4. 增强后的数据 SHALL 包含现有的 5 个结构化字段：
   - TLDR
   - Motivation
   - Method
   - Result
   - Conclusion
5. IF AI 增强失败（如 API 错误）THEN 系统 SHALL 保留原始数据并记录错误

---

### 需求 5：独立的 Markdown 输出与发布

**用户故事：** 作为读者，我希望在 GitHub Pages 上通过独立 Tab 浏览 NeurIPS 论文，以便与 arXiv 论文区分。

#### 验收标准

1. 系统 SHALL 生成独立的 Markdown 文件 `data/neurips-2024-oral.md`
2. Markdown 文件 SHALL 包含元数据，标识为 NeurIPS 来源：
   ```yaml
   ---
   title: NeurIPS 2024 Oral Papers
   source: neurips
   year: 2024
   category: oral
   ---
   ```
3. WHEN 更新 README.md THEN 系统 SHALL 添加 NeurIPS 论文的导航链接
4. GitHub Pages 发布后 SHALL 支持按来源（arXiv / NeurIPS）筛选论文
5. NeurIPS 论文列表 SHALL 与 arXiv 论文列表使用相同的展示格式

---

### 需求 6：独立的爬虫命令与配置

**用户故事：** 作为系统维护者，我希望 NeurIPS 爬虫与 arXiv 爬虫独立运行，互不干扰。

#### 验收标准

1. 系统 SHALL 提供独立的 Scrapy 爬虫 `neurips`
2. 用户 SHALL 通过以下命令运行爬虫：
   ```bash
   scrapy crawl neurips -o neurips-2024-oral.jsonl
   ```
3. NeurIPS 爬虫 SHALL 不依赖 `CATEGORIES` 环境变量（arXiv 专用）
4. NeurIPS 爬虫 SHALL 支持年份和类别参数（未来扩展）：
   ```bash
   scrapy crawl neurips -a year=2024 -a category=oral
   ```
5. WHEN 同时运行 arXiv 和 NeurIPS 爬虫 THEN 两者 SHALL 不产生冲突

---

### 需求 7：错误处理与日志

**用户故事：** 作为系统维护者，我希望在爬取失败时能快速定位问题，而不是静默失败。

#### 验收标准

1. WHEN 网络请求失败 THEN 系统 SHALL 记录错误日志并重试最多 3 次
2. WHEN 论文页面结构变化导致解析失败 THEN 系统 SHALL 记录警告并继续处理下一篇
3. 系统 SHALL 在爬取结束时输出统计信息：
   - 总论文数
   - 成功爬取数
   - 失败数（含原因）
4. IF 超过 50% 论文爬取失败 THEN 系统 SHALL 输出错误提示，建议检查网页结构
5. 所有日志 SHALL 使用 Scrapy 的标准日志系统

---

## 非功能性需求

### 性能
- 爬取 60 篇 Oral 论文（估计数量）SHALL 在 5 分钟内完成
- 单篇论文爬取时间 SHALL 不超过 10 秒（含详情页请求）

### 可维护性
- NeurIPS 爬虫代码 SHALL 与 arXiv 爬虫保持独立，避免耦合
- Pipeline 设计 SHALL 支持未来添加其他会议（ICML、ICLR）

### 可扩展性
- 系统架构 SHALL 预留以下扩展点：
  - 支持 Spotlight 论文类别（3个月内）
  - 支持 PDF 全文下载与分析（3个月内）
  - 支持历史年份（按需）

---

## 验收测试场景

### 场景 1：首次爬取 NeurIPS 2024 Oral
1. 运行 `scrapy crawl neurips -o neurips-2024-oral.jsonl`
2. 验证生成的 JSONL 文件包含所有 Oral 论文
3. 运行 AI 增强脚本
4. 验证生成的 Markdown 文件可在 GitHub Pages 正常显示

### 场景 2：与 arXiv 爬虫并行
1. 同时运行 `scrapy crawl arxiv` 和 `scrapy crawl neurips`
2. 验证两个爬虫互不干扰
3. 验证输出文件正确分离

### 场景 3：网络异常恢复
1. 模拟网络间歇性故障
2. 验证爬虫自动重试
3. 验证最终输出数据完整性

---

## 实现优先级

### P0（MVP 核心功能）
- ✅ 需求 1：爬取基本信息
- ✅ 需求 2：获取 OpenReview 链接
- ✅ 需求 3：标准化输出
- ✅ 需求 6：独立爬虫命令

### P1（AI 集成）
- ✅ 需求 4：AI 增强流程集成
- ✅ 需求 5：Markdown 输出

### P2（可靠性）
- ✅ 需求 7：错误处理

### P3（未来扩展，3个月内）
- ⏳ Spotlight 论文支持
- ⏳ PDF 全文下载与分析

---

## 技术约束

1. 必须使用 Scrapy 框架（与现有系统一致）
2. 必须输出 JSONL 格式（与 arXiv 一致）
3. 不得修改现有 arXiv 爬虫代码（零破坏性）
4. Pipeline 设计应支持多数据源（arXiv, NeurIPS, 未来的 ICML/ICLR）

---

## 术语表

- **Oral**：NeurIPS 会议的口头报告论文，通常为录用论文中的 Top 1-2%
- **Spotlight**：NeurIPS 会议的重点论文，介于 Oral 和 Poster 之间
- **OpenReview**：学术论文开放评审平台，NeurIPS 论文发布在此
- **JSONL**：每行一个 JSON 对象的文本格式
- **AI 增强**：使用 LLM 生成论文的结构化摘要（TLDR/Motivation/Method/Result/Conclusion）
