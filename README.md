# Agents Zone Skillset

> **这是一套从生产环境中提取的参考实现。** 不是教程，不是玩具 — 这些是一个真实开发团队每天用来编排 TDD、质量控制和 CI/CD 自愈的实际文件。拿去用，根据你的项目改，在实践中演化它们。

配套 [Harness Engineering Playbook](https://github.com/lipingtababa/harness-engineering-playbook)，适用于 [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview)。Playbook 讲 **为什么** — 闭环验证、规格驱动开发、对抗式质检。这个仓库给你 **怎么做**。

---

## 团队：角色与协作方式

这套 Skillset 定义了一个小型的 AI 角色团队。每个角色职责清晰，通过严格的交接协议和质量关卡进行协作。

### 角色一览

**产品经理 (Product Owner)** — `skills/prd.md`
把产品想法翻译成结构化的 PRD（产品需求文档）。问澄清问题、调研基础设施约束、区分 MVP 与后续阶段。产出 `PRD.md` — 下游所有工作的 "做什么和为什么"。

**架构师 (Architect)** — `skills/architect.md`
拿到 PRD，设计技术架构：组件图、API 设计、数据流、部署策略。产出 `ARCHITECTURE.md` — 连接需求和实现的 "怎么做"。会对照真实代码库验证模式，而不是凭空发明。

**故事编写者 (Story Writer)** — `skills/story.md`
把 PRD + 架构转化为超详细的开发故事。每个故事是一个自包含的任务包：验收标准、测试场景、精确的文件路径、工具引用、反模式。故事文件是**唯一信息源** — Tester 和 Coder 只看这个文件。

**测试员 (Tester)** — `agents/tester.md`
TDD 红灯阶段。读故事，写失败的测试。关键设计：测试从**需求**出发，不从实现代码出发。这是刻意为之 — 防止 [共谋问题](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/03b-collusion.md)，即 AI 写出的测试只是确认代码碰巧在做什么。测试员验证所有测试都失败（因为功能还不存在），然后交接。

**编码员 (Coder)** — `agents/coder.md`
TDD 绿灯阶段。读同一个故事加失败的测试，然后实现代码让测试通过。遵循故事中的技术上下文模式。有 3 次迭代上限 — 如果 3 次尝试后测试仍然失败，停下来汇报阻塞，而不是无限循环。

**质检审计员 (QC Auditor)** — `skills/qc.md`
对抗式验证者。不信任任何人的声明。当测试员说 "所有 AC 已覆盖"，QC 去读实际测试代码检查。当编码员说 "所有测试通过"，QC 去跑测试。抓假测试（无论实现如何都会通过的测试）、缺失覆盖、占位符代码（`TODO`、`NotImplemented`）、以及声明与现实的不匹配。这是 [Agent 验证 Agent](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/03e-adversarial-verification.md) 模式的实践。

**自动质检触发器 (Auto-QC Trigger)** — `skills/auto_qc.md`
监听子 Agent 的完成报告，自动触发 QC。当测试员或编码员报告 "完成"，Auto-QC 检测到它，跑相应的检查，如果质量关卡失败就阻止流程继续。无需手动调用 `/qc`。

**CI/CD 自愈器 (CI/CD Healer)** — `skills/follow.md`
Push 后监控 GitHub Actions。当检查失败，下载日志、分类故障（lint、测试、构建、部署）、修复、本地验证、Push、再等 CI。最多 2 次迭代 — 如果同一个错误持续存在，停下来给出详细的根因分析和建议的手动修复方案。

**指挥家 (Conductor)** — `skills/conduct.md`
编排者。读 `PROGRESS.md` 知道项目上次停在哪，验证下一阶段的前置条件，执行它（启动相应的 Skill 或子 Agent），更新进度，继续前进。支持自主完成整个故事 — 你可以输入 `/conduct` 然后走开。它会自动跑 Tester → QC → Coder → QC → Commit → Push → CI 监控，每一步都不需要你的许可。

**环境搭建 (Environment Setup)** — `skills/setup.md`
准备开发环境：Git Worktree 用于并行开发、依赖验证、构建检查。可选 — 很多开发者跳过这步直接在主仓库工作。

**HR（人力资源）** — `skills/hr.md`
团队能力的守护者。详见下方专题。

### 协作流程

```
         你
          |
          | "加一个用户认证功能"
          v
    +-----------+
    | 产品经理   | -- 调研、提问、产出 PRD.md
    +-----------+
          | PRD.md
          v
    +-----------+
    |  架构师    | -- 设计组件、数据流、产出 ARCHITECTURE.md
    +-----------+
          | ARCHITECTURE.md
          v
    +-----------+
    |  故事      | -- 创建自包含的任务包：AC、测试计划、文件路径
    |  编写者    |
    +-----------+
          | story.md（唯一信息源）
          |
    +=============================================+
    |  指挥家 (CONDUCTOR) 编排以下所有环节          |
    +=============================================+
          |
          v
    +-----------+     story.md
    |  测试员    | <------------ 从需求出发，不看实现
    |  (红灯)    |
    +-----------+
          | 失败的测试
          v
    +-----------+
    | 质检审计员  | -- 这些是真测试吗？覆盖了所有 AC 吗？
    +-----------+
          | 通过（或打回测试员）
          v
    +-----------+     story.md + 失败的测试
    |  编码员    | <------------ 实现代码让测试通过
    |  (绿灯)    |
    +-----------+
          | 通过的代码
          v
    +-----------+
    | 质检审计员  | -- 有占位符？有假通过？匹配故事吗？
    +-----------+
          | 通过（或打回编码员）
          v
    +-----------+
    |  CI/CD     | -- Push、监控 GitHub Actions、自动修复失败
    |  自愈器    |
    +-----------+
          |
          v
       完成
```

**核心设计原则：**

1. **信息单向流动** — 每个角色读上一个角色的产出，不回头找上游
2. **QC 卡在每个交接点** — 没有对抗式验证，什么都不能往前走
3. **故事文件是唯一信息源** — 测试员和编码员只看故事，防止上下文漂移
4. **失败循环有界** — 编码员最多 3 次迭代，CI 自愈器最多 2 次，然后停下来汇报
5. **指挥家管理状态** — `PROGRESS.md` 跨会话存活，随时可以从上次的地方继续

---

## HR：整个 Skill System 的灵魂

HR（Human Resources）不是修代码的 — 它是**发展团队能力的**。当有人产出了糟糕的结果，HR 问的是 "缺了什么指导"，而不是 "谁搞砸了"。

这是这套系统最关键的设计：**Agent 和 Skill 的质量决定了所有产出的上限。** 如果测试员的指导文档没有教它检查现有 Fixture，它每次都会创建重复的 Fixture。如果编码员的文档没有说 "先查看已有的工具函数"，它每次都会重新发明轮子。HR 的工作就是确保这些指导文档始终完整、准确、没有冗余。

### 为什么 HR 是灵魂？

其他角色解决的是 "当前这个功能怎么做好"。HR 解决的是 "团队怎么越来越好"。

想象一下：你发现编码员把业务逻辑写进了架构文档。你可以手动修复那个文档，但下次它还会犯同样的错。HR 的做法不同：

1. **查历史** — 去翻会话日志，看当时发生了什么
2. **找根因** — 哪个 Agent 或 Skill 在执行？它的指导文档缺了什么？
3. **补漏洞** — 把教训嵌入到正确的文档中，确保下次不再犯

这就是从 "修一个 bug" 到 "消灭一类 bug" 的区别。

### 命令

```bash
/hr <教训>                      # 把教训嵌入到相关的 Agent/Skill 文档中
/hr audit                       # 对所有 Agent 和 Skill 做一次全面质量审计
/hr audit <文件>                 # 审计某个特定的 Agent 或 Skill 文件
/hr dedup                       # 查找跨文件的重复内容
/hr dedup --fix                 # 查找重复并提出修复方案
/hr list                        # 列出所有发现的 Agent 和 Skill
```

### 三大核心能力

#### 能力一：问题调查与教训路由

当问题出现时（代码放错地方、输出质量差、工作流断裂），HR **不直接修复产物**。产物是症状，HR 修的是团队。

**调查流程：**

1. **查历史** — 检查 `.claude` 的会话记录，看问题是怎么产生的
2. **读文档** — 读所有相关的 Agent 和 Skill 文件，找出哪个文件本应防止这个问题
3. **问** — 哪个 Agent 或 Skill 在事发时是活跃的？它遵循的是什么指导？缺了什么？
4. **定位漏洞** — 一条缺失的规则、一个模糊的边界、一个默认的假设
5. **路由教训** — 把教训嵌入正确的文件，填补漏洞

**实际例子：**

```
你: /hr 永远不要在架构文档里写代码片段，代码属于实现

HR:
  调查: 检查了 architect.md 的当前指导...
  发现: 架构师文档没有明确禁止代码片段

  教训路由完成

  目标发现: 11 个文件
  路由到: 2 个文件
  - skills/architect.md (HIGH)
    - 章节: "产出规范"
    - 变更: 添加了 "架构文档不包含代码片段" 规则
  - skills/prd.md (MEDIUM)
    - 章节: "PRD 范围"
    - 变更: 强化了 "PRD 只关注产品/业务，代码属于技术文档" 的规则
  跳过: tester.md, coder.md, qc.md... (不相关)
```

**相关性评分：**

| 评分 | 标准 | 动作 |
|------|------|------|
| HIGH | 关键词匹配目标描述，角色被明确提及 | 必须路由 |
| MEDIUM | 部分重叠，跨领域关注点 | 如果适用则路由 |
| LOW/NO | 无关键词重叠，不同关注领域 | 跳过 |

#### 能力二：质量审计

检查 Agent/Skill 文件的质量问题。审计不是挑毛病 — 是发现那些会降低团队效能的系统性问题。

**审计清单：**

| 维度 | 检查项 |
|------|--------|
| **内容质量** | 单一职责、无过期引用、无过期示例、Agent 花名册准确、无硬编码路径 |
| **重复** | 文件内无重复内容、无跨文件复制粘贴、样板代码最小化 |
| **精简** | Agent < 15KB / Skill < 20KB、无死章节、示例有存在价值 |
| **一致性** | 与 CLAUDE.md 一致、同行文件不冲突、术语统一、模型引用最新 |
| **正确性** | Frontmatter 完整有效、引用的工具存在、工作流与现实匹配 |

**严重级别：**

| 级别 | 含义 | 示例 |
|------|------|------|
| CRITICAL | 积极误导或已失效 | 引用了被删除的文件、错误的工作流 |
| HIGH | 严重浪费或混淆 | 175 行重复的中英文内容 |
| MEDIUM | 可维护性问题 | 同一段样板出现在 3 个文件中 |
| LOW | 轻微改进机会 | 稍显过时的示例 |

**审计报告示例：**

```
审计完成: 11 个文件已扫描

CRITICAL (1):
- skills/architect.md: 引用了不存在的 skills/deploy.md (第 45 行)

HIGH (2):
- agents/tester.md: Git 工作流样板与 coder.md 重复 (共 35 行)
- skills/qc.md: 对 Auto-QC 的描述与 auto_qc.md 冲突

MEDIUM (3):
- agents/coder.md: 工作目录说明与 tester.md 重复
- skills/conduct.md: Worktree 命名约定与 setup.md 重复
- skills/follow.md: 选择性 git add 规则与 conduct.md 重复

建议动作:
1. 修复 architect.md 的过期引用 -- 解决 1 个 CRITICAL
2. 把 Git 工作流样板提取到 CLAUDE.md -- 解决 2 个 HIGH + 3 个 MEDIUM
```

#### 能力三：去重

查找跨 Agent 和 Skill 文件的重复内容，提出整合方案。

**常见重复模式：**

| 模式 | 出现位置 | 修复方法 |
|------|---------|---------|
| 项目根路径 | coder, tester | 每个 Agent 一句话声明，不重复 |
| 完成/QC 流程 | coder, tester | 保留在一个地方，其他引用 |
| 选择性 git add 规则 | ship（权威） | 其他引用 ship |
| 调试指南 | troubleshooter（权威） | coder 和 tester 引用它 |
| 测试质量标准 | qc（权威） | tester 引用它 |

**权威文件选择原则：**

当同一内容出现在多个地方，权威归属选：
- **概念所有者** — 该概念是这个文件的核心职责
- **最完整版本** — 最丰富的处理
- **最多被引用** — 其他文件已经指向它

其他文件引用，不复制。

### HR 不做什么

- **不修产物** — 如果 architecture.md 里有代码，HR 不去改 architecture.md。用户或架构师去修产物。HR 修团队。
- **不打补丁** — 添加一条规则来防止某个特定的错误太狭隘了。要识别错误的类别，写出覆盖这一类错误的指导。
- **不无证据行动** — 在得出结论之前先读历史和文件。不假设你知道发生了什么。

### 核心原则

- **教，不说教** — 教训应该是简洁的增补，不是长篇大论
- **权威归属** — 每个概念有一个家，其他地方引用它
- **带着同理心审计** — 文件是有机增长的，严重性反映的是影响而不是责备
- **修重要的** — 175 行重复是 CRITICAL，一行重复的话是噪音

---

## 快速开始

### 1. 复制到你的 Claude Code 配置

```bash
# 克隆
git clone https://github.com/lipingtababa/agents-zone-skillset.git

# 复制你需要的
cp -r agents-zone-skillset/agents/ ~/.claude/agents/
cp -r agents-zone-skillset/skills/ ~/.claude/skills/
cp -r agents-zone-skillset/templates/ ~/.claude/templates/
cp -r agents-zone-skillset/hooks/ ~/.claude/hooks/
```

### 2. 在你的 CLAUDE.md 中引用

```markdown
## 开发工作流

遵循 TDD 工作流 — 写测试在先，实现代码在后。

### Agents
- **Tester**: `~/.claude/agents/tester.md` — 从故事中写失败的测试
- **Coder**: `~/.claude/agents/coder.md` — 实现代码让测试通过

### 质量控制
- Tester/Coder 完成后运行 `/qc`
- Auto-QC 在子 Agent 完成时自动触发

### 工作流编排
- 运行 `/conduct` 自动执行下一阶段
- PROGRESS.md 跨会话跟踪状态

### 团队管理
- 运行 `/hr <教训>` 把教训嵌入 Agent/Skill 文档
- 运行 `/hr audit` 审计所有文档质量
```

### 3. 替换占位符

文件使用 `[方括号占位符]` 表示项目特定值：

| 占位符 | 替换为 | 示例 |
|--------|--------|------|
| `[project-root]` | 你的项目目录 | `~/myproject` |
| `[service]` | 你的服务名 | `api`, `web`, `worker` |
| `[your-org]` | 你的 GitHub 组织 | `mycompany` |
| `[your-domain]` | 你的部署域名 | `myapp.com` |
| `[shared-lib]` | 你的共享库路径 | `lib/`, `packages/shared/` |
| `[reference-app]` | 一个参考实现 | `apps/example/` |
| `[infrastructure-repo]` | 你的基础设施仓库 | `terraform/`, `infra/` |

---

## 使用示例

### 从零开始做一个完整功能

```
你: /prd "加 JWT 用户认证"

Claude: [调研需求、问澄清问题、产出 PRD.md]

你: /architect

Claude: [读 PRD、设计架构和组件图、产出 ARCHITECTURE.md]

你: /story

Claude: [创建超详细的开发故事：AC、测试场景、文件路径]

你: /conduct

Claude: [自动编排整个流水线]
  1. 启动测试员 → 写失败的测试（红灯阶段）
  2. Auto-QC 验证测试质量 → 通过
  3. 启动编码员 → 实现代码（绿灯阶段）
  4. Auto-QC 验证实现 → 通过
  5. 提交、Push、监控 CI → 全绿
```

### 修复失败的 CI

```
你: /follow

Claude:
  发现: 3 个 lint 错误, 1 个测试失败

  迭代 1:
  - 修复 lint: golangci-lint --fix
  - 修复测试: handler 缺少 nil 检查
  - 本地验证: 全部通过
  - Push 修复提交
  - 等待 CI... 全绿！
```

### 审计已完成工作的质量

```
你: /qc stories/user-auth.md --phase=both

Claude:
  测试员声明:
  - "测试覆盖了认证" → 已验证（测试了 200 和 401）
  - "测试覆盖了限流" → 假测试（只测试了成功场景）

  编码员声明:
  - "实现了 JWT 验证" → 已验证
  - "加了错误处理" → 部分（缺少超时处理）

  必须修复:
  1. 修复假的限流测试（循环验证）
  2. 添加超时错误处理
```

### 教团队一个教训

```
你: /hr 创建新 Fixture 之前永远先检查是否已有现成的

Claude:
  教训路由完成

  目标发现: 11 个文件
  路由到: 2 个文件
  - agents/tester.md (HIGH) — 嵌入 "步骤 2：写测试"
  - agents/coder.md (MEDIUM) — 嵌入 "实现标准"
  跳过: architect.md, prd.md（不相关）
```

### 审计团队文档质量

```
你: /hr audit

Claude:
  审计完成: 11 个文件已扫描

  CRITICAL (1):
  - skills/follow.md: 引用了已删除的 deploy.sh 脚本

  HIGH (1):
  - agents/tester.md: 调试章节与 coder.md 重复 42 行

  MEDIUM (2):
  - skills/conduct.md: Worktree 命名约定与 setup.md 重复
  - agents/coder.md: 工作目录样板与 tester.md 重复

  建议动作:
  1. 更新 follow.md 的脚本引用 -- 解决 1 个 CRITICAL
  2. 调试指南保留在 coder.md，tester.md 改为引用 -- 解决 1 个 HIGH
```

### 跨会话恢复进度

```
你: /conduct

Claude: [读取 PROGRESS.md]
  功能: 用户认证
  阶段: 实现（测试 已完成）
  下一步: 启动编码员子 Agent

  执行实现阶段...
```

---

## 文件参考

### Agents

| 文件 | 角色 | 描述 |
|------|------|------|
| [`agents/tester.md`](agents/tester.md) | 测试员 | TDD 红灯阶段。从故事需求写失败的测试。从 AC 设计，不看实现。 |
| [`agents/coder.md`](agents/coder.md) | 编码员 | TDD 绿灯阶段。实现代码让测试通过。3 次迭代上限，超出则汇报阻塞。 |

### Skills

| 文件 | 角色 | 描述 |
|------|------|------|
| [`skills/prd.md`](skills/prd.md) | 产品经理 | 调研优先的 PRD 创建。先验证假设再记录。MVP 分阶段。 |
| [`skills/architect.md`](skills/architect.md) | 架构师 | 把 PRD 转化为技术架构。对照真实代码库模式验证。 |
| [`skills/story.md`](skills/story.md) | 故事编写者 | 创建自包含的开发故事。Tester/Coder 的唯一信息源。 |
| [`skills/qc.md`](skills/qc.md) | 质检审计员 | 对抗式验证。读实际代码验证声明。抓假测试、占位符、缺失覆盖。 |
| [`skills/auto_qc.md`](skills/auto_qc.md) | 自动质检触发器 | 检测子 Agent 完成报告，自动触发 QC。失败则阻止流程。 |
| [`skills/follow.md`](skills/follow.md) | CI/CD 自愈器 | 自动修复 GitHub Actions 失败。下载日志、分类、修复、本地验证、Push。最多 2 次迭代。 |
| [`skills/conduct.md`](skills/conduct.md) | 指挥家 | 从 PROGRESS.md 编排完整工作流。自主完成整个故事。 |
| [`skills/setup.md`](skills/setup.md) | 环境搭建 | Git Worktree、依赖验证、环境就绪检查。 |
| [`skills/hr.md`](skills/hr.md) | HR | 团队能力管理。嵌入教训、审计质量、去重。整个系统的灵魂。 |

### Templates

| 文件 | 描述 |
|------|------|
| [`templates/architecture.md`](templates/architecture.md) | 14 节架构文档脚手架 |
| [`templates/prd.md`](templates/prd.md) | MVP 分阶段 PRD 模板 |
| [`templates/progress.md`](templates/progress.md) | 跨会话进度追踪器 |

### Hooks

| 文件 | 描述 |
|------|------|
| [`hooks/validate-git.py`](hooks/validate-git.py) | 阻止 `git add .` 和 `git add -A`，防止意外提交敏感文件 |

---

## 与 Playbook 的映射

| Playbook 概念 | 本仓库的实现 |
|---------------|-------------|
| [规格](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/02-specification.md) | `prd` + `architect` + `story` Skills + Templates |
| [测试优先验证](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/03a-test-first.md) | Tester Agent（红灯在绿灯之前） |
| [防共谋](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/03b-collusion.md) | 测试员从需求设计，不从实现设计 |
| [对抗式验证](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/03e-adversarial-verification.md) | QC 审计员用证据验证声明 |
| [持续反馈](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/03d-continuous-feedback.md) | Auto-QC + CI/CD 自愈器 |
| [任务分解](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/04b-task-decomposition.md) | Story Writer 把功能拆成有界的任务 |
| [上下文工程](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/04c-context-engineering.md) | 故事文件作为唯一信息源 |
| [记忆工程](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/04d-memory.md) | PROGRESS.md + Conductor 的跨会话状态 |
| [隐性知识](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/02d-tacit-knowledge.md) | HR 把教训嵌入文档 |
| [放手](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/04e-letting-go.md) | Conductor 自主运行完整故事 |

---

## 贡献

发现了 bug？有更好的模式？欢迎 PR。

- 保持文件自包含 — 每个 Agent/Skill 独立工作
- 用 `[方括号占位符]` 表示项目特定值
- 提交前用 Claude Code 测试

## 许可证

MIT
