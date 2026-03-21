# Story: Developer Story Creation Command

Transform PRD requirements and architecture into **hyper-detailed developer stories** that give tester and coder subagents EVERYTHING they need.

## Your Mission

Create stories that serve as the **single source of truth** for tester/coder. They will ONLY have the story file - no additional context gathering.

## Critical Principles

**Story = Ultimate Context Engine**:
- Story file is the ONLY context tester/coder will have
- They will NOT search codebase or read other docs
- ALL technical details must be IN the story
- Include specific file paths, patterns, library versions

**Prevent LLM Mistakes**:
- Wrong libraries → Exact library names/imports
- Wrong locations → Exact file paths
- Reinventing → List existing utilities to reuse
- Breaking patterns → Provide pattern REFERENCES (not full code)
- Vague implementations → Interface signatures, struct fields

**Token Efficient**: Every sentence guides implementation. No fluff, scannable structure.

## Code Policy (IMPORTANT)

**Stories define WHAT to build, not HOW.**

### ✅ DO Include
- Pattern references: `See internal/handlers/users.go:25-45`
- Interface signatures: `GetUser(ctx, id) (*User, error)`
- Struct field lists: `User: ID, Name, Email, CreatedAt`
- Utility one-liners: `lo.ToPtr(value)`
- Anti-patterns: `❌ Don't use fmt.Println`

### ❌ DO NOT Include
- Full function implementations (coder should implement)
- Complete test files (tester should write)
- Entire struct definitions (field list sufficient)
- Multi-line code blocks >10 lines (too detailed, becomes stale)

**Why**: Stories with full code = copy-paste exercises. Full code drifts. Stories should guide, not dictate.

## Workflow

### Phase 1: Deep Context Gathering (CRITICAL)

**Step 1.1: Read Source Documents**
1. PRD.md - Requirements, AC, MVP scope
2. ARCHITECTURE.md - Technical design, patterns, structure
3. go.mod/package.json - Exact library versions
4. Existing handlers/services - Code patterns
5. Existing tests - Test patterns
6. Previous stories - Learnings, patterns

**Step 1.2: Extract Technical Details** (MUST INCLUDE):
```markdown
## Technical Context
### Exact Versions (from go.mod)
- Go: 1.21, Gin: v1.9.1, testify: v1.8.4

### File Paths (from ARCHITECTURE.md)
- Handler: `internal/api/handlers/[name].go`
- Service: `internal/services/[name].go`
- Tests: `test/integration/[name]_test.go`

### Existing Utilities to Reuse
- Pointer: `lo.ToPtr()` from samber/lo
- Error: `fmt.Errorf("context: %w", err)`
- HTTP errors: `gin.AbortWithStatusJSON()`

### Pattern References (paths, NOT full code)
- Handler: See `internal/api/handlers/users.go:25-45`
- Service: See `internal/services/users.go:30-50`
- Test: See `test/integration/users_test.go:15-40`
```

**Step 1.3: Identify Anti-Patterns**:
```markdown
### Anti-Patterns (DO NOT DO)
- ❌ Custom pointer helpers - use `lo.ToPtr()`
- ❌ Hand-written API structs - use `internal/api/gen/`
- ❌ Direct SQL - use GORM repository
- ❌ fmt.Println - use `zap.Logger`
```

### Phase 2: Test Scenario Planning

**Step 2.1: Analyze Feature Complexity**

**Simple** (use LIGHT scenarios):
- Basic CRUD only
- 1-3 straightforward AC
- No state transitions/workflows
- No external integrations
- No complex business logic

**Complex** (use FULL scenarios):
- Business logic (calculations, validations)
- 4+ AC
- Multi-step flows (OAuth, CIBA, payment)
- State machines (consent lifecycle)
- External integrations (external APIs)
- Financial/security/time-sensitive operations

**Step 2.2: Design Test Scenarios**

**Simple Features** (Light Template):
```markdown
## Test Scenarios
**Strategy**: Integration tests following standard CRUD pattern
**Coverage**: AC tests + basic error cases (404, 400, 500)
**Pattern**: See `test/integration_test/[similar]_test.go`
```

**Complex Features** (Full Template):
```markdown
## Test Scenarios

### Test Strategy
**Coverage**: [Unit + Integration | Integration-only]
**Complexity**: [Simple CRUD | Moderate | Complex Multi-step]

### Test Layer Breakdown
| Layer | Scope | Justification |
|-------|-------|---------------|
| Unit | [Isolated logic] | Fast feedback |
| Integration | [Endpoints/flows] | Real dependencies |

### Boundary Analysis
**Input**: [field: min, max, zero, null, empty]
**State**: [transitions: valid/invalid]
**Temporal**: [expiration, timing issues]

### Edge Cases
- Missing/invalid fields (AC#)
- External API failures (timeout, 500)
- Token expiration, invalid transitions
- [Feature-specific edge cases]

### Risk Areas
**High**: [Component/flow - why risky]
**Medium**: [Standard operations]
**Low**: [Read-only, no logic]

### Pattern References
- Integration: `test/integration_test/[example]_test.go`
- Unit: `internal/[package]/[example]_test.go`
- Table-driven for boundaries
```


### Phase 3: Story Scope Definition

**Step 3.1: Clarify with User**
1. Which feature/epic? (Specific PRD section)
2. Story size? (1-3 days completable)
3. Dependencies? (Prerequisite stories)

**Step 3.2: Break Down if Needed**
If scope too large, propose multiple stories with clear boundaries.

### Phase 4: Write Story Document

**Story Structure**:

#### Section 1: Header
```markdown
# Story: [Epic.Story] [Title]
**Status**: ready-for-dev
**Epic**: [Epic name]
**Depends On**: [Previous stories or "None"]
```

#### Section 2: User Story
```markdown
As a [role], I want [action], so that [benefit].
```

#### Section 3: Acceptance Criteria (BDD - for Tester)
```markdown
### AC1: [Happy Path]
**Given** [precondition] **When** [action] **Then** [expected result]

### AC2: [Error Case]
**Given** [error condition] **When** [action] **Then** [error response + status]
```

#### Section 4: Technical Context (for Coder - CRITICAL)
```markdown
## Technical Context
### Tech Stack & Versions
[From go.mod/package.json]

### File Locations
[Exact paths]

### Utilities to Reuse
[One-liners: `lo.ToPtr(value)`]

### Pattern References
[Paths + lines: `See internal/handlers/users.go:25-45`]

### Interface Signatures (if new)
[Method signatures: `GetUser(ctx, id) (*User, error)`]

### Struct Fields (if new)
[Field lists: `User: ID, Name, Email`]

### Anti-Patterns
[Specific things NOT to do + alternatives]
```

#### Section 5: Tasks (for Coder)
```markdown
### Task 1: [Name] (AC: #1)
- [ ] Create `path/to/file.go`
- [ ] Implement [function]
- [ ] Follow pattern from `path/to/reference.go`
```

#### Section 6: Test Requirements (for Tester)
```markdown
### Integration Tests (REQUIRED)
Location: `test/integration/[name]_test.go`

| Test Case | AC | Input | Expected |
|-----------|-----|-------|----------|
| Happy path | #1 | valid | 200 + data |
| Not found | #2 | invalid ID | 404 |

### Mock Requirements
- Mock [external service]
- Use fixtures from `test/fixtures/`
```

#### Section 7: Definition of Done
```markdown
- [ ] All AC have passing tests
- [ ] No regressions
- [ ] No TODO/FIXME in production
- [ ] Code follows patterns
- [ ] Coverage >80%
```

### Phase 5: Validation

**Content Checks**:
- [ ] All AC testable (Given-When-Then)
- [ ] File paths REAL (from architecture)
- [ ] Library versions REAL (from go.mod)
- [ ] Anti-patterns specific to codebase
- [ ] Tasks map to AC
- [ ] Test requirements cover all AC

**Code Policy Checks**:
- [ ] NO full function implementations (use references)
- [ ] NO complete test code (use requirements table)
- [ ] NO code blocks >10 lines
- [ ] Pattern references to REAL files + lines
- [ ] Interface signatures concise (one line/method)
- [ ] Struct definitions field lists only

### Phase 6: Save Story

**CRITICAL: Save story to dev branch, NOT worktree**

When using git worktrees:
```bash
# ✅ CORRECT: Save story to dev branch
cd [project-root]/[project]-dev-branch
# Story file saved here in plans/

# Then create worktree for implementation
git worktree add [project-root]/[project]-S${NUM}-feature -b S${NUM}-feature
cd [project-root]/[project]-S${NUM}-feature
# Implement code here - story already in dev ✅
```

**Why this matters**: Story files created in worktree branches are lost when worktrees are deleted. Story files must survive in the main dev branch for documentation continuity.

Save to: `plans/S${NUM}-[title].md` (or project-specific plans directory)


## Story Template

```markdown
# Story: [Epic.Story] [Title]

**Status**: ready-for-dev
**Epic**: [Epic name]
**Depends On**: [Dependencies]

---

## User Story

As a [role], I want [action], so that [benefit].

---

## Acceptance Criteria

### AC1: [Name]
**Given** [precondition] **When** [action] **Then** [result]

### AC2: [Name]
**Given** [precondition] **When** [action] **Then** [result]

---

## Technical Context

### Tech Stack & Versions
- Language: [version], Framework: [version], Database: [version]

### File Locations
[Exact paths where new files go]

### Utilities to Reuse
- `lo.ToPtr(value)` - Pointers (samber/lo)
- `fmt.Errorf("context: %w", err)` - Error wrapping
- `logger.Info("msg", zap.String("k", v))` - Logging (uber/zap)

### Pattern References
- Handler: `internal/api/handlers/[existing].go:[lines]`
- Service: `internal/services/[existing].go:[lines]`
- Test: `test/integration/[existing]_test.go:[lines]`

### Anti-Patterns
- ❌ [Thing not to do] → Do [this] instead

---

## Implementation Guidance

### [Component] Fields (if new struct)
FieldName1, FieldName2, FieldName3 (types if non-obvious)

### Interface Signatures (if new interface)
- `MethodName(param1, param2) (ReturnType, error)`
- `OtherMethod(ctx, id) (*Result, error)`

### Key Logic (prose, not code)
- [Step 1], [Step 2], [Edge case handling]

---

## Tasks

### Task 1: [Name] (AC: #1, #2)
- [ ] [Subtask]
**Files**: `path/to/file.go`
**Pattern**: `path/to/reference.go`

### Task 2: [Name] (AC: #3)
- [ ] [Subtask]
**Depends On**: Task 1

---

## Test Scenarios

[Content from Phase 2 - light or full template based on complexity]

---

## Test Requirements

### Integration Tests
**Location**: `test/integration/[name]_test.go`

| Test Case | AC | Input | Expected |
|-----------|-----|-------|----------|
| [case] | #1 | [input] | [output] |

### Mocks Required
- [What to mock and how]

---

## Definition of Done

- [ ] All AC have passing tests
- [ ] No regressions
- [ ] No TODO/FIXME
- [ ] Follows patterns
- [ ] Coverage >80%
```

## Integration with TDD Workflow

```
/story creates story.md
       ↓
tester reads story.md → writes failing tests
       ↓
coder reads story.md + tests → implements code
       ↓
Done when Definition of Done met
```

**Tester and coder will ONLY read the story file. They trust it has everything.**

## After Completion

**Immediate Actions**:
1. **Verify story file committed to dev branch**:
   ```bash
   cd [project-root]/[project]-dev-branch
   git add plans/S${NUM}*.md
   git commit -m "docs: Add S${NUM} story"
   git push origin dev
   ```
2. **Verify file exists** before proceeding:
   ```bash
   ls -lh plans/S${NUM}*.md
   # Must show file - if not found, story will be lost!
   ```

Update `PROGRESS.md`:
1. Mark [x] Story phase complete
2. Add story info to Current Work section
3. Note story file path for validation
