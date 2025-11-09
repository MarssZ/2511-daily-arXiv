# 任务清单：NeurIPS 会议论文爬取与增强

> **排序原则**：按验证容易程度排序，越容易发现 bug 的功能越早做，避免错误传染

---

## 阶段 1：核心爬虫实现（P0）

### 1秒验证任务

- [ ] 1. 创建 NeurIPSSpider 骨架
  - 需求：REQ-6.1
  - 文件：`daily_arxiv/daily_arxiv/spiders/neurips.py`
  - 验证：
    - 运行 `scrapy list` → 输出包含 `neurips`
    - 耗时：< 1秒

- [ ] 2. 配置爬虫基本参数
  - 需求：REQ-6.3, REQ-6.4
  - 文件：`daily_arxiv/daily_arxiv/spiders/neurips.py`
  - 实现：
    - `__init__` 方法支持 `year` 和 `category` 参数
    - `start_urls` 动态生成
    - `custom_settings` 禁用 Pipeline + 礼貌爬取
  - 验证：
    - 运行 `scrapy crawl neurips --help` → 显示可用参数
    - 耗时：< 1秒

---

### 5秒验证任务

- [ ] 3. 实现列表页解析（parse 方法）
  - 需求：REQ-1.1, REQ-1.2
  - 文件：`daily_arxiv/daily_arxiv/spiders/neurips.py`
  - 实现：
    - 提取论文基本信息（title, authors, summary）
    - 生成详情页 URL
    - 构造 scrapy.Request 传递数据到 parse_detail
  - 验证：
    - 添加调试日志：`self.logger.info(f"Found paper: {title}")`
    - 运行 `scrapy crawl neurips -s CLOSESPIDER_ITEMCOUNT=1`
    - Console 显示：`Found paper: [论文标题]`
    - 耗时：~5秒

- [ ] 4. 实现详情页解析（parse_detail 方法）
  - 需求：REQ-2.1, REQ-2.2
  - 文件：`daily_arxiv/daily_arxiv/spiders/neurips.py`
  - 实现：
    - 提取 OpenReview 链接（多候选选择器）
    - 生成 PDF URL
    - 合并所有字段输出完整 Item
  - 验证：
    - 添加调试日志：`self.logger.info(f"OpenReview: {openreview_link}")`
    - 运行 `scrapy crawl neurips -s CLOSESPIDER_ITEMCOUNT=1`
    - Console 显示：`OpenReview: https://openreview.net/forum?id=...`
    - 耗时：~5秒

- [ ] 5. 实现 ID 生成逻辑
  - 需求：REQ-1.3
  - 文件：`daily_arxiv/daily_arxiv/spiders/neurips.py`
  - 实现：
    - 从详情页 URL 提取 ID（如 `/oral/97958` → `97958`）
    - 生成格式：`neurips2024_oral_{id}`
  - 验证：
    - 运行 `scrapy crawl neurips -o test.jsonl -s CLOSESPIDER_ITEMCOUNT=1`
    - 打开 `test.jsonl` → ID 格式正确（如 `neurips2024_oral_97958`）
    - 耗时：< 5秒

---

### 简单操作验证（10-30秒）

- [ ] 6. 实现数据输出标准化
  - 需求：REQ-3.2, REQ-3.3
  - 文件：`daily_arxiv/daily_arxiv/spiders/neurips.py`
  - 实现：
    - 确保所有字段类型正确（authors 是数组，categories 是数组）
    - 添加固定字段：`source: "neurips"`, `comment: null`, `categories: ["NeurIPS 2024 Oral"]`
  - 验证：
    - 运行 `scrapy crawl neurips -o test.jsonl -s CLOSESPIDER_ITEMCOUNT=3`
    - 运行验证脚本：
      ```python
      import json
      with open('test.jsonl') as f:
          for line in f:
              item = json.loads(line)
              assert isinstance(item['authors'], list), "authors 应为数组"
              assert isinstance(item['categories'], list), "categories 应为数组"
              assert item['source'] == 'neurips', "source 应为 'neurips'"
              assert item['comment'] is None, "comment 应为 null"
              print(f"✓ {item['id']}: 字段类型正确")
      print("✅ 所有字段验证通过")
      ```
    - 耗时：~10秒

- [ ] 7. 实现优雅降级（OpenReview 链接缺失处理）
  - 需求：REQ-2.3, REQ-2.5
  - 文件：`daily_arxiv/daily_arxiv/spiders/neurips.py`
  - 实现：
    - OpenReview 链接缺失时，PDF 字段设为 `""`
    - 详情页请求失败时，仍输出基本信息
    - 添加日志记录
  - 验证：
    - 修改代码，强制让第一篇论文的 OpenReview 链接返回空
    - 运行 `scrapy crawl neurips -o test.jsonl -s CLOSESPIDER_ITEMCOUNT=1`
    - 打开 `test.jsonl` → `pdf` 字段为空字符串
    - Console 显示：`No OpenReview link found for neurips2024_oral_..., PDF field left empty`
    - 恢复代码
    - 耗时：~15秒

- [ ] 8. 实现必需字段验证
  - 需求：REQ-1.4
  - 文件：`daily_arxiv/daily_arxiv/spiders/neurips.py`
  - 实现：
    - 检查 title 和 summary 是否存在且非空
    - 缺失时记录警告并跳过该论文
  - 验证：
    - 修改代码，强制让第一篇论文的 title 返回空
    - 运行 `scrapy crawl neurips -o test.jsonl -s CLOSESPIDER_ITEMCOUNT=2`
    - Console 显示：`WARNING: Skipping paper due to missing title`
    - `test.jsonl` 只包含 1 条记录（第二篇论文）
    - 恢复代码
    - 耗时：~15秒

---

### 状态验证（1-2分钟）

- [ ] 9. 实现完整数据爬取测试（5篇论文）
  - 需求：REQ-1.1-1.5, REQ-2.1-2.5, REQ-3.1-3.4
  - 文件：`daily_arxiv/daily_arxiv/spiders/neurips.py`
  - 验证：
    - 运行 `cd daily_arxiv && scrapy crawl neurips -o ../data/test-5.jsonl -s CLOSESPIDER_ITEMCOUNT=5`
    - 验证脚本：
      ```python
      import json
      with open('data/test-5.jsonl') as f:
          items = [json.loads(line) for line in f]
          assert len(items) == 5, f"Expected 5 items, got {len(items)}"
          for item in items:
              # 验证必需字段
              required = ['id', 'title', 'authors', 'summary', 'abs', 'pdf', 'categories', 'source']
              for field in required:
                  assert field in item, f"Missing field: {field}"
              # 验证字段类型
              assert isinstance(item['authors'], list)
              assert isinstance(item['categories'], list)
              assert item['source'] == 'neurips'
              # 验证 ID 格式
              assert item['id'].startswith('neurips2024_oral_')
              print(f"✓ {item['id']}: {item['title'][:50]}...")
      print("✅ All 5 papers validated successfully")
      ```
    - 耗时：~1分钟

- [ ] 10. 实现错误处理和统计
  - 需求：REQ-7.1-7.5
  - 文件：`daily_arxiv/daily_arxiv/spiders/neurips.py`
  - 实现：
    - 添加计数器：`self.failed_count`, `self.no_pdf_count`
    - 在 `closed()` 方法中输出统计信息
    - 失败率 > 50% 时输出告警
  - 验证：
    - 运行 `scrapy crawl neurips -o test.jsonl -s CLOSESPIDER_ITEMCOUNT=5`
    - Console 最后显示：
      ```
      ===== NeurIPS Crawler Statistics =====
      Total papers processed: 5
      Successful items: 5
      Failed detail pages: 0
      Papers without PDF: 0
      ======================================
      ```
    - 耗时：~1分钟

---

## 阶段 2：AI 增强集成验证（P1）

### 简单操作验证（2-5分钟）

- [ ] 11. 测试 AI 增强流程兼容性
  - 需求：REQ-4.1, REQ-4.2, REQ-4.3
  - 文件：无需修改，仅验证
  - 验证：
    - 确保 `data/test-5.jsonl` 存在（来自任务 9）
    - 运行：
      ```powershell
      cd ai
      python enhance.py --data ../data/test-5.jsonl --max_workers 2
      ```
    - 等待完成（约 2-5 分钟，取决于 API 速度）
    - 验证输出文件存在：`data/test-5_AI_enhanced_Chinese.jsonl`
    - 验证脚本：
      ```python
      import json
      with open('data/test-5_AI_enhanced_Chinese.jsonl') as f:
          items = [json.loads(line) for line in f]
          assert len(items) == 5, f"Expected 5 items, got {len(items)}"
          for item in items:
              # 验证 AI 字段存在
              assert 'AI' in item, "Missing AI field"
              ai_data = item['AI']
              # 验证核心字段
              assert 'core_problem' in ai_data
              assert 'summary_core' in ai_data
              print(f"✓ {item['id']}: AI 增强成功")
      print("✅ AI 增强兼容性验证通过")
      ```
    - 耗时：2-5分钟

- [ ] 12. 测试 Markdown 转换兼容性
  - 需求：REQ-5.1, REQ-5.5
  - 文件：无需修改，仅验证
  - 验证：
    - 确保 `data/test-5_AI_enhanced_Chinese.jsonl` 存在（来自任务 11）
    - 运行：
      ```powershell
      cd to_md
      python convert.py --data ../data/test-5_AI_enhanced_Chinese.jsonl
      ```
    - 验证输出文件存在：`data/test-5.md`
    - 手动打开 `data/test-5.md`，检查：
      - ✓ 包含目录（Table of Contents）
      - ✓ 论文标题、作者、摘要可见
      - ✓ AI 增强字段正确渲染（大白话、核心价值等）
      - ✓ 格式整齐，无乱码
    - 耗时：~30秒

---

## 阶段 3：完整流程测试（P1）

### 状态验证（10-30分钟）

- [ ] 13. 完整爬取所有 NeurIPS 2024 Oral 论文
  - 需求：REQ-1 至 REQ-7（所有需求）
  - 文件：无新增，执行完整流程
  - 验证：
    - 运行：
      ```powershell
      cd daily_arxiv
      scrapy crawl neurips -o ../data/neurips-2024-oral.jsonl
      ```
    - 等待完成（预计 5-10 分钟，50-80 篇论文）
    - 检查统计信息：
      - ✓ `Total papers processed: 50+`
      - ✓ `Failed detail pages: < 5`（失败率 < 10%）
    - 手动抽查 3 篇论文数据质量：
      ```python
      import json, random
      with open('data/neurips-2024-oral.jsonl') as f:
          items = [json.loads(line) for line in f]
          samples = random.sample(items, 3)
          for item in samples:
              print(f"\n--- {item['id']} ---")
              print(f"Title: {item['title'][:80]}...")
              print(f"Authors: {item['authors'][:3]}...")
              print(f"PDF: {item['pdf']}")
      ```
    - 耗时：5-10分钟

- [ ] 14. 完整 AI 增强流程
  - 需求：REQ-4
  - 文件：无
  - 验证：
    - 运行：
      ```powershell
      cd ai
      python enhance.py --data ../data/neurips-2024-oral.jsonl --max_workers 10
      ```
    - 等待完成（预计 10-20 分钟，取决于论文数量和并发数）
    - 验证输出：`data/neurips-2024-oral_AI_enhanced_Chinese.jsonl`
    - 检查完成率：
      ```python
      import json
      with open('data/neurips-2024-oral_AI_enhanced_Chinese.jsonl') as f:
          items = [json.loads(line) for line in f]
          success = sum(1 for item in items if 'AI' in item and item['AI'].get('core_problem') != '问题提取失败')
          print(f"AI 增强成功率: {success}/{len(items)} ({success/len(items)*100:.1f}%)")
      ```
    - 耗时：10-20分钟

- [ ] 15. 生成最终 Markdown 文件
  - 需求：REQ-5
  - 文件：无
  - 验证：
    - 运行：
      ```powershell
      cd to_md
      python convert.py --data ../data/neurips-2024-oral_AI_enhanced_Chinese.jsonl
      ```
    - 验证输出：`data/neurips-2024-oral.md`
    - 手动打开检查：
      - ✓ 目录包含 "NeurIPS 2024 Oral"
      - ✓ 论文数量正确
      - ✓ 随机抽查 3 篇论文格式正确
    - 耗时：~30秒

---

## 阶段 4：发布与文档（P2）

### 简单操作验证（5-10分钟）

- [ ] 16. 更新项目 README
  - 需求：REQ-5.3
  - 文件：`README.md`
  - 实现：
    - 添加 NeurIPS 爬虫使用说明
    - 添加示例命令
  - 验证：
    - 打开 `README.md`，检查新增内容清晰可读
    - 耗时：< 1分钟

- [ ] 17. 验证 GitHub Pages 发布（手动）
  - 需求：REQ-5.4
  - 文件：无
  - 验证：
    - 提交并推送 `data/neurips-2024-oral.md` 到 GitHub
    - 等待 GitHub Actions 构建完成
    - 访问 GitHub Pages 网址
    - 检查：
      - ✓ NeurIPS 论文可见
      - ✓ 格式正确
      - ✓ 可以按来源筛选（如果实现了）
    - 耗时：5-10分钟（含等待构建）

---

## 阶段 5：代码优化与清理（P2）

### Console 验证（5-10分钟）

- [ ] 18. 添加代码注释和文档字符串
  - 需求：非功能性需求 - 可维护性
  - 文件：`daily_arxiv/daily_arxiv/spiders/neurips.py`
  - 实现：
    - 为每个方法添加文档字符串
    - 添加关键逻辑注释
  - 验证：
    - 运行 `python -m pydoc daily_arxiv.spiders.neurips` → 显示清晰的文档
    - 或在代码编辑器中查看方法提示
    - 耗时：< 1分钟

- [ ] 19. 清理测试文件
  - 需求：无
  - 文件：无
  - 实现：
    - 删除或移动测试文件到 `test/` 目录：
      - `data/test.jsonl`
      - `data/test-5.jsonl`
      - `data/test-5_AI_enhanced_Chinese.jsonl`
      - `data/test-5.md`
  - 验证：
    - `data/` 目录只保留最终输出：
      - `neurips-2024-oral.jsonl`
      - `neurips-2024-oral_AI_enhanced_Chinese.jsonl`
      - `neurips-2024-oral.md`
    - 耗时：< 1分钟

- [ ] 20. 创建便捷脚本（可选）
  - 需求：无（用户体验优化）
  - 文件：`run_neurips_crawler.ps1`（新增）
  - 实现：
    - 创建类似 `run_ai_enhance.ps1` 的便捷脚本
    - 自动执行：爬取 → AI 增强 → Markdown 转换
  - 验证：
    - 运行 `.\run_neurips_crawler.ps1`
    - 检查是否自动完成全流程
    - 耗时：10-30分钟（执行完整流程）

---

## 验收测试场景（对应需求文档）

### 场景 1：首次爬取 NeurIPS 2024 Oral
✅ 对应任务：9, 10, 11, 12, 13, 14, 15

### 场景 2：与 arXiv 爬虫并行
- [ ] 21. 测试并行运行（可选）
  - 需求：REQ-6.5
  - 验证：
    - 打开两个终端
    - 终端 1：`cd daily_arxiv && scrapy crawl arxiv -o test-arxiv.jsonl -s CLOSESPIDER_ITEMCOUNT=5`
    - 终端 2：`cd daily_arxiv && scrapy crawl neurips -o test-neurips.jsonl -s CLOSESPIDER_ITEMCOUNT=5`
    - 检查：
      - ✓ 两个爬虫都成功完成
      - ✓ 输出文件互不干扰
      - ✓ 无进程冲突错误
    - 耗时：~2分钟

### 场景 3：网络异常恢复
✅ 对应任务：7, 10（已内置错误处理）

---

## 任务统计

### 按优先级
- **P0（核心功能）**：任务 1-10（爬虫实现）
- **P1（集成测试）**：任务 11-15（AI 增强、Markdown、完整流程）
- **P2（文档与优化）**：任务 16-20（发布、清理）
- **可选**：任务 21（并行测试）

### 按验证时间
- **< 5秒**：任务 1, 2, 5
- **5-30秒**：任务 3, 4, 6, 7, 8, 12, 15, 16, 18, 19
- **1-5分钟**：任务 9, 10, 11, 17, 21
- **10-30分钟**：任务 13, 14, 20

### 预计总时间
- **核心实现（P0）**：1-2 小时
- **集成测试（P1）**：30 分钟 - 1 小时
- **文档与发布（P2）**：30 分钟
- **总计**：2-3.5 小时

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

### 验证脚本模板
所有验证脚本都可以保存为 `.py` 文件，方便重复运行：
```python
# verify_output.py
import json
import sys

def verify_jsonl(filepath, expected_count=None):
    with open(filepath) as f:
        items = [json.loads(line) for line in f]

    if expected_count and len(items) != expected_count:
        print(f"❌ Expected {expected_count} items, got {len(items)}")
        sys.exit(1)

    for item in items:
        # 添加验证逻辑...
        pass

    print(f"✅ All {len(items)} items validated")

if __name__ == "__main__":
    verify_jsonl('data/neurips-2024-oral.jsonl')
```
