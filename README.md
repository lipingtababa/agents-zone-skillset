# Agents Zone Skillset

Ready-to-use [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview) agents, skills, and commands that implement the engineering practices described in the [Harness Engineering Playbook](https://github.com/lipingtababa/harness-engineering-playbook).

The playbook explains **why** — closed-loop verification, specification-driven development, adversarial QC. This repo provides the **how** — copy these files into your Claude Code setup and start using them.

---

## Quick Start

### 1. Copy to your Claude Code config

```bash
# Clone this repo
git clone https://github.com/lipingtababa/agents-zone-skillset.git

# Copy what you need into ~/.claude/
cp -r agents-zone-skillset/agents/ ~/.claude/agents/
cp -r agents-zone-skillset/skills/ ~/.claude/skills/
cp -r agents-zone-skillset/commands/ ~/.claude/commands/
cp -r agents-zone-skillset/templates/ ~/.claude/templates/
cp -r agents-zone-skillset/hooks/ ~/.claude/hooks/
```

### 2. Reference in your CLAUDE.md

Add to your project's `CLAUDE.md`:

```markdown
## Development Workflow

Follow TDD workflow - write tests BEFORE implementing code.

### Agents
- **Tester**: `~/.claude/agents/tester.md` - writes failing tests from story
- **Coder**: `~/.claude/agents/coder.md` - implements code to make tests pass

### Quality Control
- Run `/qc` after tester/coder complete work
- Auto-QC triggers automatically on subagent completion
```

### 3. Customise placeholders

Search for `[bracketed placeholders]` in the files and replace with your project specifics:

```bash
# Find all placeholders
grep -r '\[.*\]' ~/.claude/commands/ | grep -v '#\|http\|bash\|---'
```

Common ones to replace:
- `[project-root]` → your project directory (e.g., `~/myproject`)
- `[service]` → your service name (e.g., `api`, `web`, `worker`)
- `[your-org]` → your GitHub org
- `[your-domain]` → your deployment domain
- `[shared-lib]` → your shared library path
- `[reference-app]` → your reference implementation path

---

## Usage Examples

### Example 1: Full feature from scratch

Start with a product idea, end with deployed code:

```
You: /prd "Add user authentication with JWT"

Claude: [Researches requirements, asks clarifying questions, produces PRD.md]

You: /architect

Claude: [Reads PRD, designs architecture with component diagrams, produces ARCHITECTURE.md]

You: /story

Claude: [Creates hyper-detailed developer story with AC, test scenarios, file paths]

You: /conduct

Claude: [Orchestrates tester → coder → QC → CI/CD automatically]
  1. Launches tester subagent → writes failing tests (Red phase)
  2. Auto-QC verifies test quality
  3. Launches coder subagent → implements code (Green phase)
  4. Auto-QC verifies implementation quality
  5. Commits, pushes, monitors CI
```

### Example 2: Fix failing CI

Your PR has red checks:

```
You: /follow

Claude: [Downloads CI logs, categorises failures]
  Found: 3 lint errors, 1 test failure

  Iteration 1:
  - Fixed lint: golangci-lint --fix
  - Fixed test: missing nil check in handler
  - Local validation: ✅ all pass
  - Pushed fix commit
  - Waiting for CI... ✅ All green!
```

### Example 3: Quality control a PR

You want to verify tester and coder claims:

```
You: /qc stories/user-auth.md --phase=both

Claude: [Reads story, extracts requirements, audits both phases]

  ## Tester Claims Verification
  ✅ "Test covers authentication" → VERIFIED (tests both 200 and 401)
  ❌ "Test covers rate limiting" → FAKE TEST (only tests success, no failure case)

  ## Coder Claims Verification
  ✅ "Implemented JWT validation" → VERIFIED
  ⚠️  "Added error handling" → PARTIAL (missing timeout handling)

  ## Required Actions
  1. Fix fake rate limiting test
  2. Add timeout error handling
```

### Example 4: Teach a lesson to all agents

You discovered a pattern that agents should follow:

```
You: /mentor Always check for existing test fixtures before creating new ones

Claude: [Analyses lesson, routes to relevant targets]
  ✅ Routed to tester.md (HIGH relevance) - embedded in "Step 2: Write Tests"
  ✅ Routed to coder.md (MEDIUM relevance) - embedded in "Implementation Standards"
  Skipped: architect.md, prd.md (not relevant)
```

### Example 5: Resume work across sessions

You started a feature yesterday and want to continue:

```
You: /conduct

Claude: [Reads PROGRESS.md]
  📍 Current State:
  - Feature: User Authentication
  - Phase: Implementation (Testing ✅ complete)
  - Next: Launch coder subagent

  ▶️ Executing Implementation phase...
  [Launches coder with story context, monitors progress]
```

---

## What's Inside

### Agents — Subagent definitions for Claude Code

| File | Role | Playbook Chapter |
|------|------|-----------------|
| [`agents/tester.md`](agents/tester.md) | TDD Red phase: writes failing tests from requirements | Ch.3 Verification |
| [`agents/coder.md`](agents/coder.md) | TDD Green phase: implements code to pass tests | Ch.3 Verification |

**Key design**: Tester designs tests from **requirements**, not implementation. This prevents the [collusion problem](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/03b-collusion.md) where AI writes tests that merely confirm what the code does.

### Skills — Reusable capabilities

| File | Purpose | Playbook Chapter |
|------|---------|-----------------|
| [`skills/qc.md`](skills/qc.md) | Adversarial QC: verifies claims against reality | Ch.3e Agent-verifies-Agent |
| [`skills/follow.md`](skills/follow.md) | CI/CD self-healing: auto-fixes GitHub Actions failures | Ch.3d Continuous Feedback |
| [`skills/auto_qc.md`](skills/auto_qc.md) | Auto-triggers QC after subagent completion | Ch.3d Continuous Feedback |

**Key design**: QC acts as an **adversarial auditor** — it doesn't trust tester/coder claims. It reads the actual code to verify. This implements the [adversarial verification](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/03e-adversarial-verification.md) pattern from the playbook.

### Commands — User-facing workflows

| File | What it does | Playbook Chapter |
|------|-------------|-----------------|
| [`commands/prd.md`](commands/prd.md) | Research-first PRD creation | Ch.2 Specification |
| [`commands/architect.md`](commands/architect.md) | Architecture design from PRD | Ch.2 Specification |
| [`commands/story.md`](commands/story.md) | Hyper-detailed developer stories | Ch.2b Machine-readable Spec |
| [`commands/conduct.md`](commands/conduct.md) | Orchestrate full workflow from PROGRESS.md | Ch.4e Letting Go |
| [`commands/qc.md`](commands/qc.md) | Quality control (user docs) | Ch.3 Verification |
| [`commands/follow.md`](commands/follow.md) | CI/CD self-healing (user docs) | Ch.3d Continuous Feedback |
| [`commands/setup.md`](commands/setup.md) | Dev environment setup | Ch.5c Platform Engineering |
| [`commands/mentor.md`](commands/mentor.md) | Embed lessons into agent docs | Ch.2d Tacit Knowledge |

### Templates — Document scaffolds

| File | Purpose |
|------|---------|
| [`templates/architecture.md`](templates/architecture.md) | Architecture doc template (14 sections) |
| [`templates/prd.md`](templates/prd.md) | PRD template (MVP-phased) |
| [`templates/progress.md`](templates/progress.md) | Progress tracking template |

### Hooks — Safety guardrails

| File | Purpose |
|------|---------|
| [`hooks/validate-git.py`](hooks/validate-git.py) | Blocks `git add .` and `git add -A` to prevent accidental commits |

---

## The Closed-Loop Workflow

This diagram shows how the pieces fit together. Each arrow is a quality gate — nothing moves forward without verification.

```
  /prd ──→ /architect ──→ /story
    │          │             │
    │     [Specification]    │
    │     (Playbook Ch.2)    │
    ▼                        ▼
  PRD.md              story.md
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
         tester agent          coder agent
         (Red phase)           (Green phase)
              │                     │
              ▼                     ▼
         auto /qc ◄────────── auto /qc
         [Verification]       [Verification]
         (Playbook Ch.3)      (Playbook Ch.3)
              │                     │
              └──────────┬──────────┘
                         ▼
                      /follow
                   [CI/CD healing]
                         │
                         ▼
                       Done ✅
```

**`/conduct` orchestrates this entire flow automatically** — it reads PROGRESS.md, determines the current phase, executes the next step, and updates progress. You can walk away and come back.

---

## Relationship to the Playbook

| Playbook Concept | Implementation Here |
|-----------------|-------------------|
| [Specification](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/02-specification.md) | `/prd`, `/architect`, `/story` commands + templates |
| [Test-first verification](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/03a-test-first.md) | `tester.md` agent (Red phase before Green) |
| [Anti-collusion](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/03b-collusion.md) | Tester designs from requirements, not implementation |
| [Adversarial verification](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/03e-adversarial-verification.md) | `qc.md` skill audits claims with evidence |
| [Continuous feedback](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/03d-continuous-feedback.md) | `auto_qc.md` + `/follow` for CI healing |
| [Task decomposition](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/04b-task-decomposition.md) | `/story` breaks features into tester→coder tasks |
| [Context engineering](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/04c-context-engineering.md) | Story file = single source of truth for subagents |
| [Memory engineering](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/04d-memory.md) | PROGRESS.md + `/conduct` for cross-session continuity |
| [Tacit knowledge](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/02d-tacit-knowledge.md) | `/mentor` embeds lessons into agent documentation |
| [Letting go](https://github.com/lipingtababa/harness-engineering-playbook/blob/main/chapters/04e-letting-go.md) | `/conduct` runs full story autonomously |

---

## Contributing

Found a bug? Have a better pattern? PRs welcome.

When contributing:
- Keep files self-contained (each agent/skill/command should work independently)
- Use `[bracketed placeholders]` for project-specific values
- Test with Claude Code before submitting

## Licence

MIT
