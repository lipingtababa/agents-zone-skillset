# auto_qc - 自动质量检查

> 类型：Skill（自动触发）
> 版本：v1.0
> 创建日期：2026-01-11

---

## 何时自动使用

Main Agent 应在以下情况**自动应用**这个 skill：

### 触发场景 1：Tester 完成报告

当收到 tester subagent 的完成报告时：

**识别关键词**：
- "测试编写完成"、"✅ 测试编写完成"
- "tests written"、"testing complete"
- "已完成测试"、"测试已完成"

**识别特征**：
- 返回摘要包含测试文件列表
- 提到 "make test" 执行结果
- 提到覆盖的 Acceptance Criteria

### 触发场景 2：Coder 完成报告

当收到 coder subagent 的完成报告时：

**识别关键词**：
- "实现完成"、"✅ 实现完成"
- "implementation done"、"implementation complete"
- "已完成开发"、"开发已完成"

**识别特征**：
- 返回摘要包含实现文件列表
- 提到 "make test" 和 "make test-integration" 通过
- 提到满足 Definition of Done

### 不触发场景

**不要触发** auto_qc 的情况：
- Subagent 报告遇到阻塞/需要帮助
- Subagent 报告进度但未完成
- 用户只是询问进度或状态
- 用户手动运行 `/qc` 命令（手动命令独立执行）

---

## 执行逻辑

### Step 1: 识别完成阶段

根据完成报告内容，判断是哪个阶段完成：

```
如果包含"测试文件"、"测试执行结果" → Tester 阶段
如果包含"实现文件"、"Definition of Done" → Coder 阶段
```

### Step 2: 检测 Story 文件

按优先级自动检测 story 文件位置：

1. **检查最近使用的 story**
   - 查看对话历史，找到最近提到的 story 文件路径
   - 检查文件是否存在

2. **搜索当前项目的 stories 目录**
   - 查找 `stories/*.md` 或 `docs/stories/*.md`
   - 选择最新修改的 story 文件

3. **询问用户**（如果无法自动检测）
   ```
   无法自动检测 story 文件位置。请提供 story 文件路径：
   例如：stories/user-login.md
   ```

### Step 3: 调用 QC Skill

根据阶段类型，使用 `/qc` 命令的内部逻辑执行针对性质量检查：

**如果是 Tester 阶段**：
```bash
# 内部调用，等效于：
/qc <story-file> --phase=tester
```

**QC 执行内容（Tester 阶段）**：
- Phase 1: 提取 Claims 和 Requirements
- Phase 2: 验证 Tester 交付物
  - 假测试检测
  - 测试覆盖 acceptance criteria
  - 测试质量和断言
- Phase 4: 交叉验证（测试 vs 需求对齐）
- Phase 5: 生成验证报告（只包含 tester 部分）

**如果是 Coder 阶段**：
```bash
# 内部调用，等效于：
/qc <story-file> --phase=coder
```

**QC 执行内容（Coder 阶段）**：
- Phase 1: 提取 Claims 和 Requirements
- Phase 3: 验证 Coder 交付物
  - Placeholder 检测
  - 实现质量
  - 错误处理
- Phase 4: 交叉验证（实现 vs 测试对齐）
- Phase 5: 生成验证报告（只包含 coder 部分）
- Phase 6: 运行测试和 Linters
- Phase 7: Git 操作（通过后自动提交推送）

### Step 4: 处理 QC 结果

#### 4a. QC 通过

**如果是 Tester 阶段通过**：
```
✅ QC 检查通过

测试质量验证：
- ✅ 所有 Acceptance Criteria 已覆盖
- ✅ 无假测试
- ✅ 测试基于需求设计
- ✅ 测试正确失败（Red phase）

可以开始实现阶段。是否需要我调用 coder agent 开始实现？
```

**如果是 Coder 阶段通过**：
```
✅ QC 检查通过

代码质量验证：
- ✅ 无 placeholder
- ✅ 与 story 对齐
- ✅ 代码质量良好
- ✅ 所有测试通过

代码已自动提交并推送到远程仓库。
```

#### 4b. QC 失败

**构造详细的失败反馈**：

```
⚠️ QC 检查失败

发现以下问题：

[分类列出所有问题]

1. 缺失测试/实现：
   - AC #3 "用户输入无效邮箱时显示错误" 缺少对应测试

2. 假测试检测：
   - TestLogin_Success 疑似假测试（只检查函数被调用，未验证行为）

3. 代码质量问题：
   - internal/auth/login.go:45 - 发现 TODO 注释："TODO: add rate limiting"

4. Story 对齐问题：
   - AC #2 "登录失败3次后锁定账户" 未实现

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

请修复上述问题后重新报告完成。我会再次运行 QC 检查。
```

**阻塞流程**：
- 不允许进入下一阶段
- 等待 subagent 修复后重新报告
- 收到新的完成报告后，自动再次触发 QC

---

## 执行示例

### 示例 1：Tester 完成 → 自动 QC 通过

**用户对话**：
```
User: [调用 tester agent 编写测试]

Tester: ✅ 测试编写完成

测试文件：
- internal/auth/login_test.go (5 tests)
- internal/auth/register_test.go (3 tests)

测试执行结果：
--- FAIL: TestLogin_ValidCredentials (0.00s)
--- FAIL: TestLogin_InvalidPassword (0.00s)
...

覆盖的 Acceptance Criteria：
- AC #1: 用户可以使用邮箱和密码登录
- AC #2: 登录失败3次后锁定账户
```

**Main Agent 自动应用 auto_qc skill**：
```
收到 tester 完成报告，自动触发质量检查...

[运行 QC 检查]

✅ QC 检查通过

测试质量验证：
- ✅ 所有 Acceptance Criteria 已覆盖 (2/2)
- ✅ 无假测试
- ✅ 测试基于需求设计
- ✅ 测试正确失败（Red phase）

可以开始实现阶段。是否需要我调用 coder agent 开始实现？
```

### 示例 2：Coder 完成 → 自动 QC 失败 → 修复 → 通过

**第一次报告**：
```
Coder: ✅ 实现完成

实现文件：
- internal/auth/login.go
- internal/auth/session.go

测试结果：
✅ make test: PASS (8/8 tests)
✅ make test-integration: PASS (3/3 tests)
```

**Main Agent 自动应用 auto_qc skill（第一次）**：
```
收到 coder 完成报告，自动触发质量检查...

[运行 QC 检查]

⚠️ QC 检查失败

发现以下问题：

1. Placeholder 检测：
   - internal/auth/login.go:45 - 发现 TODO 注释："TODO: add rate limiting"

2. Story 对齐问题：
   - AC #2 "登录失败3次后锁定账户" 未实现

请修复上述问题后重新报告完成。
```

**Coder 修复后第二次报告**：
```
Coder: ✅ 实现完成（已修复）

修复内容：
- 实现了 rate limiting 功能
- 实现了账户锁定逻辑

测试结果：
✅ make test: PASS (10/10 tests)
✅ make test-integration: PASS (4/4 tests)
```

**Main Agent 自动应用 auto_qc skill（第二次）**：
```
收到 coder 完成报告，自动触发质量检查...

[运行 QC 检查]

✅ QC 检查通过

代码质量验证：
- ✅ 无 placeholder
- ✅ 与 story 对齐 (所有 AC 已实现)
- ✅ 代码质量良好
- ✅ 所有测试通过

正在提交代码...

[git add, commit, push]

代码已自动提交并推送到远程仓库。
```

---

## 与手动 /qc 的区别

| 特性 | auto_qc (自动) | /qc (手动) |
|------|----------------|------------|
| 触发方式 | Main Agent 自动识别 subagent 完成 | 用户显式调用 |
| 触发时机 | Tester/Coder 报告完成时 | 任何时候 |
| Story 检测 | 自动检测 | 用户提供或自动检测 |
| 失败处理 | 阻塞流程，要求修复 | 报告问题，由用户决定 |
| 成功处理 | 自动进入下一阶段/提交 | 报告通过，由用户决定 |

**兼容性**：
- auto_qc 和 /qc 可以共存
- 用户随时可以手动运行 /qc 进行检查
- 自动触发不影响手动命令

---

## 注意事项

1. **依赖现有 QC 实现**
   - auto_qc 调用 `~/.claude/skills/qc.md` 的逻辑
   - 不重复实现检查逻辑，保持一致性

2. **Story 文件检测**
   - 优先使用对话历史中的 story 路径
   - 自动搜索项目 stories 目录
   - 无法检测时询问用户

3. **阻塞流程严格执行**
   - QC 失败时明确要求修复
   - 不允许跳过或忽略问题
   - 保持质量标准

4. **清晰的反馈**
   - 分类列出所有问题
   - 提供具体的文件位置和行号
   - 给出明确的修复建议

5. **避免误触发**
   - 仔细识别完成报告的关键词
   - 排除进度更新、求助、询问等场景
   - 确保只在真正完成时触发

---

## 相关文档

- `~/.claude/commands/qc.md` - QC 命令用户文档
- `~/.claude/skills/qc.md` - QC Skill 实现指南
- `~/.claude/agents/tester.md` - Tester Subagent 指南
- `~/.claude/agents/coder.md` - Coder Subagent 指南
- `~/.claude/CLAUDE.md` - 全局工作流指南

---

_Created for CC_COLLABORATION Framework Integration v1.0_
