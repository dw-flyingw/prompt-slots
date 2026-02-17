#!/usr/bin/env bash
# install.sh — Pull the generate_prompts package from GitHub into a project.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/dw-flyingw/prompt-slots/main/install.sh | bash -s /path/to/project
#
#   Or clone the repo first and run locally:
#   ./install.sh /path/to/project
#
# This fetches the generate_prompts/ package and .env.example so you
# can use it as a local library:
#
#   from generate_prompts import PromptConfig, generate_example_prompts, extend_prompt
#
set -euo pipefail

REPO="https://github.com/dw-flyingw/prompt-slots.git"
BRANCH="main"

if [ $# -lt 1 ]; then
    echo "Usage: $0 <target-project-dir>"
    echo ""
    echo "Pulls the generate_prompts package from GitHub into the target project."
    exit 1
fi

TARGET="$1"

if [ ! -d "$TARGET" ]; then
    echo "Error: target directory '$TARGET' does not exist."
    exit 1
fi

# Create a temporary directory for the clone
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

echo "Fetching prompt-slots from $REPO ($BRANCH)..."
git clone --depth 1 --branch "$BRANCH" "$REPO" "$TMPDIR/prompt-slots" 2>/dev/null

# Copy the package
echo "Copying generate_prompts/ -> $TARGET/generate_prompts/"
rm -rf "$TARGET/generate_prompts"
cp -r "$TMPDIR/prompt-slots/generate_prompts" "$TARGET/generate_prompts"

# Remove any __pycache__ from the copy
find "$TARGET/generate_prompts" -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

# Copy .env.example if it doesn't already exist in target
if [ ! -f "$TARGET/.env.example" ]; then
    echo "Copying .env.example -> $TARGET/.env.example"
    cp "$TMPDIR/prompt-slots/.env.example" "$TARGET/.env.example"
else
    echo "Skipping .env.example (already exists in target)"
fi

echo ""
echo "Done! You can now import from the package:"
echo "  from generate_prompts import PromptConfig, generate_example_prompts, extend_prompt"
echo ""
echo "Make sure python-dotenv is installed: pip install python-dotenv"
