#!/usr/bin/env bash
# install.sh — Copy the generate_prompts package into another project.
#
# Usage:
#   ./install.sh /path/to/target/project
#
# This copies the generate_prompts/ package directory and .env.example
# into the target project so it can be used as a local library:
#
#   from generate_prompts import PromptConfig, generate_example_prompts, extend_prompt
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="$SCRIPT_DIR/generate_prompts"

if [ $# -lt 1 ]; then
    echo "Usage: $0 <target-project-dir>"
    echo ""
    echo "Copies the generate_prompts package into the target project."
    exit 1
fi

TARGET="$1"

if [ ! -d "$TARGET" ]; then
    echo "Error: target directory '$TARGET' does not exist."
    exit 1
fi

# Copy the package
echo "Copying generate_prompts/ -> $TARGET/generate_prompts/"
rm -rf "$TARGET/generate_prompts"
cp -r "$PACKAGE_DIR" "$TARGET/generate_prompts"

# Remove any __pycache__ from the copy
find "$TARGET/generate_prompts" -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

# Copy .env.example if it doesn't already exist in target
if [ ! -f "$TARGET/.env.example" ]; then
    echo "Copying .env.example -> $TARGET/.env.example"
    cp "$SCRIPT_DIR/.env.example" "$TARGET/.env.example"
else
    echo "Skipping .env.example (already exists in target)"
fi

echo ""
echo "Done! You can now import from the package:"
echo "  from generate_prompts import PromptConfig, generate_example_prompts, extend_prompt"
echo ""
echo "Make sure python-dotenv is installed: pip install python-dotenv"
