# daily-arXiv: AI驱动的论文母题筛选器

一个基于研究母题（Research Topics）的 arXiv 论文自动筛选和摘要工具。

---

## 🎯 核心价值

**问题**：每天 arXiv 发布 100+ 篇论文，手动筛选耗时 30 分钟
**方案**：AI 根据你的研究母题自动筛选，只推送 20 篇高相关论文
**收益**：节省 80% 阅读时间 + 零漏报（LLM 理解语义，不仅是关键词匹配）

---

## 🚀 快速开始

### 1. 安装依赖

```bash
# 克隆或下载项目
cd E:\MarssPython\2511-daily-arXiv

# 安装依赖（使用 uv 或 pip）
uv pip install -e .
# 或
pip install -e .
```

### 2. 配置环境变量

创建 `.env` 文件：

```bash
# OpenAI API 配置（或兼容的 API，如 DeepSeek）
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.deepseek.com  # 可选，默认为 OpenAI

# arXiv 配置
ARXIV_CATEGORIES=cs.CV,cs.CL,cs.AI,cs.LG  # 要爬取的类别
```

### 3. 定义研究母题

编辑 `config/research_topics.txt`：

```
AI Agent 的工具调用优化
长视频理解的效率问题
RAG 中的知识图谱应用
多模态大模型的端侧部署
可解释性：Sparse Autoencoder
```

### 4. 运行

```bash
python main.py
```

输出示例：

```
📊 今日论文统计
├── 爬取论文: 127 篇
├── 母题筛选后: 23 篇
└── 成本: ¥0.09

✅ 已保存到 output/2024-01-15.md
```

---

## 📂 项目结构

```
E:\MarssPython\2511-daily-arXiv/
├── main.py                      # 主程序入口
├── src/                         # 源代码
│   ├── fetcher.py              # arXiv 论文爬取
│   ├── filter.py               # 母题筛选（LLM）
│   ├── summarizer.py           # 论文摘要（LLM）
│   └── config.py               # 配置管理
├── config/                      # 配置文件
│   ├── research_topics.txt     # 研究母题列表
│   └── .env                    # API 密钥（不纳入版本控制）
├── output/                      # 输出结果
│   ├── 2024-01-15.md           # 每日摘要
│   └── archive/                # 历史归档
├── specs/                       # 需求和设计文档
│   ├── requirements.md         # 需求文档
│   └── design.md               # 设计文档
├── tests/                       # 测试文件
├── pyproject.toml              # 项目配置
├── CLAUDE.md                   # 项目总览（给 AI 看）
└── README.md                   # 本文件（给用户看）
```

---

## 🎯 核心功能

### 1. 母题驱动筛选

**区别于关键词匹配**：
- ❌ 关键词：`"video understanding"` → 只匹配标题/摘要中有这两个词的论文
- ✅ 母题：`"长视频理解的效率问题"` → LLM 理解问题域，找到所有相关论文（即使用词不同）

**示例**：
```python
# 你的母题
"如何让深度学习模型更可解释"

# LLM 会筛选出：
✅ "Sparse Autoencoders for Interpretability"  # 直接相关
✅ "Mechanistic Interpretability via Circuit Discovery"  # 同义表述
✅ "Feature Visualization in Neural Networks"  # 问题域相关
❌ "Efficient Training of Large Models"  # 虽然有"模型"，但不相关
```

### 2. 低成本 AI 摘要

**成本优化**：
```
传统方案：100 篇 × 摘要 = ¥0.20/天
母题筛选：100 篇 × 判断 + 20 篇 × 摘要 = ¥0.09/天
节省：55%
```

### 3. 零漏报保证

**关键词方案的问题**：
- 论文标题：`"Attention Is All You Need"`
- 关键词 `"transformer"` → ❌ 漏报（标题中没有这个词）
- 母题 `"注意力机制的新架构"` → ✅ 命中（LLM 理解语义）

---

## 🛠️ 技术栈

**极简原则：Less is More**

- **语言**：Python 3.10+
- **依赖**：
  - `requests` - HTTP 请求
  - `feedparser` - 解析 arXiv RSS
  - `openai` - LLM API 调用
  - `python-dotenv` - 环境变量管理
- **架构**：单文件脚本 → 模块化（按需重构）

---

## 💡 设计哲学

### 1. 实用主义
> "解决真实问题，不是为论文服务。"

- 优先验证核心价值（母题筛选是否有效）
- 拒绝过度设计（先跑起来，再优化）

### 2. 极简执念
> "如果核心逻辑超过 300 行，说明方向错了。"

- 函数只做一件事并做好
- 复杂性是万恶之源

### 3. 零破坏性
> "未来要加新功能，只需要添加字段，不改现有代码。"

- 数据结构设计为"只增不改"
- 向后兼容是铁律

---

## 📊 成本估算

**假设**：
- 每天爬取 100 篇论文
- 筛选后剩余 20 篇
- 使用 DeepSeek API（¥0.001/1K tokens）

**成本拆解**：
```
1. 母题判断：100 篇 × 300 tokens × ¥0.001 = ¥0.03
2. 论文摘要：20 篇 × 500 tokens × ¥0.001 = ¥0.01
3. 输出生成：20 篇 × 500 tokens × ¥0.001 = ¥0.01

总计：¥0.05/天 ≈ ¥1.5/月
```

**对比人工成本**：
- 人工筛选：30 分钟/天 × ¥100/小时 = ¥50/天
- AI 筛选：¥0.05/天
- **ROI：1000x**

---

## 🧪 验收标准

### 功能完整性
- [ ] 能成功爬取指定类别的 arXiv 论文
- [ ] 母题筛选的准确率 > 80%（手动验证 20 篇）
- [ ] 摘要质量：普通人能在 30 秒内理解论文核心贡献
- [ ] 输出格式：Markdown，适合导入 Obsidian

### 用户体验
- [ ] 运行时间 < 5 分钟（100 篇论文）
- [ ] 配置简单：只需修改 `research_topics.txt`
- [ ] 错误提示清晰：API 失败、网络错误等

### 代码质量
- [ ] 核心逻辑 < 300 行（不含注释）
- [ ] 没有超过 3 层的嵌套
- [ ] 关键函数有单元测试

---

## 📖 相关文档

- **[CLAUDE.md](CLAUDE.md)**：项目总览（给 AI 和开发者看）
- **[specs/requirements.md](specs/requirements.md)**：需求文档（用户故事、验收标准）
- **[specs/design.md](specs/design.md)**：设计文档（数据结构、算法实现）

---

## 🚧 未来扩展（非 MVP 范围）

### 二期功能
1. **Web UI**：网页配置界面，无需编辑配置文件
2. **邮件推送**：每日摘要发送到邮箱
3. **历史追踪**：论文被引量、代码实现追踪
4. **知识图谱**：自动挂载到 Obsidian 概念网络

### 扩展原则
- ❌ **不要**：一次性加所有功能（过度设计）
- ✅ **要**：先验证核心价值（母题筛选是否有效）
- ✅ **要**：每次只加一个功能，确保向后兼容

---

## 📝 许可证

本项目为个人学习项目，代码随意使用。

---

**Remember: Less is More. 如果代码超过 300 行，说明方向错了。**
