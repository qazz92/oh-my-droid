#!/bin/bash
# Block edits to protected files

FILE_PATH="$1"

if [ -z "$FILE_PATH" ]; then
    exit 0
fi

# Protected patterns
PROTECTED=(
    ".env"
    "package-lock.json"
    "yarn.lock"
    ".git/"
    "node_modules/"
    "dist/"
    "build/"
)

for pattern in "${PROTECTED[@]}"; do
    if echo "$FILE_PATH" | grep -q "$pattern"; then
        echo "ERROR: Protected file modification blocked: $FILE_PATH" >&2
        exit 1
    fi
done

exit 0
