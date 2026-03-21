# QC Command - Quality Control Checker

## Purpose
The `/qc` command performs automated quality control checks on code and tests produced by tester and coder subagents, verifying alignment with stories and PRDs.

## Usage
```
/qc [story-file] [options]
```

**Arguments:**
- `story-file` (optional): Path to story file (auto-detected if not provided)
- `--phase=<phase>`: Which phase to check (`tester`, `coder`, or `both` - default: `both`)
- `--prd=<file>`: Path to PRD file (optional)
- `--changed-files`: Only check files changed in current branch
- `--strict`: Enable strict mode (warnings become failures)

**Examples:**
```bash
/qc                           # Check both tester and coder outputs
/qc --phase=tester           # Only check tester's test files
/qc --phase=coder            # Only check coder's implementation
/qc stories/login.md --strict # Strict mode on specific story
```

## Quality Check Categories

### 1. Placeholder Detection
**Purpose**: Identify incomplete or stub implementations

**Checks:**
- ❌ Functions returning hardcoded empty values (`return []`, `return {}`, `return ""`)
- ❌ HTTP handlers returning `501 Not Implemented` (should be temporary only)
- ❌ TODO/FIXME/HACK comments in implementation code
- ❌ Stub functions that don't contain real logic
- ❌ Copy-pasted code with "example" or "placeholder" names
- ❌ Functions that always return success without actual work
- ⚠️  Functions with only logging, no business logic

**Pass Criteria:**
- All functions have real implementations
- No hardcoded empty returns unless explicitly justified
- No TODO/FIXME in production code (tests are OK)

### 2. Fake Test Detection
**Purpose**: Ensure tests actually validate functionality

**Checks:**
- ❌ Tests that always pass (no assertions)
- ❌ Tests using `t.Skip()` without justification
- ❌ Mock implementations that don't simulate real behavior
- ❌ Tests checking only for non-error, not correctness
- ❌ Tests with hardcoded expected values matching stub returns
- ❌ Integration tests that don't exercise real dependencies
- ⚠️  Tests with only a single assertion
- ⚠️  Missing negative test cases (error paths)

**Pass Criteria:**
- All tests have meaningful assertions
- Tests verify both success and failure cases
- Integration tests use real or realistic dependencies
- No skipped tests (unless using build tags properly)

### 3. Story Alignment Check
**Purpose**: Verify implementation and tests satisfy story requirements

**Checks:**
- ❌ Story requirements not implemented
- ❌ Story acceptance criteria not covered by tests
- ❌ Implementation deviates from story specification
- ⚠️  Extra features not mentioned in story (scope creep)
- ⚠️  Different approach than story suggests (may be OK if justified)

**Pass Criteria:**
- All story requirements have corresponding implementation
- All acceptance criteria have corresponding tests
- Implementation approach matches or improves upon story design

### 4. PRD Alignment Check
**Purpose**: Verify story and implementation meet PRD goals

**Checks:**
- ❌ Story solves different problem than PRD describes
- ❌ Implementation breaks PRD constraints (performance, security, etc.)
- ❌ Missing PRD requirements in story
- ⚠️  Story adds scope beyond PRD (may need PRD update)
- ⚠️  Technical approach differs from PRD architecture

**Pass Criteria:**
- Story addresses PRD requirements
- Implementation respects PRD constraints
- No scope gaps between PRD → Story → Implementation

### 5. Code Quality Check
**Purpose**: Identify common quality issues

**Checks:**
- ❌ Hardcoded credentials, API keys, or sensitive data
- ❌ Mixing test frameworks or paradigms unnecessarily
- ❌ Missing error handling in critical paths
- ❌ Inconsistent patterns with existing codebase
- ⚠️  Complex functions without comments
- ⚠️  Overly generic variable names (`data`, `result`, `temp`)
- ⚠️  Duplicated code (should be refactored)

**Pass Criteria:**
- No security vulnerabilities
- Error handling present and appropriate
- Code follows project conventions
- Reasonable complexity and readability

### 6. Completeness Check
**Purpose**: Ensure all aspects of the work are finished

**Checks:**
- ❌ Story marked complete but has unfinished requirements
- ❌ Tests written but not passing
- ❌ Implementation written but tests not updated
- ❌ Integration tests not run (when required)
- ⚠️  Missing documentation for complex logic
- ⚠️  No comments explaining non-obvious decisions

**Pass Criteria:**
- All story tasks marked as complete
- All tests passing
- Implementation and tests in sync
- Adequate documentation

## QC Workflow

### Step 1: Context Gathering
1. **Locate story file** (auto-detect or use provided path)
2. **Locate PRD** (if `--prd` provided or auto-detected)
3. **Identify changed files** (via git diff or explicit list)
4. **Read relevant documentation** (README, architecture docs)

### Step 2: Implementation Analysis
1. **Scan implementation files** for placeholder patterns
2. **Analyze function implementations** for real logic
3. **Check error handling** and edge cases
4. **Verify security best practices** (no hardcoded secrets)
5. **Assess code complexity** and readability

### Step 3: Test Analysis
1. **Scan test files** for fake test patterns
2. **Analyze test assertions** for meaningfulness
3. **Check test coverage** of requirements
4. **Verify negative test cases** exist
5. **Validate integration test quality**

### Step 4: Alignment Verification
1. **Extract story requirements** and acceptance criteria
2. **Map requirements to implementation** (each req → code)
3. **Map acceptance criteria to tests** (each criterion → test)
4. **If PRD provided, verify story covers PRD goals**
5. **Check for scope creep** or missing scope

### Step 5: Report Generation
1. **Categorize findings** (fail/warn/pass)
2. **Provide specific locations** (file:line references)
3. **Suggest fixes** for each issue
4. **Generate summary statistics**
5. **Provide overall pass/fail verdict**

## Output Format

```markdown
# Quality Control Report
Generated: [timestamp]
Story: [story-file]
PRD: [prd-file or N/A]

## Summary
- ✅ Passed: X checks
- ⚠️  Warnings: Y checks
- ❌ Failed: Z checks

**Overall Verdict**: [PASS | FAIL | PASS WITH WARNINGS]

---

## 1. Placeholder Detection
[PASS | FAIL | WARNINGS]

### Issues Found:
- ❌ `internal/service/account.go:45` - Function returns empty array without implementation
  ```go
  func GetAccounts() []Account {
      return [] // Placeholder!
  }
  ```
  **Suggestion**: Implement actual account retrieval logic

- ⚠️  `internal/handler/balance.go:23` - Only logging, no business logic
  **Suggestion**: Add balance calculation or retrieval

---

## 2. Fake Test Detection
[PASS | FAIL | WARNINGS]

### Issues Found:
- ❌ `test/account_test.go:12` - Test has no assertions
  ```go
  func TestGetAccounts(t *testing.T) {
      accounts := GetAccounts()
      // No assertions!
  }
  ```
  **Suggestion**: Add assertions to verify account data

---

## 3. Story Alignment
[PASS | FAIL | WARNINGS]

### Requirements Coverage:
- ✅ Req 1: User can view account list - IMPLEMENTED & TESTED
- ❌ Req 2: User can filter by account type - NOT IMPLEMENTED
- ✅ Req 3: System caches results - IMPLEMENTED & TESTED

### Issues Found:
- ❌ Story requirement "filter by account type" has no corresponding implementation
  **Suggestion**: Implement filtering in `GetAccounts()` function

---

## 4. PRD Alignment
[PASS | FAIL | WARNINGS]

### PRD Goals Coverage:
- ✅ Goal: Provide account overview - COVERED
- ⚠️  Constraint: Response time < 200ms - NOT VERIFIED IN TESTS

### Issues Found:
- ⚠️  PRD specifies response time constraint but no performance tests exist
  **Suggestion**: Add performance test or benchmarks

---

## 5. Code Quality
[PASS | FAIL | WARNINGS]

### Issues Found:
- ❌ `internal/db/connection.go:8` - Hardcoded database password
  **Suggestion**: Use environment variable

---

## 6. Completeness
[PASS | FAIL | WARNINGS]

### Status:
- ✅ All tests passing
- ❌ 1 story requirement not implemented
- ✅ No TODOs in production code

---

## Recommendations

### Must Fix (Blockers):
1. Implement account filtering (story req 2)
2. Remove hardcoded password in db/connection.go
3. Add assertions to account_test.go

### Should Fix (Warnings):
1. Add performance tests for response time constraint
2. Add comments to complex balance calculation logic

### Nice to Have:
1. Refactor duplicated error handling code
2. Add integration test for account filtering

---

## Detailed File Analysis

### Files Checked:
- internal/service/account.go (Implementation)
- internal/handler/balance.go (Implementation)
- test/account_test.go (Test)
- test/integration_test/account_integration_test.go (Test)

### Files with Issues:
- ❌ internal/service/account.go (2 issues)
- ❌ internal/db/connection.go (1 issue)
- ❌ test/account_test.go (1 issue)
- ⚠️  internal/handler/balance.go (1 warning)

---

## Git Operations (When QC Passes)

When **Overall Verdict: PASS**, QC automatically commits and pushes:

### Commit Created:
- **SHA**: abc123f
- **Message**: [IT-8830] Implement GET /accounts endpoint
- **Summary**:
  - Added GET /accounts handler with authentication
  - Implemented filtering by account type
  - Created integration tests with PostgreSQL
  - Quality Control: ✅ PASSED

### Push Status:
- ✅ Pushed to: origin/feature-branch
- Commit URL: https://github.com/[your-org]/[your-repo]/commit/abc123f

### Next Steps:
1. Run `/follow` to ensure CI passes
2. Create pull request after CI is green
3. Update progress.md
```

## Integration with Workflow

### When to Use `/qc`

**Required:**
- ✅ After tester completes test suite (use `--phase=tester`)
- ✅ After coder completes implementation (use `--phase=coder`)
- ✅ Before marking story as complete (use `--phase=both` or no flag)

**Optional:**
- During development to catch issues early
- After major refactoring
- When reviewing others' code

### Typical Workflow Integration

```
1. User creates story (via /story)
2. Main agent assigns to tester subagent
3. Tester writes tests
4. Main agent runs /qc [story] --phase=tester
   → If QC fails: Fix issues, return to step 3
   → If QC passes: Continue to step 5
5. Main agent assigns to coder subagent
6. Coder implements code
7. Main agent runs /qc [story] --phase=coder
   → If QC fails: Fix issues, return to step 6
   → If QC passes:
     ✅ QC commits and pushes changes
     Continue to step 8
8. Main agent runs /follow
   → Ensures CI passes, fixes any failures
9. Main agent updates progress.md
10. Story complete! Ready for PR
```

### Phase-Specific Checks

**`--phase=tester` checks:**
- Phase 2: Verify Tester's Deliverables
  - Fake test detection
  - Test coverage of acceptance criteria
  - Test quality and assertions
- Phase 4: Cross-Verification (tests vs requirements)
- Phase 5: Generate report (tester section only)

**`--phase=coder` checks:**
- Phase 3: Verify Coder's Deliverables
  - Placeholder detection
  - Implementation quality
  - Error handling
- Phase 4: Cross-Verification (implementation vs tests)
- Phase 5: Generate report (coder section only)
- Phase 6: Run tests
- Phase 7: Git operations (commit + push)

**`--phase=both` checks (default):**
- All phases (2, 3, 4, 5, 6, 7)
- Comprehensive verification
- Use when both tester and coder have completed

## Configuration

### QC Rules Configuration (Optional)
Create `.claude/qc.yaml` to customise rules:

```yaml
qc:
  strict_mode: false
  ignore_patterns:
    - "**/*_generated.go"
    - "**/vendor/**"

  placeholder_detection:
    enabled: true
    fail_on_todo: true
    allowed_stubs:
      - "internal/providers/example/**"  # Known incomplete provider

  test_quality:
    enabled: true
    min_assertions_per_test: 1
    require_negative_tests: true

  story_alignment:
    enabled: true
    require_all_requirements: true

  prd_alignment:
    enabled: true
    auto_detect_prd: true

  code_quality:
    enabled: true
    max_function_lines: 50
    max_complexity: 10
```

## Error Handling

### If Story File Not Found:
- Search for `.claude/*.md` files
- Search for `docs/stories/*.md` files
- Ask user to provide path

### If PRD Not Provided:
- Look for `.claude/prd.md`
- Look for `docs/prd.md`
- Continue without PRD checks if not found

### If Cannot Determine Changed Files:
- In git repo: Use `git diff --name-only`
- Not in git: Ask user to specify files
- Fallback: Check entire codebase (may be slow)

## Success Criteria

A QC check **passes** when:
- ✅ Zero failed checks (❌ items)
- ⚠️  Warnings are acceptable (but should be addressed)

A QC check **fails** when:
- ❌ One or more failed checks exist
- Must fix all failed items before proceeding

## Future Enhancements

Potential additions:
- Performance regression detection
- Security vulnerability scanning (SAST)
- Dependency version checks
- Code coverage metrics
- API contract validation
- Database migration checks

## After Completion

**Update Project Progress**:

After QC passes, update `PROGRESS.md`:
1. Mark [x] Quality Check phase complete
2. Set next step: "Run `/follow` to validate CI/CD" or "Ready for PR creation"
