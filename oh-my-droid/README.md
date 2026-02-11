# oh-my-droid

Factory CLI optimization plugin with productivity tools and automation.

## Features

### Commands

| Command | Description |
|---------|-------------|
| `/code-review` | Comprehensive code review |
| `/refactor` | Systematic code refactoring |
| `/session-summary` | Generate session summaries |

### Skills

| Skill | Description |
|-------|-------------|
| `code-cleanup` | Automated code cleanup |
| `test-automation` | Test generation |
| `documentation` | Documentation generation |
| `security-scanner` | Security scanning |
| `git-master` | Git expertise |
| `browser-automation` | Browser automation |
| `visual-design` | UI/UX design |
| `skill-creation` | Skill generation |
| `human-writing` | Natural writing |
| `session-navigation` | Session management |
| `continuous-learning` | Self-improvement |

### Droids

| Droid | Description |
|-------|-------------|
| `code-reviewer` | Focused code reviewer |
| `security-auditor` | Security analysis |
| `test-engineer` | Testing workflows |
| `docs-writer` | Documentation |
| `sisyphus` | Task orchestrator |
| `oracle` | Debugging expert |
| `librarian` | Research specialist |
| `explore` | Fast code search |
| `prometheus` | Strategic planning |
| `metis` | Pre-planning analysis |
| `momus` | Plan validation |
| `atlas` | Session orchestrator |
| `hephaestus` | Deep coder |

### Hooks

| Hook Script | Description |
|------------|-------------|
| `format-on-write.sh` | Auto-format code on save |
| `lint-on-edit.sh` | Auto-lint code on edit |
| `session-summary.sh` | Generate session summaries |
| `notification.sh` | Desktop notifications |
| `protect-files.sh` | Block protected files |

## Installation

```bash
# Add marketplace
droid plugin marketplace add /Users/rokhun/dev/oh-my-droid

# Install plugin
droid plugin install oh-my-droid@oh-my-droid --scope user
```

## Hooks Setup

Hooks are automatically loaded from the plugin. The hooks.json includes:

```json
{
  "PreToolUse": [
    {
      "matcher": "Edit|Write",
      "hooks": [
        {
          "type": "command",
          "command": "${DROID_PLUGIN_ROOT}/hooks/protect-files.sh ${file_path}"
        },
        {
          "type": "command",
          "command": "${DROID_PLUGIN_ROOT}/hooks/format-on-write.sh ${file_path}"
        }
      ]
    }
  ],
  "PostToolUse": [
    {
      "matcher": "Edit|Write",
      "hooks": [
        {
          "type": "command",
          "command": "${DROID_PLUGIN_ROOT}/hooks/lint-on-edit.sh ${file_path}"
        }
      ]
    }
  ],
  "Stop": [
    {
      "matcher": "",
      "hooks": [
        {
          "type": "command",
          "command": "${DROID_PLUGIN_ROOT}/hooks/session-summary.sh"
        }
      ]
    }
  ],
  "Notification": [
    {
      "matcher": "",
      "hooks": [
        {
          "type": "command",
          "command": "${DROID_PLUGIN_ROOT}/hooks/notification.sh ${notification_message}"
        }
      ]
    }
  ]
}
```

Use `${DROID_PLUGIN_ROOT}` to reference plugin files - this is automatically expanded.

## Structure

```
oh-my-droid/
├── .factory-plugin/plugin.json
├── commands/
├── skills/
├── droids/
├── hooks/
│   ├── hooks.json
│   ├── format-on-write.sh
│   ├── lint-on-edit.sh
│   ├── session-summary.sh
│   ├── notification.sh
│   └── protect-files.sh
└── README.md
```
