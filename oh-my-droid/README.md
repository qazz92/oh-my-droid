# oh-my-droid

Factory CLI optimization plugin with productivity tools and automation.

## Quick Start

```bash
# Add marketplace
droid plugin marketplace add https://github.com/qazz92/oh-my-droid

# Install plugin
droid plugin install oh-my-droid@oh-my-droid --scope user
```

## Usage

```bash
# Auto-route task to best droid
/oh-my-droid-autopilot "fix authentication bug"

# Persistent execution with verify/fix loops (max 3 attempts)
/oh-my-droid-ralph "build a REST API"

# Maximum parallel execution
/oh-my-droid-ultrawork "fix all errors in codebase"

# Token-efficient execution
/oh-my-droid-ecomode "explain how this works"

# Sequential staged execution
/oh-my-droid-pipeline "build, test, and deploy"
```

## Commands

| Command | Description |
|---------|-------------|
| `/oh-my-droid-autopilot` | Auto-route and execute with best droid |
| `/oh-my-droid-ralph` | Persistent execution with verify/fix loops |
| `/oh-my-droid-ultrawork` | Maximum parallel execution |
| `/oh-my-droid-ecomode` | Token-efficient execution |
| `/oh-my-droid-pipeline` | Sequential staged execution |

## Skills

| Skill | Description |
|-------|-------------|
| `autopilot` | Auto-route and execute autonomously |
| `ralph` | Persistent verify/fix loops |
| `ultrawork` | Maximum parallel task execution |
| `ecomode` | Token-conscious execution |
| `pipeline` | Multi-stage execution |

## Droids

| Droid | Complexity | Description |
|-------|-----------|-------------|
| `orchestrator` | Very High | Task breakdown and delegation |
| `executor-low` | Low | Simple changes |
| `executor-med` | Medium | Implementation/fix/debug |
| `executor-high` | High | Complex implementation |
| `basic-searcher` | Low | Simple file search |
| `basic-reader` | Low | Code reading/explanation |
| `hephaestus` | Very High | Complex architecture |
| `prometheus` | High | Strategic planning |
| `metis` | High | Pre-planning analysis |
| `momus` | High | Plan validation |
| `oracle` | High | Debugging expert |
| `code-reviewer` | Medium | Code review |
| `security-auditor` | Medium | Security review |
| `explorer` | Low | Fast code search |
| `librarian` | Medium | Research specialist |
| `test-engineer` | Medium | Test creation |
| `verifier` | Medium | Validation/verification |
| `docs-writer` | Medium | Documentation |

## Structure

```
oh-my-droid/
├── commands/                 # User commands (*.md)
├── skills/                  # AI skills (*/SKILL.md)
├── droids/                  # Droid definitions (*.md)
├── hooks/                   # Hook scripts
│   ├── hooks.json
│   ├── intelligent-router.py
│   ├── state-manager.py
│   ├── background-manager.py
│   └── *.sh
└── README.md
```

## Hooks Configuration

Hooks are automatically loaded from the plugin:

```json
{
  "PreToolUse": [
    { "matcher": "Edit|Write", "hooks": [
      { "type": "command", "command": "${DROID_PLUGIN_ROOT}/hooks/protect-files.sh ${file_path}" },
      { "type": "command", "command": "${DROID_PLUGIN_ROOT}/hooks/format-on-write.sh ${file_path}" }
    ]}
  ],
  "PostToolUse": [
    { "matcher": "Edit|Write", "hooks": [
      { "type": "command", "command": "${DROID_PLUGIN_ROOT}/hooks/lint-on-edit.sh ${file_path}" }
    ]}
  ],
  "Stop": [
    { "matcher": "", "hooks": [
      { "type": "command", "command": "${DROID_PLUGIN_ROOT}/hooks/session-summary.sh" }
    ]}
  ]
}
```

Use `${DROID_PLUGIN_ROOT}` to reference plugin files.
