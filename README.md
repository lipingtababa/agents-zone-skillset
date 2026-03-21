# Agents Zone Skillset

> **This is a reference implementation.** These are real agents, skills, and commands extracted from a production development team's daily workflow. They are not tutorials or toy examples — they are the actual files that orchestrate TDD, quality control, and CI/CD healing in a working codebase. Use them as a starting point, adapt them to your project, and evolve them as you learn what works for your team.

A companion to the [Harness Engineering Playbook](https://github.com/lipingtababa/harness-engineering-playbook) for [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview). The playbook explains **why** — closed-loop verification, specification-driven development, adversarial QC. This repo provides the **how**.

---

## The Team: Roles and How They Work Together

This skillset defines a small, specialised team of AI roles. Each role has a clear responsibility, and they collaborate through a strict handoff protocol with quality gates at every boundary.

### The Roles

**Product Owner** — `/prd` command
Translates a product idea into a structured PRD (Product Requirements Document). Asks clarifying questions, researches infrastructure constraints, separates MVP from future phases. Produces `PRD.md` — the "what and why" that everything downstream depends on.

**Architect** — `/architect` command
Takes the PRD and designs the technical architecture: component diagrams, API design, data flows, deployment strategy. Produces `ARCHITECTURE.md` — the "how" that bridges requirements to implementation. Verifies patterns against the actual codebase rather than inventing new ones.

**Story Writer** — `/story` command
Transforms PRD + Architecture into hyper-detailed developer stories. Each story is a self-contained briefing pack: acceptance criteria, test scenarios, exact file paths, utility references, anti-patterns. The story file is the **single source of truth** — tester and coder will read nothing else.

**Tester** — `agents/tester.md`
TDD Red phase. Reads the story and writes failing tests. Critically, the tester designs tests from **requirements**, not from implementation code. This is deliberate — it prevents the [collusion problem](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/03b-collusion.md) where AI writes tests that merely confirm what the code happens to do. The tester verifies that all tests fail (because the feature doesn't exist yet), then hands off.

**Coder** — `agents/coder.md`
TDD Green phase. Reads the same story plus the failing tests, then implements code to make them pass. Follows patterns from the story's technical context. Has a 3-iteration limit — if tests still fail after 3 attempts, it stops and reports the blockage rather than spiralling.

**QC Auditor** — `skills/qc.md`
The adversarial verifier. Doesn't trust anyone's claims. When the tester says "all AC covered", QC reads the actual test code and checks. When the coder says "all tests pass", QC runs them. Catches fake tests (tests that pass regardless of implementation), missing coverage, placeholder code (`TODO`, `NotImplemented`), and mismatches between claims and reality. This is the [agent-verifies-agent](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/03e-adversarial-verification.md) pattern in action.

**CI/CD Healer** — `skills/follow.md`
Monitors GitHub Actions after a push. When checks fail, it downloads logs, categorises failures (lint, test, build, deploy), applies fixes, validates locally, pushes, and waits for CI again. Max 2 iterations — if the same error persists, it stops with a detailed root cause analysis and suggested manual fix. Saves 50-60% of the time developers spend on CI failures.

**Conductor** — `commands/conduct.md`
The orchestrator. Reads `PROGRESS.md` to know where the project left off, validates prerequisites for the next phase, executes it (launching the appropriate command or subagent), updates progress, and moves on. Enables autonomous story completion — you can type `/conduct` and walk away. It will run tester → QC → coder → QC → commit → push → CI monitoring without asking for permission at each step.

**Mentor** — `commands/mentor.md`
The knowledge propagator. When you discover a lesson ("always check for existing fixtures before creating new ones"), the mentor analyses which agents/commands would benefit, finds the right section in each file, and embeds the lesson organically — matching the document's tone and structure. This is how the team learns and improves over time.

### How They Collaborate

```
         YOU
          │
          │ "Add user authentication"
          ▼
    ┌───────────┐
    │  Product   │ ── Researches, asks questions, produces PRD.md
    │  Owner     │
    └─────┬─────┘
          │ PRD.md
          ▼
    ┌───────────┐
    │ Architect  │ ── Designs components, data flow, produces ARCHITECTURE.md
    └─────┬─────┘
          │ ARCHITECTURE.md
          ▼
    ┌───────────┐
    │  Story     │ ── Creates self-contained briefing: AC, test plan, file paths
    │  Writer    │
    └─────┬─────┘
          │ story.md (single source of truth)
          │
    ╔═════╧═══════════════════════════════════════╗
    ║  CONDUCTOR orchestrates everything below     ║
    ╚═════╤═══════════════════════════════════════╝
          │
          ▼
    ┌───────────┐     story.md
    │  Tester    │ ◄──────────── reads requirements, NOT implementation
    │ (Red)      │
    └─────┬─────┘
          │ failing tests
          ▼
    ┌───────────┐
    │ QC Auditor │ ── Are these REAL tests? Do they cover all AC?
    └─────┬─────┘
          │ ✅ pass (or ❌ back to tester)
          ▼
    ┌───────────┐     story.md + failing tests
    │  Coder     │ ◄──────────── implements to make tests pass
    │ (Green)    │
    └─────┬─────┘
          │ passing code
          ▼
    ┌───────────┐
    │ QC Auditor │ ── No placeholders? No fake passes? Matches story?
    └─────┬─────┘
          │ ✅ pass (or ❌ back to coder)
          ▼
    ┌───────────┐
    │  CI/CD     │ ── Push, monitor GitHub Actions, auto-fix failures
    │  Healer    │
    └─────┬─────┘
          │
          ▼
       Done ✅
```

**Key design principles:**

1. **Information flows one way** — each role reads the output of the previous role, never reaches back upstream
2. **QC sits between every handoff** — nothing moves forward without adversarial verification
3. **The story file is the single source of truth** — tester and coder read nothing else, preventing context drift
4. **Failure loops are bounded** — coder gets 3 iterations, CI healer gets 2, then they stop and report
5. **The conductor handles state** — `PROGRESS.md` survives across sessions, so you can pick up where you left off

---

## Quick Start

### 1. Copy to your Claude Code config

```bash
# Clone
git clone https://github.com/lipingtababa/agents-zone-skillset.git

# Copy what you need
cp -r agents-zone-skillset/agents/ ~/.claude/agents/
cp -r agents-zone-skillset/skills/ ~/.claude/skills/
cp -r agents-zone-skillset/commands/ ~/.claude/commands/
cp -r agents-zone-skillset/templates/ ~/.claude/templates/
cp -r agents-zone-skillset/hooks/ ~/.claude/hooks/
```

### 2. Reference in your CLAUDE.md

```markdown
## Development Workflow

Follow TDD workflow — write tests BEFORE implementing code.

### Agents
- **Tester**: `~/.claude/agents/tester.md` — writes failing tests from story
- **Coder**: `~/.claude/agents/coder.md` — implements code to make tests pass

### Quality Control
- Run `/qc` after tester/coder complete work
- Auto-QC triggers automatically on subagent completion

### Workflow Orchestration
- Run `/conduct` to execute the next phase automatically
- PROGRESS.md tracks state across sessions
```

### 3. Customise placeholders

Files use `[bracketed placeholders]` for project-specific values:

| Placeholder | Replace with | Example |
|-------------|-------------|---------|
| `[project-root]` | Your project directory | `~/myproject` |
| `[service]` | Your service name | `api`, `web`, `worker` |
| `[your-org]` | Your GitHub org | `mycompany` |
| `[your-domain]` | Your deployment domain | `myapp.com` |
| `[shared-lib]` | Your shared library path | `lib/`, `packages/shared/` |
| `[reference-app]` | A reference implementation | `apps/example/` |
| `[infrastructure-repo]` | Your infra repo | `terraform/`, `infra/` |

---

## Usage Examples

### Full feature from scratch

```
You: /prd "Add user authentication with JWT"

Claude: [Researches requirements, asks clarifying questions, produces PRD.md]

You: /architect

Claude: [Reads PRD, designs architecture with component diagrams, produces ARCHITECTURE.md]

You: /story

Claude: [Creates hyper-detailed developer story with AC, test scenarios, file paths]

You: /conduct

Claude: [Orchestrates the full pipeline automatically]
  1. Launches tester → writes failing tests (Red phase)
  2. Auto-QC verifies test quality → ✅ pass
  3. Launches coder → implements code (Green phase)
  4. Auto-QC verifies implementation → ✅ pass
  5. Commits, pushes, monitors CI → ✅ all green
```

### Fix failing CI

```
You: /follow

Claude:
  Found: 3 lint errors, 1 test failure

  Iteration 1:
  - Fixed lint: golangci-lint --fix
  - Fixed test: missing nil check in handler
  - Local validation: ✅ all pass
  - Pushed fix commit
  - Waiting for CI... ✅ All green!
```

### Audit quality of completed work

```
You: /qc stories/user-auth.md --phase=both

Claude:
  Tester Claims:
  ✅ "Test covers authentication" → VERIFIED (tests both 200 and 401)
  ❌ "Test covers rate limiting" → FAKE TEST (only tests success case)

  Coder Claims:
  ✅ "Implemented JWT validation" → VERIFIED
  ⚠️  "Added error handling" → PARTIAL (missing timeout handling)

  Must Fix:
  1. Fix fake rate limiting test (circular validation)
  2. Add timeout error handling
```

### Teach the team a lesson

```
You: /mentor Always check for existing test fixtures before creating new ones

Claude:
  ✅ Routed to tester.md (HIGH) — embedded in "Step 2: Write Tests"
  ✅ Routed to coder.md (MEDIUM) — embedded in "Implementation Standards"
  Skipped: architect.md, prd.md (not relevant)
```

### Resume across sessions

```
You: /conduct

Claude: [Reads PROGRESS.md]
  📍 Feature: User Authentication
  📍 Phase: Implementation (Testing ✅ complete)
  📍 Next: Launch coder subagent

  ▶️ Executing Implementation phase...
```

---

## File Reference

### Agents

| File | Role | Description |
|------|------|-------------|
| [`agents/tester.md`](agents/tester.md) | Tester | TDD Red phase. Writes failing tests from story requirements. Designs from AC, not implementation. |
| [`agents/coder.md`](agents/coder.md) | Coder | TDD Green phase. Implements code to pass tests. 3-iteration limit, then reports blockage. |

### Skills

| File | Role | Description |
|------|------|-------------|
| [`skills/qc.md`](skills/qc.md) | QC Auditor | Adversarial verification. Reads actual code to verify claims. Catches fake tests, placeholders, missing coverage. |
| [`skills/follow.md`](skills/follow.md) | CI/CD Healer | Auto-fixes GitHub Actions failures. Downloads logs, categorises, fixes, validates locally, pushes. Max 2 iterations. |
| [`skills/auto_qc.md`](skills/auto_qc.md) | Auto-QC Trigger | Detects subagent completion reports and automatically triggers QC. Blocks progression on failure. |

### Commands

| File | Role | Description |
|------|------|-------------|
| [`commands/prd.md`](commands/prd.md) | Product Owner | Research-first PRD creation. Validates assumptions before documenting. MVP-phased. |
| [`commands/architect.md`](commands/architect.md) | Architect | Transforms PRD into technical architecture. Verifies against actual codebase patterns. |
| [`commands/story.md`](commands/story.md) | Story Writer | Creates self-contained developer stories. Single source of truth for tester/coder. |
| [`commands/conduct.md`](commands/conduct.md) | Conductor | Orchestrates full workflow from PROGRESS.md. Autonomous story completion. |
| [`commands/qc.md`](commands/qc.md) | QC (user docs) | User-facing documentation for the QC command. Phase-specific checks. |
| [`commands/follow.md`](commands/follow.md) | CI/CD (user docs) | User-facing documentation for the follow command. Deployment monitoring. |
| [`commands/setup.md`](commands/setup.md) | Environment Setup | Git worktrees, dependency validation, environment readiness checks. |
| [`commands/mentor.md`](commands/mentor.md) | Mentor | Embeds lessons into agent/command documentation. Dynamic discovery and routing. |

### Templates

| File | Description |
|------|-------------|
| [`templates/architecture.md`](templates/architecture.md) | 14-section architecture document scaffold |
| [`templates/prd.md`](templates/prd.md) | MVP-phased PRD template |
| [`templates/progress.md`](templates/progress.md) | Cross-session progress tracker |

### Hooks

| File | Description |
|------|-------------|
| [`hooks/validate-git.py`](hooks/validate-git.py) | Blocks `git add .` and `git add -A` to prevent accidental commits of sensitive files |

---

## Mapping to the Playbook

| Playbook Concept | Implementation Here |
|-----------------|-------------------|
| [Specification](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/02-specification.md) | `/prd` + `/architect` + `/story` + templates |
| [Test-first verification](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/03a-test-first.md) | Tester agent (Red phase before Green) |
| [Anti-collusion](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/03b-collusion.md) | Tester designs from requirements, not implementation |
| [Adversarial verification](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/03e-adversarial-verification.md) | QC auditor verifies claims with evidence |
| [Continuous feedback](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/03d-continuous-feedback.md) | Auto-QC + CI/CD healer |
| [Task decomposition](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/04b-task-decomposition.md) | Story writer breaks features into bounded tasks |
| [Context engineering](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/04c-context-engineering.md) | Story file as single source of truth |
| [Memory engineering](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/04d-memory.md) | PROGRESS.md + conductor for cross-session state |
| [Tacit knowledge](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/02d-tacit-knowledge.md) | Mentor embeds lessons into documentation |
| [Letting go](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/04e-letting-go.md) | Conductor runs full story autonomously |

---

## Contributing

Found a bug? Have a better pattern? PRs welcome.

- Keep files self-contained — each agent/skill/command works independently
- Use `[bracketed placeholders]` for project-specific values
- Test with Claude Code before submitting

## Licence

MIT
