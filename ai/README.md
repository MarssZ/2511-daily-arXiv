# AI 增强模块

> **导航**: [← 返回主文档](../CLAUDE.md) | [数据结构](../docs/data-structures.md) | [核心工作流](../docs/workflows.md) | [v2.0 设计](../docs/v2-design.md)

使用 LLM 为论文生成结构化中文摘要。

## 快速使用

```powershell
# 使用便捷脚本（推荐）
.\run_ai_enhance.ps1

# 或手动运行
cd ai
python enhance.py --data ../data/2025-11-08.jsonl --max_workers 10
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `enhance.py` | 主程序（并发处理、错误处理） |
| `structure.py` | 输出结构定义（5个字段） |
| `system.txt` | System Prompt（AI 角色定义） |
| `template.txt` | User Prompt（任务指令） |

## 输出结构

生成 5 个结构化字段：

```json
{
  "AI": {
    "tldr": "一句话总结",
    "motivation": "研究动机和背景",
    "method": "技术方案",
    "result": "实验结果",
    "conclusion": "结论和未来工作"
  }
}
```

## 配置

通过 `.env` 文件或环境变量配置：

```bash
OPENAI_API_KEY=sk-xxx          # API 密钥
OPENAI_BASE_URL=https://...    # API 地址
MODEL_NAME=qwen-plus            # 模型名称
LANGUAGE=Chinese                # 输出语言
MAX_WORKERS=10                  # 并发数
```

### 支持的模型

**阿里百炼（推荐）：**
- `qwen-plus` - 性价比高（推荐）
- `qwen-turbo` - 速度快
- `qwen-max` - 最强性能

**DeepSeek：**
- `deepseek-chat` - 通用模型

## 自定义 Prompt

### 修改角色定义（system.txt）

```
You are a professional paper analyst.
Your output should in {language}.
```

### 修改任务指令（template.txt）

```
Please analyze the following abstract of papers.

Content:
{content}
```

**优化建议：**
- 为每个字段添加具体要求（如"TLDR 不超过50字"）
- 强调关注点（如"重点分析实验结果"）
- 提供示例输出

### 修改输出结构（structure.py）

```python
class Structure(BaseModel):
    tldr: str = Field(description="...")
    motivation: str = Field(description="...")
    # 添加新字段
    innovation: str = Field(description="创新点")
```

## 性能优化

- **并发控制**: 根据 API 限制调整 `MAX_WORKERS`
- **错误重试**: 代码已内置重试机制
- **敏感词过滤**: 自动调用外部 API 检查

## 成本估算

**阿里百炼 qwen-plus：**
- 输入: ¥0.0004/1K tokens
- 输出: ¥0.0012/1K tokens
- 平均: ¥0.002/篇论文
- **100篇/天**: 约 ¥0.20

## 故障排除

### 代理问题

访问国内 API（如阿里百炼）时，需禁用代理：

```powershell
# 临时禁用
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
```

## 相关文档

- [工作流](../docs/workflows.md) - 完整流程
- [数据结构](../docs/data-structures.md) - 输入输出格式
