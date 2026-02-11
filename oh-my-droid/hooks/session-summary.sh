#!/bin/bash
# Generate session summary on stop

SESSION_DIR="${HOME}/.factory/sessions"
TIMESTAMP=$(date +%s)

# Get recent commands from history
if [ -f "${HOME}/.factory/bash-command-log.txt" ]; then
    echo "Recent commands:" > "/tmp/summary_${TIMESTAMP}.txt"
    tail -20 "${HOME}/.factory/bash-command-log.txt" >> "/tmp/summary_${TIMESTAMP}.txt" 2>/dev/null || true
fi

echo "Summary generated at $(date)" >> "/tmp/summary_${TIMESTAMP}.txt"
mv "/tmp/summary_${TIMESTAMP}.txt" "${SESSION_DIR}/summary_${TIMESTAMP}.txt" 2>/dev/null || true
