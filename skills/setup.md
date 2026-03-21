# Setup Command - Development Environment Setup

## Overview

Sets up git worktrees and development environment for story implementation.

**Note**: This command is OPTIONAL. Use only if you need:
- Git worktrees for parallel development
- Automated environment setup (dependencies, databases)

## When to Use

```bash
/setup S28    # Setup worktree + environment for story S28 (OPTIONAL)
/setup        # Interactive mode

# Many developers skip this and work directly in main repo
```

## What It Does

1. **Story File Lookup** - Finds story file by story ID (e.g., S28)
2. **Git Worktree Setup** - Creates isolated workspace, branch, pushes to remote
3. **Story Validation** - Checks story file exists, validates completeness
4. **Environment Setup** - Checks dependencies, runs setup, starts services, verifies build
5. **Ready to Start** - Generates summary, shows next steps

## Complete Workflow

```
/story → story.md (S28)
  ↓
/setup S28 (OPTIONAL)
  ↓ Finds story, creates worktree + branch
  ↓ Validates story, sets up environment
  ↓
Tester writes tests → /qc → Coder implements → /qc → /follow → Done
```

## Usage Examples

### With Existing Story
```
/setup S28

✅ Found story: S28-feature-name.md
✅ Created worktree: [project]-S28-feature-name
✅ Created branch: S28-feature-name
✅ Story validated, environment ready
Development environment ready!
```

### Working Without /setup (Common)
```
/story → story.md
  ↓ Work directly in main repo (no worktree)
  ↓ Tester → Coder → Done

# /setup only needed for:
# - Parallel work on multiple stories
# - Complex environment automation
```

## Features

**Story Lookup**: Finds story files by ID (e.g., S28)
**Git Worktree Benefits**: Parallel development, isolated environments, easy context switching
**Story Validation**: Checks completeness (requirements, AC)

## Requirements

**Story Files**: Story files should exist in project plans directory (e.g., `plans/`)
**Environment Setup**: Project-specific setup script (optional): `.claude/setup.sh`

## Output Example

```markdown
## Story
✅ Found: plans/S28-feature-name.md
✅ Complete: 4 requirements, 3 AC

## Git Setup
✅ Worktree: [project]-S28-feature-name
✅ Branch: S28-feature-name

## Environment
✅ Dependencies installed
✅ Build successful

## Next Steps
1. Assign to tester subagent
2. Tester writes tests
3. Run /qc to verify
```

## Error Handling

**Story File Lookup**: Story not found → Suggests running /story first, checks common locations
**Git Worktree Errors**: Path too long → Suggests shortening, already exists → Suggests different name/cleanup
**Story Errors**: Missing story → Must run /story first, incomplete → Blocks setup

## Best Practices

1. **Create Story First** - Run /story before /setup
2. **One Story = One Worktree** - Keeps work isolated
3. **Validate Story Before Starting** - Ensures completeness
4. **Setup Environment Automatically** - Catches issues early

## Troubleshooting

- **Story file not found**: Check story file location, run /story first
- **Worktree path too long**: Shorten description
- **Build fails**: Fix dependencies, check project config
- **Database won't start**: Check Docker, ports, logs

## Integration with Other Commands

**/story → /setup**: Story creates story file, setup uses it
**/setup → /qc → /follow**: Full pipeline from setup to CI passing

## Summary

`/setup` is OPTIONAL but useful for:
- Parallel development (worktrees)
- Automated environment validation
- Large teams with complex setups

Most developers can skip it and work directly in main repo.
