# Conduct: Workflow Orchestration Command

Orchestrate complete feature development by reading PROGRESS.md, validating prerequisites, executing phases, and updating progress automatically.

## Mission

Resume and continue workflows seamlessly - no context loss between sessions:
1. Read PROGRESS.md to understand current state
2. Validate prerequisites for next phase
3. Execute appropriate command/subagent
4. Update PROGRESS.md after completion
5. Handle blockers gracefully

## Core Principle

**PROGRESS.md is the single source of truth** - Never maintain separate state.

---

## Workflow

### Phase 1: Initialize

**Project Context**:
- **Working Directory**: `[project-root]` (parent directory for all project repos)
- **PROGRESS.md Location**: `[project-root]/[project]-dev-branch/plans/PROGRESS.md`
- **Stories Location**: `[project-root]/[project]-dev-branch/plans/`
- **Git Workflow**: Use `git worktree` to create new branches when starting work on a story

**Locate PROGRESS.md**:
1. Default: Check `[project-root]/[project]-dev-branch/plans/PROGRESS.md`
2. Fallback: Search `./PROGRESS.md`, `../PROGRESS.md`, up to 3 levels

**If not found**: Offer to run `/prd`, create manually from `~/.claude/PROGRESS.md.template`, or navigate to project directory

**Parse**: Extract features in "In Progress", phase checkmarks, artifact paths, notes, blockers

**Discover All Stories**:
1. Scan `[project-root]/[project]-dev-branch/plans/` for all `*.md` files
2. Cross-reference with PROGRESS.md entries
3. **If story exists but not in PROGRESS.md**: Add to "In Progress" section with initial state:
   ```markdown
   ### [Story Name] - [ID]
   **Phase Progress**: [ ] Design [ ] Architecture [ ] Story [ ] Setup [ ] Testing [ ] Implementation [ ] Quality Check [ ] Dev Testing [ ] CI/CD
   **Artifacts**: Story: `plans/[story-file].md`
   **Current Phase**: Story (already exists)
   **Next Step**: Setup
   **Last Updated**: [timestamp]
   ```

**Select Feature**:
- 1 in progress → auto-select
- 2+ in progress → select most recently updated
- 0 in progress → check "Blocked" section, offer to resume or run `/prd`

---

### Phase 2: Validate State

**Determine Current Phase**: First unchecked item in Phase Progress

**If all phases checked**: Offer to create PR, mark completed, or add deployment phase

**Prerequisites by Phase**:

| Phase | Prerequisites |
|-------|---------------|
| Design | None |
| Architecture | PRD.md exists |
| Story | ARCHITECTURE.md exists |
| Setup | **story.md exists AND committed to dev branch** |
| Testing | story.md, git branch exists |
| Implementation | Tests exist and failing |
| Quality Check | Implementation complete, tests passing |
| Dev Testing | QC passed, in project repo, dev branch exists |
| CI/CD | Dev Testing passed, feature validated in dev |

**If prerequisites missing**: Report actionable error with fix suggestions

**Story File Validation** (before Setup phase):
```bash
# Verify story file exists in dev branch
cd [project-root]/[project]-dev-branch
if [ ! -f "plans/S${NUM}*.md" ]; then
  echo "❌ BLOCKER: Story file missing in dev branch"
  echo "Expected: plans/S${NUM}*.md"
  echo "Action: Run /story to create story file in dev branch"
  exit 1
fi
```

**Blocked features**: Ask user if blocker resolved, move back to "In Progress" if yes

---

### Phase 3: Execute Next Phase

**Announce**:
```
Current State:
- Feature: [Name] - [ID]
- Current Phase: [Phase]
- Next Step: [Action]
Artifacts: [Paths]
Executing [Phase]...
```

**Dry-run mode** (`--dry-run`): Show what would execute without actually running or updating PROGRESS.md

**Execute**:

**Command Phases** (prd, architect, story, setup, qc, follow):
- Invoke command with context from PROGRESS.md
- Wait for completion
- Verify output artifact created

**Subagent Phases** (tester, coder):
- Launch via Task tool with story path
- Wait for completion
- Parse report for phase status, artifacts, next step

**On Success**: Report completion, update PROGRESS.md (mark phase [x], update timestamp, add notes), ask to continue to next phase

**On Blockage**: Report blocker, move to "Blocked" section in PROGRESS.md with reason and unblock actions

---

### Phase 4: Update PROGRESS.md

**Read-Modify-Write Pattern** (atomic):
1. Read current PROGRESS.md
2. Parse to find feature entry
3. Update: mark phase [x], timestamp, current phase, notes, next step
4. Write back

---

## Phase Execution Details

**Design**: `/prd` workflow → creates PRD.md → mark [x] Design, next: Architecture

**Architecture**: `/architect` workflow, reads PRD → creates ARCHITECTURE.md → mark [x] Architecture, next: Story

**Story**: `/story` workflow, reads PRD + ARCHITECTURE → creates story.md → **verify file committed to dev** → mark [x] Story, next: Setup

**Setup**: `/setup` workflow → create branch, worktree → mark [x] Setup, next: Testing

**Testing**: Launch tester subagent → writes failing tests → mark [x] Testing, next: Implementation

**Implementation**: Launch coder subagent → implements code → mark [x] Implementation, next: QC OR move to "Blocked" if blocked

**Quality Check**: `/qc` workflow → validates quality → mark [x] QC, next: Dev Testing OR stay in Implementation if fails

**Dev Testing**: Merge to dev, deploy, monitor GitHub Actions (10min timeout), verify health check → mark [x] Dev Testing, next: CI/CD OR stay if fails

**CI/CD**: Create PR via `gh pr create`, monitor via `/follow` → mark [x] CI/CD → move to "Completed" when merged

---

## Git Worktree Workflow

**When Setup phase starts**:
1. Navigate to base repo: `[project-root]/[project]-dev-branch`
2. Create new worktree with descriptive branch from `dev` base
3. Work in the isolated worktree directory
4. When complete, merge back to dev branch

**Naming Convention**: `[project]-{STORY_ID}-{short-description}` (e.g., `[project]-S27-feature-name`)

**Example**:
```bash
cd [project-root]/[project]-dev-branch
git worktree add [project-root]/[project]-S27-feature-name -b S27-feature-name
cd [project-root]/[project]-S27-feature-name
# Work on story here
```

**Check existing worktrees**:
```bash
git worktree list
```

---

## Error Handling

**Missing Prerequisites**: Show expected vs actual, suggest fixes (run command, update path, create manually)

**Corrupted PROGRESS.md**: Offer to fix manually, backup/recreate from template, or help diagnose

**Multiple Failures**: After 3 failures, move to "Blocked" section with reason

---

## State Transitions

**In Progress → Completed**: All phases checked → offer PR creation → move to "Completed" section

**Blocked → In Progress**: User confirms blocker resolved → move back, resume from blocked phase

**In Progress → Blocked**: Phase fails → move to "Blocked" with reason and unblock actions

---

## Workflow Intelligence

**Smart Phase Selection**: If Testing phase but tests passing → warn unexpected state, offer to skip to Implementation or re-run tester

**Context Passing**: Automatically pass artifact paths between phases via PROGRESS.md

---

## Invoking Commands/Subagents

**Commands**: Invoke as if user ran it, pass context from PROGRESS.md

**Subagents**: Use Task tool:
```
Task(
  subagent_type="tester|coder",
  prompt="[Phase] for story at [path]. Follow guidelines. Report: phase completed, artifacts, next step."
)
```

**Parse Reports**:
- Tester: "Phase completed: Testing", "Artifacts created: [files]", "Tests verified to FAIL"
- Coder: "Implementation Complete ✅" / "Implementation Blocked ❌", "Files Created/Modified: [files]", "Blocker: [reason]"

---

## Usage

```bash
/conduct              # Execute next phase
/conduct --dry-run    # Preview without executing
```

**Typical Session**:
```
Day 1:
$ /prd "Add login" → PRD.md
$ /conduct → /architect → ARCHITECTURE.md
$ /conduct → /story → story.md

Day 2:
$ /conduct → /setup → branch created
$ /conduct → tester → tests written
$ /conduct → coder → code implemented
$ /conduct → /qc → quality verified
$ /conduct → merge to dev → deployed
$ /conduct → PR created
```

---

## Autonomous Execution

**Goal**: Complete one full story autonomously, then pause before next story

**Execute automatically** (no user prompt):
- Phase transitions within story
- Git commits after QC
- PROGRESS.md updates

**Prompt user only when**:
- Story complete (before next story)
- Prerequisites missing
- Failures/errors needing decisions
- All work done (PR creation)
- Ambiguous situations

**Never prompt for**:
- Phase execution within story
- Normal workflow operations

---

## Key Principles

1. **PROGRESS.md is truth** - Always read, never cache
2. **Validate before execute** - Check prerequisites every time
3. **Autonomous by default** - Complete full story without prompting
4. **Graceful failures** - Clear errors + suggested fixes
5. **Atomic updates** - Read-modify-write PROGRESS.md atomically
6. **No shortcuts** - Don't skip validation

**Keep it Simple**: One feature at a time, complete full story autonomously, clear reporting, dry-run for troubleshooting only

---

**Now implement the /conduct command following this workflow!**
