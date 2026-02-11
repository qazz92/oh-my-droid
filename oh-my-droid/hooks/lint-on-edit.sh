#!/bin/bash
# Auto-lint code on write/edit

FILE_PATH="$1"

if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# Get file extension
EXT="${FILE_PATH##*.}"

case "$EXT" in
    ts|js|tsx|jsx)
        if command -v eslint &> /dev/null; then
            npx eslint --quiet --max-warnings=10 "$FILE_PATH" 2>/dev/null || true
        fi
        ;;
    py)
        if command -v flake8 &> /dev/null; then
            flake8 --max-line-length=100 "$FILE_PATH" 2>/dev/null || true
        fi
        ;;
esac
