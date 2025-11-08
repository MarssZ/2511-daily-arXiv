# 🚀 GitHub Pages 部署完整指南

> **仓库地址**: https://github.com/MarssZ/2511-daily-arXiv
> **部署后访问地址**: https://marssz.github.io/2511-daily-arXiv/

---

## 📋 目录

1. [前置准备](#前置准备)
2. [第一步：配置 GitHub Secrets](#第一步配置-github-secrets)
3. [第二步：配置 GitHub Variables](#第二步配置-github-variables)
4. [第三步：启用 GitHub Pages](#第三步启用-github-pages)
5. [第四步：手动触发工作流测试](#第四步手动触发工作流测试)
6. [第五步：验证部署](#第五步验证部署)
7. [常见问题排查](#常见问题排查)

---

## 前置准备

### ✅ 必需项

- [x] GitHub 账号
- [x] 阿里百炼 API Key（已配置在本地 `.env` 文件中）
- [x] 已将代码推送到 GitHub 仓库

### 📝 检查清单

在开始之前，确保：

1. **本地 `.env` 文件存在**，包含以下内容：
   ```bash
   OPENAI_API_KEY=sk-xxxxxxxxxx
   OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
   MODEL_NAME=qwen-plus
   CATEGORIES=cs.AI, cs.CL, cs.CV
   LANGUAGE=Chinese
   ```

2. **代码已推送到 GitHub**：
   ```bash
   git push -u origin main
   ```

---

## 第一步：配置 GitHub Secrets

Secrets 用于存储敏感信息（如 API Key），只有 GitHub Actions 可以访问。

### 1.1 打开 Secrets 配置页面

1. 访问你的仓库：https://github.com/MarssZ/2511-daily-arXiv
2. 点击顶部导航栏的 **Settings** (⚙️设置)
3. 在左侧边栏找到 **Secrets and variables** → 点击 **Actions**

![Settings位置](../assets/deploy-settings.png)

### 1.2 添加 Secrets

点击右上角的 **New repository secret** 按钮，依次添加以下 3 个 Secrets：

#### Secret 1: OPENAI_API_KEY（必需）

- **Name**: `OPENAI_API_KEY`
- **Secret**: 粘贴你的阿里百炼 API Key（从本地 `.env` 文件中复制）
  ```
  sk-0e687ddcf0164a6fb66c1096447223c4
  ```
- 点击 **Add secret**

#### Secret 2: OPENAI_BASE_URL（必需）

- **Name**: `OPENAI_BASE_URL`
- **Secret**:
  ```
  https://dashscope.aliyuncs.com/compatible-mode/v1
  ```
- 点击 **Add secret**

#### Secret 3: ACCESS_PASSWORD（可选）

> **注意**：如果不设置此项，网站将**公开访问**（无需密码）

- **Name**: `ACCESS_PASSWORD`
- **Secret**: 输入你想设置的访问密码（例如：`mypassword123`）
- 点击 **Add secret**

### ✅ Secrets 配置完成

你应该看到 3 个 Secrets（如果跳过 ACCESS_PASSWORD，则是 2 个）：

- `OPENAI_API_KEY`
- `OPENAI_BASE_URL`
- `ACCESS_PASSWORD` (可选)

---

## 第二步：配置 GitHub Variables

Variables 用于存储非敏感的配置信息。

### 2.1 切换到 Variables 标签

在同一页面（Settings → Secrets and variables → Actions），点击顶部的 **Variables** 标签。

### 2.2 添加 Variables

点击右上角的 **New repository variable** 按钮，依次添加以下 5 个 Variables：

#### Variable 1: MODEL_NAME

- **Name**: `MODEL_NAME`
- **Value**: `qwen-plus`
- 点击 **Add variable**

#### Variable 2: LANGUAGE

- **Name**: `LANGUAGE`
- **Value**: `Chinese`
- 点击 **Add variable**

#### Variable 3: CATEGORIES

- **Name**: `CATEGORIES`
- **Value**: `cs.AI, cs.CL, cs.CV`
- 点击 **Add variable**

> **提示**：可以根据需要修改类别，多个类别用逗号+空格分隔

#### Variable 4: EMAIL

- **Name**: `EMAIL`
- **Value**: 输入你的 GitHub 邮箱（用于 Git 提交）
  ```
  your-email@example.com
  ```
- 点击 **Add variable**

#### Variable 5: NAME

- **Name**: `NAME`
- **Value**: 输入你的名字（用于 Git 提交）
  ```
  Your Name
  ```
- 点击 **Add variable**

### ✅ Variables 配置完成

你应该看到 5 个 Variables：

- `MODEL_NAME` = `qwen-plus`
- `LANGUAGE` = `Chinese`
- `CATEGORIES` = `cs.AI, cs.CL, cs.CV`
- `EMAIL` = 你的邮箱
- `NAME` = 你的名字

---

## 第三步：启用 GitHub Pages

### 3.1 打开 Pages 设置

1. 在仓库页面，点击顶部导航栏的 **Settings**
2. 在左侧边栏找到 **Pages** (🌐网页)

### 3.2 配置部署源

在 **Source** 部分：

- **Source**: 选择 `Deploy from a branch`
- **Branch**: 选择 `main`
- **Folder**: 选择 `/` (root)

点击 **Save** 保存。

### 3.3 等待部署

GitHub 会开始构建网站，大约 1-2 分钟后，你会看到：

```
✅ Your site is live at https://marssz.github.io/2511-daily-arXiv/
```

> **注意**：此时网站是空的，因为还没有运行 GitHub Actions 生成数据。

---

## 第四步：手动触发工作流测试

### 4.1 打开 Actions 页面

1. 在仓库页面，点击顶部导航栏的 **Actions**
2. 在左侧边栏找到 **arXiv-daily-ai-enhanced** 工作流
3. 点击右侧的 **Run workflow** 下拉菜单
4. 点击绿色的 **Run workflow** 按钮

![Run Workflow](../assets/deploy-run-workflow.png)

### 4.2 监控运行状态

工作流将开始运行，你会看到一个黄色的运行中状态。

**预计耗时**：
- 爬取论文：2-5 分钟（取决于论文数量）
- AI 增强：25-40 分钟（约 100 篇论文，17秒/篇）
- 转换 + 推送：1-2 分钟

**总计**：约 30-50 分钟

### 4.3 检查运行日志

点击正在运行的工作流，查看详细日志：

1. 点击工作流名称（例如：`update: 2025-11-09 arXiv papers`）
2. 点击左侧的 **build** 任务
3. 展开各个步骤查看日志：
   - ✅ **Crawl arXiv papers** - 爬取成功
   - ✅ **Check for duplicates** - 去重检查
   - ✅ **AI Enhancement Processing** - AI 处理进度
   - ✅ **Convert to Markdown** - 转换完成
   - ✅ **Commit changes** - 提交成功

### 4.4 等待完成

当所有步骤都显示 ✅ 绿色对勾时，表示运行成功！

---

## 第五步：验证部署

### 5.1 访问网站

打开浏览器，访问：

```
https://marssz.github.io/2511-daily-arXiv/
```

### 5.2 预期看到的内容

#### 如果设置了 ACCESS_PASSWORD：

1. 首先会看到登录页面
2. 输入你设置的密码
3. 登录后进入主页

#### 主页功能：

- **日期选择器**：顶部可以选择查看不同日期的论文
- **论文列表**：按类别分组展示（cs.AI, cs.CL, cs.CV）
- **论文卡片**：
  - 标题（可点击跳转到 arXiv）
  - 价值评分（高价值 badge）
  - 💡 大白话版（一眼看懂）
  - 🎯 核心价值（专业总结）
  - 📖 详细分析（折叠，点击展开）

#### 其他页面：

- **统计页** (`statistic.html`): 论文数量趋势图
- **设置页** (`settings.html`): 个性化配置

### 5.3 检查自动更新

每天北京时间 **09:30**，GitHub Actions 会自动运行，更新论文数据。

你可以在 **Actions** 页面查看历史运行记录。

---

## 常见问题排查

### ❌ 问题1：工作流运行失败

**症状**：Actions 页面显示红色 ❌

**解决方案**：

1. 点击失败的工作流，查看错误日志
2. 常见错误：
   - **API Key 无效**：检查 `OPENAI_API_KEY` 是否正确
   - **爬取失败**：arXiv 可能临时不可用，等待下次自动运行
   - **AI 处理失败**：检查 API 余额是否充足

### ❌ 问题2：网站显示 404

**症状**：访问网站显示 "404 Page Not Found"

**解决方案**：

1. 检查 GitHub Pages 是否正确启用（Settings → Pages）
2. 确保 `index.html` 文件在仓库根目录
3. 等待 5 分钟，GitHub Pages 需要时间部署

### ❌ 问题3：网站没有数据

**症状**：网站可以访问，但没有论文列表

**解决方案**：

1. 检查 Actions 是否成功运行（至少运行一次）
2. 检查 `data/` 目录是否有生成的 `.md` 文件
3. 手动触发一次工作流（Actions → Run workflow）

### ❌ 问题4：代理问题

**症状**：AI 增强步骤报错 "socksio package is not installed"

**解决方案**：

已在 `ai/enhance.py` 中自动禁用代理，如果仍有问题：

1. 检查 GitHub Actions 环境变量
2. 确认 `OPENAI_BASE_URL` 正确指向阿里百炼

### ❌ 问题5：字段不匹配

**症状**：Markdown 生成失败，显示 "incomplete AI fields"

**解决方案**：

确保本地测试成功后再推送：

```bash
# 本地测试完整流程
cd daily_arxiv
../.venv/Scripts/python.exe -m scrapy crawl arxiv -o "../data/test.jsonl"

cd ../ai
../.venv/Scripts/python.exe enhance.py --data "../data/test.jsonl" --max_workers 5

cd ../to_md
../.venv/Scripts/python.exe convert.py --data "../data/test_AI_enhanced_Chinese.jsonl"
```

---

## 🎉 完成！

恭喜！你的 AI 驱动的 arXiv 论文追踪系统已经部署完成。

### 📅 自动化时间线

```
每天 09:30 北京时间
    ↓
GitHub Actions 自动触发
    ↓
爬取 + AI 增强 + 转换
    ↓
自动推送到仓库
    ↓
GitHub Pages 自动更新
    ↓
✅ 10:00-10:30 网站更新完成！
```

### 🔗 相关链接

- **网站地址**: https://marssz.github.io/2511-daily-arXiv/
- **仓库地址**: https://github.com/MarssZ/2511-daily-arXiv
- **Actions 日志**: https://github.com/MarssZ/2511-daily-arXiv/actions
- **阿里百炼控制台**: https://dashscope.console.aliyun.com/

### 📊 成本估算

- **每日成本**: ¥0.60-0.80 (约 100 篇论文)
- **每月成本**: ¥20-25
- **基础设施**: 完全免费（GitHub Actions + Pages）

### 🛠️ 后续调整

如果需要修改配置（如类别、模型），只需：

1. 修改 GitHub Variables (Settings → Secrets and variables → Actions)
2. 无需改代码，下次运行自动生效

---

## 📞 技术支持

如遇到问题，可以：

1. 查看 [GitHub Actions 日志](https://github.com/MarssZ/2511-daily-arXiv/actions)
2. 检查 [Issues](https://github.com/MarssZ/2511-daily-arXiv/issues)
3. 参考原项目文档：[dw-dengwei/daily-arXiv-ai-enhanced](https://github.com/dw-dengwei/daily-arXiv-ai-enhanced)

---

**文档版本**: v1.0
**最后更新**: 2025-11-09
**作者**: Claude Code
