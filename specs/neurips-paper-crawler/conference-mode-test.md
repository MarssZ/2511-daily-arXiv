# Conference Papers Mode - 测试清单

> 在推送到GitHub前完成本地测试

---

## 🧪 本地测试

### 1. 启动本地服务器

```bash
cd E:\MarssPython\2511-daily-arXiv
python -m http.server 8000
```

访问: http://localhost:8000

---

## ✅ 功能测试清单

### 基础UI测试

- [ ] **View Mode Toggle显示正常**
  - [ ] 看到 `[📅 Daily]` 和 `[🏆 Conference]` 两个按钮
  - [ ] Daily按钮默认高亮（紫色渐变背景）
  - [ ] 鼠标悬停有hover效果

- [ ] **Daily Mode（默认模式）**
  - [ ] 显示日期选择器
  - [ ] Conference选择器隐藏
  - [ ] 显示Daily Papers数据

- [ ] **切换到Conference Mode**
  - [ ] 点击 `[🏆 Conference]` 按钮
  - [ ] 按钮切换为高亮状态
  - [ ] Daily选择器隐藏
  - [ ] Conference选择器显示

---

### Conference Selector测试

- [ ] **Conference Selector显示**
  - [ ] 显示 "NeurIPS 2024 Oral (Test)" 或 "Select Conference"
  - [ ] 右侧有下拉箭头图标
  - [ ] 鼠标悬停有边框高亮效果

- [ ] **Conference Picker Modal**
  - [ ] 点击Conference Selector打开弹窗
  - [ ] 弹窗居中显示，带半透明背景
  - [ ] 看到会议列表卡片

---

### Conference List测试

- [ ] **会议卡片内容**
  - [ ] 显示会议名称: "NeurIPS 2024 Oral (Test)"
  - [ ] 显示论文数量: "6 papers"
  - [ ] 显示日期: "📅 2024-12-15"
  - [ ] 显示类别: "🏷️ oral"
  - [ ] 显示年份: "📖 Year: 2024"
  - [ ] 显示描述文本

- [ ] **交互效果**
  - [ ] 鼠标悬停卡片有阴影和上移效果
  - [ ] 点击卡片加载论文
  - [ ] 弹窗自动关闭

---

### 论文加载测试

- [ ] **加载流程**
  - [ ] 显示Loading动画
  - [ ] Console无错误信息
  - [ ] 成功加载6篇NeurIPS测试论文

- [ ] **论文展示**
  - [ ] 论文卡片正常显示
  - [ ] 标题、作者、摘要完整
  - [ ] AI增强字段（TLDR、动机等）正常显示
  - [ ] 点击卡片打开详情弹窗

- [ ] **过滤功能**
  - [ ] Category过滤正常工作
  - [ ] 关键词过滤正常工作
  - [ ] 文本搜索正常工作

---

### 模式切换测试

- [ ] **Daily ↔ Conference切换**
  - [ ] 从Conference切回Daily模式
  - [ ] 日期选择器恢复显示
  - [ ] Daily Papers正常加载
  - [ ] 再次切换到Conference，记住上次选择的会议

- [ ] **浏览器刷新**
  - [ ] 刷新页面后默认显示Daily模式
  - [ ] 状态不丢失

---

### 错误处理测试

- [ ] **空会议列表**
  - [ ] 临时清空 `conference-list.json` 的 conferences 数组
  - [ ] 切换到Conference模式
  - [ ] 显示 "No conferences available" 提示

- [ ] **文件不存在**
  - [ ] 修改conference-list.json中的file字段为不存在的文件
  - [ ] 尝试加载会议
  - [ ] 显示错误提示和文件路径

- [ ] **JSON格式错误**
  - [ ] 临时破坏conference-list.json的JSON格式
  - [ ] 刷新页面
  - [ ] Console显示解析错误
  - [ ] 恢复JSON格式，功能恢复正常

---

### 响应式测试（可选）

- [ ] **移动端（宽度<768px）**
  - [ ] Mode按钮文字隐藏，只显示图标
  - [ ] Conference选择器宽度缩小
  - [ ] 弹窗宽度适配屏幕（95%）
  - [ ] 会议卡片meta信息垂直排列

- [ ] **桌面端（宽度≥768px）**
  - [ ] 所有元素正常显示
  - [ ] 弹窗最大宽度600px

---

## 🐛 已知问题检查

- [ ] **Console错误**
  - [ ] 打开DevTools Console
  - [ ] 无红色错误信息
  - [ ] 看到 "Loaded 1 conferences" 日志
  - [ ] 看到 "Loaded 6 papers from..." 日志

- [ ] **网络请求**
  - [ ] Network面板查看请求
  - [ ] `assets/conference-list.json` 200 OK
  - [ ] `data/2025-11-09_AI_enhanced_Chinese.jsonl` 200 OK

- [ ] **兼容性**
  - [ ] Chrome/Edge测试
  - [ ] Firefox测试（可选）
  - [ ] Safari测试（如有Mac）

---

## 📊 测试数据验证

### 测试论文数据检查

打开DevTools Console，运行:

```javascript
// 查看加载的会议
console.log('Conference List:', conferenceList);

// 查看当前会议
console.log('Current Conference:', currentConference);

// 查看加载的论文
console.log('Papers:', currentFilteredPapers);
console.log('Paper count:', currentFilteredPapers.length); // 应该是6
```

预期输出:
```
Conference List: [{id: "neurips2024_oral_test", name: "NeurIPS 2024 Oral (Test)", ...}]
Current Conference: {id: "neurips2024_oral_test", ...}
Papers: (6) [{...}, {...}, ...]
Paper count: 6
```

---

## 🎯 部署前检查

- [ ] **代码提交**
  - [ ] 所有改动已git add
  - [ ] commit message清晰描述功能

- [ ] **文件确认**
  - [ ] `assets/conference-list.json` 存在且有效
  - [ ] `data/2025-11-09_AI_enhanced_Chinese.jsonl` 存在（6篇论文）
  - [ ] `js/conference.js` 存在
  - [ ] `index.html` 引入了conference.js
  - [ ] `css/styles.css` 包含Conference样式

- [ ] **GitHub Actions兼容**
  - [ ] 确认workflow不需要修改
  - [ ] assets/和js/文件会自动部署
  - [ ] conference-list.json会被推送到仓库

---

## 🚀 GitHub Pages验证（部署后）

推送后等待GitHub Actions构建完成（~2-5分钟），然后:

- [ ] **访问GitHub Pages URL**
  - [ ] https://你的用户名.github.io/2511-daily-arXiv/

- [ ] **Conference模式测试**
  - [ ] 切换到Conference模式
  - [ ] 能看到NeurIPS 2024 Oral (Test)
  - [ ] 加载论文成功
  - [ ] 论文内容与本地一致

- [ ] **跨设备测试**
  - [ ] 手机浏览器测试
  - [ ] 平板测试（如有）

---

## 📝 测试结果记录

| 测试项 | 状态 | 备注 |
|--------|------|------|
| View Mode Toggle | ⬜ 待测 | |
| Conference Selector | ⬜ 待测 | |
| Conference Picker | ⬜ 待测 | |
| 论文加载 | ⬜ 待测 | |
| 过滤功能 | ⬜ 待测 | |
| 模式切换 | ⬜ 待测 | |
| 错误处理 | ⬜ 待测 | |
| 响应式 | ⬜ 待测 | |
| GitHub Pages | ⬜ 待测 | 需部署后测试 |

---

**测试完成后**:
- ✅ 所有核心功能通过 → 可以推送到GitHub
- ⚠️ 发现问题 → 记录到此文档，修复后重新测试
- ℹ️ 非阻塞性问题 → 创建Issue，计划后续优化

---

*最后更新：2025-11-09*
