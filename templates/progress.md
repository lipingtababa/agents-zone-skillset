# Project Progress: [Project Name]

**Last Updated**: YYYY-MM-DD HH:MM
**Current Phase**: [design|architect|story|setup|test|code|qc|ci]

---

## Current Work

### [Feature/Story Name] - [Ticket ID]
**Started**: YYYY-MM-DD
**Last Updated**: YYYY-MM-DD HH:MM
**Status**: In Progress
**Story**: `[path/to/story.md or plans/story.md]`
**Branch**: `[IT-XXXX-description]`

**Phase Progress**:
- [ ] Design (PRD)
- [ ] Architecture (ARCHITECTURE.md)
- [ ] Story (story.md - creates ticket)
- [ ] Setup (environment setup - optional)
- [ ] Testing (tester subagent)
- [ ] Implementation (coder subagent)
- [ ] Quality Check (qc)
- [ ] Dev Testing (merge to dev, auto-deploy, validate)
- [ ] CI/CD (PR dev→main)

**Artifacts**:
- PRD: `[path/to/PRD.md]`
- Architecture: `[path/to/ARCHITECTURE.md]`
- Story: `[path/to/story.md]`

**Details** (Optional):
- Estimated: [X hours/days]
- Impact: [What this unblocks or enables]
- Changes Required:
  - [Bullet list of major changes]
  - [Technical details]

**Notes**:
- Waiting on: [Dependencies or prerequisites]
- Blockers: [None or list]
- Next step: [What to do next]

<!-- Example:
### Offset/Limit Pagination - IT-XXXX-S9
**Started**: 2025-12-26
**Story**: `apps/[service]/plans/S9-offset-limit-pagination.md`

**Phase Progress**:
- [x] Design
- [x] Architecture
- [x] Story
- [ ] Testing (current)

**Details**:
- Impact: Unblocks [Provider A] and [Provider B] providers
- Changes Required:
  - Add PaginationType to ProviderConfig
  - Update BaseProvider URL building logic
-->

---

## Completed

### [Feature Name] - [Ticket ID] (Completed: YYYY-MM-DD)
**PR**: #[number]
**Summary**: [Brief description of what was accomplished]

**Achievements**:
- [Major accomplishments]
- [Metrics if relevant: e.g., "5x faster", "300 lines reduced"]
- [Test results: e.g., "All 35 tests passing"]

<!-- Example:
### Flow-Based Provider Architecture - IT-XXXX (2025-12-24)
**PR**: #87
**Summary**: Refactored authentication flows to reusable flow-based pattern

**Achievements**:
- 472 lines of reusable flow code
- 5x faster provider implementation time (4-6h → ~1h)
- 2 providers fully working ([Provider A], [Provider B])
- Zero code duplication
-->

---

## Blocked

### [Feature Name] - [Ticket ID]
**Blocked Since**: YYYY-MM-DD
**Reason**: [Why blocked - e.g., waiting for API credentials, missing dependency]
**Unblock Action**: [What needs to happen to unblock]
**Owner**: [Who is responsible for unblocking]

<!-- Example:
### [Provider A] Integration - IT-XXXX
**Blocked Since**: 2025-12-20
**Reason**: Waiting for developer portal access
**Unblock Action**: Contact DevOps team to request portal registration
**Owner**: DevOps team
-->

---

## Gap Analysis vs PRD (Optional)

<!-- Use this section for complex projects to track requirements vs implementation -->

### [Service Name] PRD Gaps

| Category | Gap | Priority | Status | Notes |
|----------|-----|----------|--------|-------|
| **Feature X** | Description | High | Not implemented | Details |
| **Feature Y** | Description | Medium | In progress | Details |

<!-- Example:
| **Pagination** | Offset/Limit support | High | Not implemented | Blocks 2 providers |
| **Pagination** | Token-based | High | Implemented | Works for [Provider A], [Provider B] |
-->

---

## Metrics (Optional)

<!-- Use this section to track quantitative progress -->

| Metric | Current | Target | Progress |
|--------|---------|--------|----------|
| [Metric name] | X/Y | Y | XX% |

<!-- Example:
| Providers | 2/11 | 11 | 18% |
| API Endpoints | 11/11 | 11 | 100% |
| Test Coverage | Comprehensive | Comprehensive | Done |
-->

---

## Next Steps (Optional)

<!-- Priority-ordered list of what to do next -->

### Critical (This Week)
1. [High priority item with estimate]
2. [Another critical item]

### High Priority (Following Week)
3. [High priority item]
4. [Another high priority item]

### Medium Priority
5. [Medium priority item]

<!-- Example:
### Critical
1. Implement Story S9 - Offset/Limit Pagination
2. Register at provider developer portals

### High Priority
3. Implement [Provider A] integration (~1 hour after S9)
4. Implement [Provider B] integration (~1 hour after S9)
-->

---

## Branching Workflow

**Strategy**: feature → dev → main

**Daily Flow**:
1. Create feature branch from main: `git checkout -b IT-XXXX-name`
2. Develop feature (use `/conduct` for automation)
3. After QC passes: Merge to dev → auto-deploys to dev environment
4. Validate in dev: Test at https://dev-{service}.[your-domain]
5. Create PR: `gh pr create --base main --head dev`
6. After merge: dev and main are in sync

**Commands**:
- `/conduct` - Automates workflow, merges to dev after QC
- `/follow` - Monitors dev deployment
- `/qc` - Quality checks before dev merge

---

## Usage Guidelines

**When to Update**:
- After completing a story/ticket
- After major milestones (e.g., "all tests passing")
- After significant refactoring or implementation
- NOT for every file edit or minor change

**Who Updates**:
- **Main agent**: Updates based on subagent reports and phase completions
- **Subagents**: Report back to main agent (do NOT directly update PROGRESS.md)

**Update Workflow**:
1. Subagent completes work → reports to main agent
2. Main agent reads report → updates PROGRESS.md
3. Mark phase complete, add notes, move to Completed/Blocked if done

**Flexibility**:
- **Simple features**: Use minimal format (just Phase Progress + basic notes)
- **Complex projects**: Use full format (with Gap Analysis, Metrics, detailed Next Steps)
