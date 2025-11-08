# 项目：daily-arXiv - AI驱动的 arXiv 论文增强工具

## 项目定位

**一句话描述：**
基于 AI 的 arXiv 论文自动抓取、结构化摘要和 Markdown 发布工具，使用 LLM 生成高质量论文摘要。**v2.0 将增加母题筛选功能，实现零漏报 + 80% 降噪。**

**当前版本 (v1.0) 特点：**
- **零基础设施**：基于 GitHub Actions + Pages，无需服务器
- **AI 驱动摘要**：使用阿里百炼/DeepSeek 生成结构化论文摘要（TLDR、动机、方法、结果、结论）
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

- **语言**：Python 3.12+
- **包管理器**：uv (快速、现代的 Python 包管理器)
- **核心依赖**：
  - `scrapy` - 网页爬虫框架
  - `langchain` + `langchain-openai` - LLM 集成和结构化输出
  - `python-dotenv` - 环境变量管理
  - `tqdm` - 进度条显示

---

## 本地环境

- **操作系统**：Windows 11
- **工作目录**：`E:\MarssPython\2511-daily-arXiv`
- **Python 版本**：3.12+ (实际使用 3.12.9，由 uv 管理)
- **虚拟环境**：`.venv` (由 uv 自动创建和管理)

---

## 📁 项目结构

```
E:\MarssPython\2511-daily-arXiv/
├── daily_arxiv/                # Scrapy 爬虫项目
│   └── daily_arxiv/
│       ├── spiders/arxiv.py   # arXiv 爬虫
│       ├── items.py           # 数据结构定义
│       ├── pipelines.py       # 数据处理管道
│       └── settings.py        # Scrapy 配置
├── ai/                         # AI 增强模块
│   ├── structure.py           # 输出结构定义（5个字段）
│   ├── enhance.py             # LLM 摘要生成（并发处理）
│   ├── system.txt             # System Prompt（AI 角色定义）
│   ├── template.txt           # User Prompt（任务指令）
│   └── README.md              # AI 模块使用说明
├── to_md/                      # Markdown 转换
│   └── convert.py             # JSONL → Markdown
├── src/                        # 🆕 v2.0 母题筛选模块（计划中）
│   ├── models.py              # 数据模型
│   ├── config.py              # 配置管理
│   ├── fetcher.py             # 轻量级爬取（可选）
│   └── filter.py              # 母题筛选（待实现）
├── docs/                       # 📚 详细文档
│   ├── data-structures.md     # 数据结构设计
│   ├── workflows.md           # 核心工作流
│   └── v2-design.md           # v2.0 设计方案
├── config/                     # 配置文件
│   └── research_topics.txt    # 研究母题列表（v2.0）
├── data/                       # 发布的 Markdown 文件
├── .env                        # 环境变量配置
├── run_ai_enhance.ps1         # AI 增强便捷脚本
├── update_readme.py            # README 自动生成
├── pyproject.toml             # 项目配置和依赖
└── README.md                  # 用户使用指南
```

**架构演进：**
- **v1.0（当前）**：Scrapy 爬虫 → AI 增强（所有论文） → Markdown 转换 → GitHub Pages
- **v2.0（升级）**：Scrapy 爬虫 → **母题筛选** → AI 增强（仅相关论文） → Markdown 转换 → GitHub Pages

---

## 📖 文档导航

### 核心文档

| 文档 | 说明 |
|------|------|
| [数据结构设计](docs/data-structures.md) | 详细的数据格式说明（JSONL、AI 增强输出、Python 模型） |
| [核心工作流](docs/workflows.md) | 完整的数据处理流程（爬虫→AI→Markdown） |
| [v2.0 设计](docs/v2-design.md) | 母题筛选功能设计（降低 80% 成本） |
| [AI 模块说明](ai/README.md) | Prompt 配置和自定义指南 |

### 快速链接

- **数据格式**：参见 [data-structures.md](docs/data-structures.md)
- **工作流程**：参见 [workflows.md](docs/workflows.md)
- **AI 配置**：参见 [ai/README.md](ai/README.md)
- **v2.0 功能**：参见 [v2-design.md](docs/v2-design.md)

---

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆仓库
git clone <your-repo-url>
cd 2511-daily-arXiv

# 使用 uv 安装依赖（推荐）
uv sync

# 激活虚拟环境（Windows PowerShell）
.venv\Scripts\Activate.ps1
```

**为什么选择 uv？**
- ⚡ **快速**：比 pip 快 10-100 倍
- 🔒 **可靠**：自动创建和管理虚拟环境
- 📦 **现代**：支持 pyproject.toml，无需 requirements.txt
- 🎯 **精确**：使用 uv.lock 确保依赖版本一致

### 2. 配置 API

创建 `.env` 文件：

```bash
# 阿里百炼 API 配置（推荐）
OPENAI_API_KEY=sk-xxxxxxxx
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
MODEL_NAME=qwen-plus

# arXiv 类别配置
CATEGORIES=cs.AI, cs.CL, cs.CV

# AI 增强配置
LANGUAGE=Chinese
MAX_WORKERS=10
```

**支持的模型：**
- **阿里百炼（推荐）**：`qwen-plus`（性价比高）、`qwen-turbo`（速度快）、`qwen-max`（最强）
- **DeepSeek**：`deepseek-chat`

### 3. 运行流程

**使用便捷脚本（推荐）：**

```powershell
# 步骤 1：爬取论文（无需 API）
cd daily_arxiv
$env:CATEGORIES="cs.AI"
../.venv/Scripts/python.exe -m scrapy crawl arxiv -o "../data/2025-11-08.jsonl"
cd ..

# 步骤 2：AI 增强（生成中文摘要）
.\run_ai_enhance.ps1

# 步骤 3：转换为 Markdown
cd to_md
python convert.py --data "../data/2025-11-08_AI_enhanced_Chinese.jsonl"
cd ..

# 步骤 4：更新 README
python update_readme.py
```

详细的命令说明和工作流程请参见 [workflows.md](docs/workflows.md)。

### 4. 查看结果

生成的文件在 `data/` 目录：
- `{date}.jsonl` - 原始爬取数据
- `{date}_AI_enhanced_Chinese.jsonl` - AI 增强后的数据
- `{date}.md` - 最终的 Markdown 文档

---

## ⚙️ 配置说明

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `OPENAI_API_KEY` | API 密钥 | 必填 |
| `OPENAI_BASE_URL` | API 地址 | 必填 |
| `MODEL_NAME` | 模型名称 | `qwen-plus` |
| `CATEGORIES` | arXiv 类别 | `cs.AI` |
| `LANGUAGE` | 摘要语言 | `Chinese` |
| `MAX_WORKERS` | 并发数 | `10` |

### AI 模块配置

AI 增强模块支持自定义 Prompt 和输出结构，详见 [ai/README.md](ai/README.md)：
- **structure.py** - 修改输出字段
- **system.txt** - 修改 AI 角色定义
- **template.txt** - 修改任务指令

---

## 💡 核心概念

### 数据流转

```
爬虫抓取 → JSONL 原始数据 → AI 增强 → JSONL 增强数据 → Markdown 转换 → GitHub Pages
```

详细的数据结构说明请参见 [data-structures.md](docs/data-structures.md)。

### AI 增强输出

每篇论文生成 5 个结构化字段：
- **TLDR**: 一句话总结
- **Motivation**: 研究动机和背景
- **Method**: 技术方案
- **Result**: 实验结果
- **Conclusion**: 结论和未来工作

### v2.0 升级计划

v2.0 将在爬虫和 AI 增强之间插入**母题筛选**步骤：
- 使用 LLM 判断论文是否匹配用户关心的研究母题
- 只对相关论文生成摘要，成本降低 80%
- 详细设计请参见 [v2-design.md](docs/v2-design.md)

---

## 🔧 常见任务

### 修改抓取的论文类别

编辑 `.env` 文件：
```bash
CATEGORIES=cs.AI, cs.CL, cs.CV, cs.LG
```

### 自定义 AI 摘要格式

参见 [ai/README.md](ai/README.md) 中的 Prompt 配置说明。

### 切换模型

编辑 `.env` 文件：
```bash
# 使用 DeepSeek
OPENAI_BASE_URL=https://api.deepseek.com
MODEL_NAME=deepseek-chat

# 使用阿里百炼
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
MODEL_NAME=qwen-plus
```

### 查看历史数据

历史 JSONL 和 Markdown 文件位于：
- `data/` - 发布的 Markdown 文件
- `output/archive/` - 历史 JSONL 归档

---

## 📊 性能与成本

### 性能指标

- **爬取速度**: ~3秒/篇（礼貌爬取）
- **AI 增强**: ~2-5秒/篇（取决于并发数和模型）
- **总耗时**: ~5-10分钟（100篇论文）

### 成本估算

**阿里百炼 qwen-plus（推荐）：**
- 输入: ¥0.0004/1K tokens
- 输出: ¥0.0012/1K tokens
- 平均: ¥0.002/篇论文
- **100篇/天**: 约 ¥0.20

**v2.0 成本对比：**
- v1.0：100篇 × ¥0.002 = ¥0.20
- v2.0：20篇相关论文 × (筛选 + 摘要) ≈ ¥0.05
- **节省 75%！**

---

## 🐛 故障排除

### 代理问题

访问国内 API（如阿里百炼）时需禁用代理：

```powershell
# 临时禁用（PowerShell）
$env:HTTP_PROXY=""
$env:HTTPS_PROXY=""
$env:ALL_PROXY=""
```

`run_ai_enhance.ps1` 脚本已自动处理。

### API 错误

检查配置：
```powershell
echo $env:OPENAI_API_KEY
echo $env:OPENAI_BASE_URL
echo $env:MODEL_NAME
```

### 模块未找到

确保使用虚拟环境中的 Python：
```powershell
# 正确
.venv\Scripts\python.exe -m scrapy crawl arxiv

# 错误（使用系统 Python）
python -m scrapy crawl arxiv
```

---

## 🎯 开发约定

### 设计原则

- **实用主义**：Production-Ready 优先
- **模块化**：每个模块职责单一
- **向后兼容**：数据结构只增不改
- **错误容错**：LLM 调用失败不中断流程
- **成本控制**：去重、并发控制、轻量级模型

### 扩展原则

- ✅ **要**：保持模块独立性和兼容性
- ✅ **要**：每次只加一个功能，充分测试
- ❌ **不要**：破坏现有功能的稳定性

---

## 📚 相关资源

- **原项目**：[dw-dengwei/daily-arXiv-ai-enhanced](https://github.com/dw-dengwei/daily-arXiv-ai-enhanced)
- **详细文档**：查看 `docs/` 目录
- **用户指南**：[README.md](README.md)
- **项目配置**：[pyproject.toml](pyproject.toml)

---

## ✨ 总结

这是一个**实用主义 + Production-Ready** 的 AI 工具：

- **核心价值**：零基础设施，完全自动化的 arXiv 论文摘要生成
- **技术栈**：Scrapy + LangChain + GitHub Actions + Pages
- **成本**：约 ¥0.2/天，完全免费部署
- **未来升级**：v2.0 母题筛选功能，降低 80% 成本

**详细文档请查看 `docs/` 目录。**
