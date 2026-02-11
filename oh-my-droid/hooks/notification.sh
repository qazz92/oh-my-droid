#!/bin/bash
# Notify on notification events

MESSAGE="$1"

if command -v notify-send &> /dev/null; then
    notify-send "Droid" "$MESSAGE" 2>/dev/null || true
elif command -v osascript &> /dev/null; then
    osascript -e "display notification \"$MESSAGE\" with title \"Droid\"" 2>/dev/null || true
fi
