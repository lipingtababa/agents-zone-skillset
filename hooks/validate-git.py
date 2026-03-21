#!/usr/bin/env python3
"""
Claude Code hook to prevent dangerous git add patterns.
Blocks: git add ., git add -A, git add --all
"""

import json
import sys
import re

def main():
    try:
        # Read input from Claude
        input_data = json.load(sys.stdin)

        # Extract the command from Bash tool input
        tool_input = input_data.get("tool_input", {})
        command = tool_input.get("command", "")

        # Patterns to block
        blocked_patterns = [
            r'\bgit\s+add\s+\.$',          # git add . (only at end of command)
            r'\bgit\s+add\s+\.\s',         # git add . followed by space
            r'\bgit\s+add\s+-A\b',         # git add -A
            r'\bgit\s+add\s+--all\b',      # git add --all
        ]

        # Check if command matches any blocked pattern
        for pattern in blocked_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                # Block the command with clear explanation
                output = {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": (
                            "❌ BLOCKED: 'git add .' and 'git add -A' are not allowed.\n"
                            "Please add specific files instead:\n"
                            "  • git add path/to/file.txt\n"
                            "  • git add *.py\n"
                            "  • git add directory/\n"
                            "This prevents accidentally committing sensitive files or unintended changes."
                        )
                    }
                }
                print(json.dumps(output))
                sys.exit(0)

        # Command is allowed - exit silently
        sys.exit(0)

    except Exception as e:
        # On error, allow the command (fail open)
        # Log error for debugging
        error_output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "error": f"Hook validation error: {str(e)}"
            }
        }
        print(json.dumps(error_output), file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
