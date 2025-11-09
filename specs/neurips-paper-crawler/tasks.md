# 任务清单：NeurIPS 会议论文爬取与增强

> **实用主义原则**：合并细碎任务，关注可交付成果

---

## 阶段 1：核心爬虫实现（P0）✅ **已完成**

- [x] **任务 1：实现 NeurIPS 爬虫核心功能**
  - 文件：`daily_arxiv/daily_arxiv/spiders/neurips.py`
  - 完成内容：
    - ✅ Spider 骨架（支持 `year` 和 `category` 参数）
    - ✅ 列表页解析（提取 title, authors, summary）
    - ✅ 详情页解析（提取 OpenReview 链接，生成 PDF URL）
    - ✅ ID 生成逻辑（`neurips2024_oral_{id}`）
    - ✅ 数据标准化输出（JSONL 格式，与 arXiv 兼容）
    - ✅ 优雅降级（缺 PDF 时仍输出基本信息）
    - ✅ 必需字段验证（title/summary 缺失则跳过）
    - ✅ 错误处理和统计（失败计数、PDF 缺失统计）
  - 验证结果：
    - ✅ 成功爬取 72 篇 NeurIPS 2024 Oral 论文列表
    - ✅ 测试数据（6 篇）全部通过字段验证
    - ✅ 优雅降级生效（2 篇缺 PDF 但仍输出）
    - ✅ 统计信息正常显示
  - 耗时：约 2 小时

---

## 阶段 2：AI 增强集成验证（P1）

- [ ] **任务 2：测试 AI 增强流程兼容性**
  - 需求：REQ-4.1, REQ-4.2, REQ-4.3
  - 验证：
    ```powershell
    cd ai
    ../.venv/Scripts/python.exe enhance.py --data ../daily_arxiv/test-5.jsonl --max_workers 2
    ```
  - 验证目标：
    - [ ] 生成 `test-5_AI_enhanced_Chinese.jsonl`
    - [ ] 包含所有 AI 结构化字段（由 `structure.py` 定义）
    - [ ] `source: "neurips"` 字段被正确透传
  - 预计耗时：2-5 分钟

- [ ] **任务 3：测试 Markdown 转换兼容性**
  - 需求：REQ-5.1, REQ-5.5
  - 验证：
    ```powershell
    cd to_md
    python convert.py --data ../daily_arxiv/test-5_AI_enhanced_Chinese.jsonl
    ```
  - 验证目标：
    - [ ] 生成 Markdown 文件
    - [ ] 格式正确（标题、作者、摘要、AI 增强字段可见）
    - [ ] 无乱码
  - 预计耗时：~30 秒

---

## 阶段 3：完整流程测试（P1）

- [ ] **任务 4：完整爬取所有 NeurIPS 2024 Oral 论文**
  - 需求：REQ-1 至 REQ-7（所有需求）
  - 执行：
    ```powershell
    cd daily_arxiv
    ../.venv/Scripts/python.exe -m scrapy crawl neurips -o ../data/neurips-2024-oral.jsonl
    ```
  - 验证目标：
    - [ ] 成功爬取 50+ 篇论文
    - [ ] 失败率 < 10%
    - [ ] 手动抽查 3 篇数据质量
  - 预计耗时：5-10 分钟

- [ ] **任务 5：完整 AI 增强流程**
  - 需求：REQ-4
  - 执行：
    ```powershell
    cd ai
    ../.venv/Scripts/python.exe enhance.py --data ../data/neurips-2024-oral.jsonl --max_workers 10
    ```
  - 验证目标：
    - [ ] 生成 `neurips-2024-oral_AI_enhanced_Chinese.jsonl`
    - [ ] AI 增强成功率 > 90%
  - 预计耗时：10-20 分钟

- [ ] **任务 6：生成最终 Markdown 文件**
  - 需求：REQ-5
  - 执行：
    ```powershell
    cd to_md
    python convert.py --data ../data/neurips-2024-oral_AI_enhanced_Chinese.jsonl
    ```
  - 验证目标：
    - [ ] 生成 `neurips-2024-oral.md`
    - [ ] 目录包含 "NeurIPS 2024 Oral"
    - [ ] 随机抽查 3 篇格式正确
  - 预计耗时：~30 秒

---

## 阶段 4：发布与文档（P2）

- [ ] **任务 7：更新项目文档**
  - 文件：`README.md`, `CLAUDE.md`
  - 内容：
    - [ ] 添加 NeurIPS 爬虫使用说明
    - [ ] 添加示例命令
    - [ ] 更新架构图（可选）
  - 预计耗时：< 10 分钟

- [ ] **任务 8：验证 GitHub Pages 发布**
  - 需求：REQ-5.4
  - 执行：
    - [ ] 提交并推送 `data/neurips-2024-oral.md` 到 GitHub
    - [ ] 等待 GitHub Actions 构建完成
    - [ ] 访问 GitHub Pages 检查论文可见性
  - 预计耗时：5-10 分钟（含等待构建）

- [ ] **任务 9：清理测试文件**
  - 执行：
    - [ ] 删除或归档测试文件：
      - `daily_arxiv/test.jsonl`
      - `daily_arxiv/test-5.jsonl`
      - 相关 AI 增强输出
    - [ ] 移除验证脚本 `verify_neurips_output.py`（或移到 `tools/`）
  - 预计耗时：< 1 分钟

---

## 任务统计

### 按阶段
- **阶段 1（P0 核心功能）**：✅ 已完成（1 个任务）
- **阶段 2（P1 集成测试）**：⏳ 进行中（2 个任务）
- **阶段 3（P1 完整流程）**：⏳ 待开始（3 个任务）
- **阶段 4（P2 发布文档）**：⏳ 待开始（3 个任务）

### 预计总时间
- **核心实现（P0）**：✅ 2 小时（已完成）
- **集成测试（P1）**：⏳ 5-30 分钟
- **完整流程（P1）**：⏳ 15-30 分钟
- **发布文档（P2）**：⏳ 15-20 分钟
- **总计**：约 2.5-3 小时

---

## 关键提示

### 调试技巧
1. **查看 Scrapy 日志**：添加 `-s LOG_LEVEL=DEBUG` 查看详细日志
2. **限制爬取数量**：使用 `-s CLOSESPIDER_ITEMCOUNT=N` 快速测试
3. **检查 HTML 结构**：使用 `scrapy shell "https://neurips.cc/virtual/2024/events/oral"` 交互式调试

### 常见问题
1. **CSS 选择器失效**：网页结构可能变化，需要调整选择器
2. **OpenReview 链接格式变化**：检查实际 URL 格式，调整正则表达式
3. **AI 增强超时**：减少 `--max_workers` 或增加超时时间

### 快速验证脚本

**验证 JSONL 数据质量**：
```python
import json
with open('data/neurips-2024-oral.jsonl') as f:
    items = [json.loads(line) for line in f]
    print(f"总计: {len(items)} 篇")
    required = ['id', 'title', 'authors', 'summary', 'abs', 'pdf', 'categories', 'source']
    for item in items[:3]:  # 抽查前3篇
        assert all(field in item for field in required)
        print(f"✓ {item['id']}: {item['title'][:60]}...")
    print("✅ 验证通过")
```

**检查 AI 增强完成率**：
```python
import json
with open('data/neurips-2024-oral_AI_enhanced_Chinese.jsonl') as f:
    items = [json.loads(line) for line in f]
    success = sum(1 for item in items if 'AI' in item and 'core_problem' in item['AI'])
    print(f"AI 增强成功率: {success}/{len(items)} ({success/len(items)*100:.1f}%)")
```

---

## 验收测试场景（对应需求文档）

### 场景 1：首次爬取 NeurIPS 2024 Oral ✅
- **覆盖任务**：1, 2, 3, 4, 5, 6
- **状态**：阶段 1 已完成，待执行阶段 2-3

### 场景 2：与 arXiv 爬虫并行（可选）
- **验证**：
  - 打开两个终端
  - 终端 1：`scrapy crawl arxiv -o test-arxiv.jsonl -s CLOSESPIDER_ITEMCOUNT=5`
  - 终端 2：`scrapy crawl neurips -o test-neurips.jsonl -s CLOSESPIDER_ITEMCOUNT=5`
  - 检查两个爬虫互不干扰
- **预计耗时**：~2 分钟

### 场景 3：网络异常恢复 ✅
- **状态**：已通过（优雅降级测试中 2 篇缺 PDF 仍成功输出）
