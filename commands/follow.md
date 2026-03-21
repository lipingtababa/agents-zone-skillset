# Follow Command - CI/CD Self-Healing

## Overview

Automatically monitors GitHub Actions, detects CI/CD failures, and fixes them through intelligent iteration until all checks pass or manual intervention is required.

## When to Use

```bash
/qc      # Quality check → commit → push
/follow  # Monitors CI, fixes any failures

# After coder completes
/coder → /qc → /follow

# When PR has failing checks
/follow  # Analyses and fixes automatically
```

## What It Does

1. **Monitors** - GitHub Actions status via gh CLI
2. **Analyses** - Categorises failures (tests, lint, build, deployment)
3. **Fixes** - Applies intelligent fixes based on type
4. **Validates** - Tests locally before pushing (saves CI time!)
5. **Iterates** - Max 2 attempts, then reports blockage
6. **Reports** - Success summary or actionable blockage analysis

## Key Features

- **Autonomous** - Minimal permission requests
- **Local Validation** - Catches 80% of issues before CI (saves 5-10 min!)
- **Critical Thinking** - Reads actual code, doesn't trust comments blindly
- **Safe** - Rollback on regression, circuit breaker on environment issues

## How It Works

### Phase 1: Discovery (~30s)
- Check GitHub Actions status
- Download failure logs
- Categorise by type, prioritise fixes

### Phase 2: Fix Loop (5-8 min/iteration, max 2)
1. Select fix strategy
2. Apply fixes
3. **Validate locally** (critical!)
4. Commit & push only if local passes
5. Wait for CI (poll every 15s)
6. Evaluate results

### Phase 3: Report
**Success**: Files fixed, duration, ready for PR
**Blockage**: Issue analysis, attempted fixes, required manual action

## Dev Branch Deployment Monitoring

When on `dev` branch, `/follow` monitors deployment workflows:

**Detection**:
- Repo: [project-main]
- Service: any configured service
- Workflows: `{service}-deploy-dev.yaml` or `{service}-build.yaml`

**Stages Monitored**:
- Test → Build → Deploy → Health Check

**Success Report**:
```
Dev Deployment Complete
Service: [service-a] | Version: abc123f | URL: https://dev-[service].[your-domain].com
Duration: 7m 30s | All stages passed
Next: Test feature, then create PR
```

**Failure Handling**:
- Test failures: Auto-fix (same as regular CI)
- Build failures: Analyse logs, suggest fixes (manual intervention)
- Deploy failures: Report infra issues, check cloud console
- Health failures: Check port config, rollback may occur

**Integration with /conduct**:
- `/conduct` calls `/follow` during Dev Testing phase
- Updates PROGRESS.md based on results

## Fix Strategies

**Lint** (auto-fix):
- Go: `golangci-lint run --fix`
- Ruby: `rubocop -a`
- Terraform: `terraform fmt -recursive`

**Tests** (analysis required):
- Read test + implementation
- Identify root cause
- Fix or delegate to coder if complex

**Build** (deps/syntax):
- Add missing imports
- Fix function names
- `go mod tidy` / `bundle install`

**Deploy** (config):
- Format terraform
- Fix validation errors
- Report state/permission issues

## Local Validation

**Why critical**: CI runs take 3-5 min, local takes 1-2 min. Saves 3-4 min/iteration!

**Go projects**:
```bash
golangci-lint run ./...
go test ./... -v -race -failfast
go build ./...
```

**Ruby projects**:
```bash
docker-compose run --rm service bundle exec rubocop
docker-compose run --rm service bundle exec rspec --fail-fast
```

**Terraform**:
```bash
terraform fmt -recursive -check
terraform validate
pre-commit run --all-files
```

## Safety Features

**Rollback**: If fixes increase failures, rollback & try alternative

**Circuit Breaker** - Stops if:
- Same error 2 iterations in a row
- Permission denied / connection refused errors
- Local passes but CI fails (environment mismatch)

**Prerequisites**:
- Git repo, gh CLI authenticated
- On a branch, no uncommitted changes

**Security**:
- Secret scanning, pre-commit hooks
- No force push to main/master

## Critical Thinking

The command reads actual code, not just comments:

```go
// Copilot comment: "Returns nil on error"
func GetAccounts() ([]Account, error) {
    return []Account{}, err  // Actually returns empty array!
}
```
→ /follow reads implementation to verify behaviour

## Examples

### Example 1: Lint Fix
```
Discovery: 5 golangci-lint failures
Fix: golangci-lint run --fix
Local validation: ✅ Pass
Result: ✅ Fixed in 6 minutes
```

### Example 2: Test Failure
```
Discovery: expected 200, got 500
Analysis: Missing error handling in handler
Fix: Added error check
Local validation: ✅ Pass
Result: ✅ Fixed in 8 minutes
```

### Example 3: Environment Issue (Blockage)
```
Discovery: PostgreSQL connection refused
Iteration 1: Updated config → Still fails
Iteration 2: Added retry → Still fails
Analysis: CI missing postgres service
Local tests pass, CI tests fail
Blockage: Update .github/workflows/test.yml
[Detailed fix instructions provided]
```

## Troubleshooting

**"gh CLI not found"**: `brew install gh && gh auth login`
**Uncommitted changes**: Commit or stash first
**CI timeout**: Check `gh pr checks`, re-run after CI completes
**Local pass, CI fail**: Environment mismatch, needs workflow config

## Performance

**With /follow**: 1-2 iterations, 5-15 min (80%+ auto-fixed)
**Without /follow**: 4-6 iterations, 20-30 min
**Time saved**: 50-60%

## Complex Fix Delegation

When fix requires substantial refactoring:
1. Detect complexity
2. Create mini-story with context
3. Delegate to coder subagent
4. Resume verification after fix

## After Completion

Update `PROGRESS.md`:
- Mark [x] CI/CD phase complete
- Move to next phase or mark complete
