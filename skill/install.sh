#!/usr/bin/env bash
# install.sh — Install the add-prompt-slots Claude Code skill.
#
# Usage:
#   ./skill/install.sh
#
#   Or from anywhere:
#   curl -fsSL https://raw.githubusercontent.com/dw-flyingw/prompt-slots/master/skill/install.sh | bash
#
# Copies the SKILL.md into ~/.claude/skills/add-prompt-slots/ so Claude Code
# can discover and use it. After install, invoke with:
#
#   /add-prompt-slots
#
# Or just describe what you need:
#   "Add example prompts to this app"
#
set -euo pipefail

SKILL_DIR="$HOME/.claude/skills/add-prompt-slots"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd 2>/dev/null)" || SCRIPT_DIR=""

# Check if running from local repo or needs to fetch from GitHub
if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/SKILL.md" ]; then
    SOURCE="$SCRIPT_DIR/SKILL.md"
else
    # Fetch from GitHub
    TMPDIR="$(mktemp -d)"
    trap 'rm -rf "$TMPDIR"' EXIT
    REPO="https://github.com/dw-flyingw/prompt-slots.git"
    echo "Fetching skill from $REPO..."
    git clone --depth 1 --branch master "$REPO" "$TMPDIR/prompt-slots" 2>/dev/null
    SOURCE="$TMPDIR/prompt-slots/skill/SKILL.md"
fi

if [ ! -f "$SOURCE" ]; then
    echo "Error: SKILL.md not found at $SOURCE"
    exit 1
fi

mkdir -p "$SKILL_DIR"
cp "$SOURCE" "$SKILL_DIR/SKILL.md"

echo "Installed add-prompt-slots skill to $SKILL_DIR"
echo ""
echo "The skill is now available in Claude Code. Use it by:"
echo "  - Saying: \"Add example prompts to this app\""
echo "  - Or invoking: /add-prompt-slots"
