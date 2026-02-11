#!/bin/bash
# Auto-format code on write/edit

FILE_PATH="$1"

if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# Get file extension
EXT="${FILE_PATH##*.}"

case "$EXT" in
    ts|js|tsx|jsx)
        if command -v prettier &> /dev/null; then
            npx prettier --write "$FILE_PATH" 2>/dev/null || true
        fi
        ;;
    py)
        if command -v black &> /dev/null; then
            black --fast "$FILE_PATH" 2>/dev/null || true
        fi
        ;;
    json)
        if command -v jq &> /dev/null; then
            jq -S . "$FILE_PATH" > "${FILE_PATH}.tmp" 2>/dev/null && mv "${FILE_PATH}.tmp" "$FILE_PATH" || true
        fi
        ;;
    md)
        if command -v prettier &> /dev/null; then
            npx prettier --write "$FILE_PATH" 2>/dev/null || true
        fi
        ;;
esac
