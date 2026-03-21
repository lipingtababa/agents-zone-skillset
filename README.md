# Agents Zone Skillset

A collection of Claude Code agents, skills, and commands for TDD-driven AI development workflows.

## What's Inside

### Agents (Subagent Definitions)
- `agents/coder.md` - TDD Green phase: implements code to make tests pass
- `agents/tester.md` - TDD Red phase: writes failing tests from story requirements

### Skills (Reusable Capabilities)
- `skills/qc.md` - Quality Control auditor: verifies tester/coder claims against reality
- `skills/follow.md` - CI/CD self-healing: monitors GitHub Actions and auto-fixes failures
- `skills/auto_qc.md` - Auto-trigger QC after subagent completion

### Commands (User-Facing Workflows)
- `commands/architect.md` - Architecture design from PRD requirements
- `commands/prd.md` - Research-first PRD creation
- `commands/story.md` - Hyper-detailed developer stories for TDD
- `commands/conduct.md` - Workflow orchestration (resume from PROGRESS.md)
- `commands/qc.md` - Quality control checker (user-facing docs)
- `commands/follow.md` - CI/CD self-healing (user-facing docs)
- `commands/setup.md` - Development environment setup
- `commands/mentor.md` - Lesson router for embedding knowledge into docs

### Templates
- `templates/architecture.md` - Architecture document template
- `templates/prd.md` - Product Requirements Document template
- `templates/progress.md` - Progress tracking template

### Hooks
- `hooks/validate-git.py` - Prevents dangerous `git add .` commands

## How to Use

1. Copy agents/skills/commands to your `~/.claude/` directory
2. Reference them in your `CLAUDE.md` or `settings.json`
3. Customise paths and project-specific details

## TDD Workflow

```
/prd → /architect → /story → tester → coder → /qc → /follow → Done
```

Each phase builds on the previous, with quality gates at every step.

## Philosophy

- **Test-Driven Development**: Write tests first, implement second
- **Quality Gates**: Auto-QC after every phase completion
- **Autonomous Agents**: Subagents work independently with full context
- **Single Source of Truth**: Story file contains everything tester/coder needs
- **No Timelines**: Focus on what to build, not when

## Licence

MIT
