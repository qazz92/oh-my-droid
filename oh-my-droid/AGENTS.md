# AGENTS.md - oh-my-droid Plugin Development Guide

> This file is the single source of truth for developing and maintaining the oh-my-droid plugin.
> Read this before making any changes.

---

## 1. Plugin Architecture Overview

oh-my-droid is a **Factory Droid CLI plugin** that provides orchestration, automation, and productivity tools.

```
oh-my-droid/
├── .factory-plugin/
│   └── plugin.json              # Plugin manifest (name, version, description)
├── commands/                     # Slash commands (user-invoked via /command-name)
│   └── oh-my-droid-*.md
├── droids/                       # Custom droids (subagents delegated via Task tool)
│   └── *.md
├── skills/                       # Skills (model-invoked or user-invoked via /skill-name)
│   └── */SKILL.md
├── hooks/                        # Lifecycle hooks (auto-executed at specific events)
│   ├── hooks.json                # Hook event → script mapping
│   └── *.py / *.sh
└── README.md
```

### How the pieces connect

```
User types prompt
  │
  ├─→ hooks/keyword-detector.py (UserPromptSubmit)
  │     detects magic keywords (ralph, autopilot, ultrawork, etc.)
  │     injects skill invocation into context
  │
  ├─→ User types /command-name
  │     commands/*.md resolves to prompt
  │     prompt delegates to a specific droid
  │
  ├─→ Droid invokes Skill tool
  │     skills/*/SKILL.md loaded
  │     skill references droids by name
  │
  └─→ Task tool spawns droid
        droids/*.md defines system prompt, model, tools
        droid executes with isolated context

Lifecycle hooks run at each stage:
  SessionStart  → session-start.py (restore active modes)
  PreToolUse    → pre-tool-enforcer.py (contextual reminders)
  PostToolUse   → post-tool-verifier.py (verify results)
  SubagentStop  → background-manager.py (track completion)
  Stop          → persistent-mode.py (prevent stopping in active modes)
```

---

## 2. Factory Droid Plugin Reference

### 2.1 Plugin Manifest

File: `.factory-plugin/plugin.json`

```json
{
  "name": "oh-my-droid",
  "description": "...",
  "version": "1.0.0"
}
```

Required fields: `name`, `description`, `version`.

### 2.2 Commands (`commands/*.md`)

Commands are user-invoked via `/command-name`. File at `commands/foo.md` becomes `/foo`.

```markdown
---
description: Short description shown in slash suggestions
argument-hint: <optional usage hint>
---

Your prompt here. Use $ARGUMENTS for user input.
```

| Frontmatter | Purpose |
|---|---|
| `description` | Shown in autocomplete |
| `argument-hint` | Usage hint (e.g., `<file or branch>`) |
| `disable-model-invocation` | Set `true` to make user-only |

**Convention**: Our commands are prefixed `oh-my-droid-` (e.g., `oh-my-droid-plan.md` → `/oh-my-droid-plan`).

### 2.3 Droids (`droids/*.md`)

Droids are subagents spawned via the Task tool. File at `droids/foo.md` exposes `subagent_type: "foo"`.

```markdown
---
name: my-droid
description: What this droid does
model: inherit
tools: ["Read", "Edit", "Execute"]
---

You are **my-droid**. Your system prompt here.
```

| Field | Notes |
|---|---|
| `name` | Required. Lowercase, digits, `-`, `_`. |
| `description` | Optional. Shown in UI. Keep under 500 chars. |
| `model` | `inherit` (parent session) or specific model ID. |
| `tools` | Omit for all tools, use category (`read-only`), or explicit array. |
| `reasoningEffort` | Optional. `low`, `medium`, `high`. Ignored when model is `inherit`. |

**Tool categories**:

| Category | Tools |
|---|---|
| `read-only` | Read, LS, Grep, Glob |
| `edit` | Create, Edit, ApplyPatch |
| `execute` | Execute |
| `web` | WebSearch, FetchUrl |

**Available tool IDs (case-sensitive)**: Read, LS, Grep, Glob, Create, Edit, ApplyPatch, Execute, WebSearch, FetchUrl, TodoWrite (auto-included).

### 2.4 Skills (`skills/*/SKILL.md`)

Skills are capabilities invoked by the model or user (`/skill-name`).

```markdown
---
name: my-skill
description: When to use this skill. Model uses this to decide.
---

Skill instructions here.
```

| Field | Required | Default | Description |
|---|---|---|---|
| `name` | No | Directory name | Display name |
| `description` | Recommended | -- | When to use (model reads this) |
| `user-invocable` | No | `true` | `false` hides from / menu |
| `disable-model-invocation` | No | `false` | `true` prevents auto-invocation |

Skills can reference droids by name. The model will use the Task tool to spawn them.

### 2.5 Hooks (`hooks/hooks.json`)

Hooks are lifecycle scripts that run at specific events.

```json
{
  "description": "Hook description",
  "hooks": {
    "EventName": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"${DROID_PLUGIN_ROOT}/hooks/script.py\"",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

**Environment variables**:
- `${DROID_PLUGIN_ROOT}` - Absolute path to plugin directory
- `${FACTORY_PROJECT_DIR}` - Project root directory

**Hook events**:

| Event | When | Matcher | Can Block? |
|---|---|---|---|
| `UserPromptSubmit` | User submits prompt | N/A | Yes (exit 2 or JSON) |
| `SessionStart` | Session begins/resumes | `startup`, `resume`, `clear`, `compact` | No |
| `PreToolUse` | Before tool execution | Tool name (e.g., `Edit\|Write`) | Yes |
| `PostToolUse` | After tool execution | Tool name | Feedback only |
| `SubagentStop` | Sub-droid task completes | `*` | Yes |
| `Stop` | Droid finishes responding | `*` | Yes (block = continue) |
| `PreCompact` | Before context compact | `manual`, `auto` | No |
| `SessionEnd` | Session ends | N/A | No |
| `Notification` | Droid sends notification | N/A | No |

**Hook I/O**:
- **Input**: JSON via stdin (contains `session_id`, `cwd`, `hook_event_name`, event-specific fields)
- **Output**: Exit code (0=ok, 2=block) OR JSON stdout

**JSON output format**:
```json
{
  "continue": true,
  "hookSpecificOutput": {
    "hookEventName": "EventName",
    "additionalContext": "Text injected into context"
  }
}
```

To suppress output: `{"continue": true, "suppressOutput": true}`

**Stop hook** - to prevent stopping:
```json
{
  "decision": "block",
  "reason": "Must continue: task not complete"
}
```

---

## 3. Current oh-my-droid Configuration

### 3.1 Droids (19 total)

| Droid | Complexity | Tools | Role |
|---|---|---|---|
| `orchestrator` | Very High | Read, Edit, Execute, TodoWrite, Task | Task breakdown, delegation, parallel execution |
| `executor-low` | Low | Read, Write, Edit | Simple code modifications |
| `executor-med` | Medium | Read, Write, Edit, Execute, Grep, Glob | Implementation, fix, debug (default) |
| `executor-high` | High | Read, Write, Edit, Execute, Create | Complex implementation |
| `basic-searcher` | Low | Read, Glob, Grep | File/pattern search |
| `basic-reader` | Low | Read | Code reading/explanation |
| `hephaestus` | Very High | Read, Write, Edit, Execute, Grep, Glob, Create | Architecture, system design |
| `prometheus` | High | Read, TodoWrite | Strategic planning |
| `metis` | High | Read, Grep | Pre-planning analysis |
| `momus` | High | Read, TodoWrite | Plan validation, QA |
| `oracle` | High | Read, Grep, WebSearch | Debugging, consultation |
| `code-reviewer` | Medium | Read, Grep, Glob | Code review |
| `security-auditor` | Medium | Read, Grep, WebSearch | Security analysis |
| `explore` | Low | Read, Grep, Glob | Fast code search |
| `explorer` | Low | Read, Grep, Glob | Fast code exploration |
| `librarian` | Medium | Read, Grep, WebSearch, FetchUrl | Research specialist |
| `test-engineer` | Medium | Read, Edit, Execute | Test creation |
| `verifier` | Medium | Read, Execute, Grep | Validation/verification |
| `docs-writer` | Medium | Read, Edit | Documentation |

### 3.2 Commands (21 total)

| Command | Delegates To | Purpose |
|---|---|---|
| `/oh-my-droid-autopilot` | skill:autopilot | Fully autonomous: plan → execute → review → fix |
| `/oh-my-droid-ralph` | skill:ralph | Persistent verify/fix loops (max 3 attempts) |
| `/oh-my-droid-ultrawork` | skill:ultrawork | Maximum parallel execution |
| `/oh-my-droid-ecomode` | skill:ecomode | Token-efficient execution |
| `/oh-my-droid-pipeline` | skill:pipeline | Sequential staged execution |
| `/oh-my-droid-plan` | prometheus | Strategic planning |
| `/oh-my-droid-review` | momus | Plan validation |
| `/oh-my-droid-orchestrator` | orchestrator | Execute approved plan |
| `/oh-my-droid-analyze` | metis | Pre-planning analysis |
| `/oh-my-droid-explore` | explore | Codebase search |
| `/oh-my-droid-debug` | oracle | Debugging/guidance |
| `/oh-my-droid-deep-work` | hephaestus | Complex autonomous task |
| `/oh-my-droid-research` | librarian | Documentation research |
| `/oh-my-droid-code-review` | (inline) | Code review checklist |
| `/oh-my-droid-refactor` | (inline) | Safe refactoring |
| `/oh-my-droid-security` | security-auditor | Security audit |
| `/oh-my-droid-test` | test-engineer | Test generation |
| `/oh-my-droid-validate` | momus | Gap/risk validation |
| `/oh-my-droid-write-docs` | docs-writer | Documentation generation |
| `/oh-my-droid-session-summary` | (inline) | Session summary |
| `/oh-my-droid-task-bg` | skill:task-bg | Background task launch |

### 3.3 Skills (17 total)

| Skill | Type | Description |
|---|---|---|
| `autopilot` | Orchestration | Full autonomous: plan → execute → review → fix |
| `ralph` | Orchestration | Persistent verify/fix loops (max 3 attempts) |
| `ultrawork` | Orchestration | Maximum parallel execution |
| `ecomode` | Orchestration | Token-efficient execution |
| `pipeline` | Orchestration | Sequential staged execution |
| `task-bg` | Utility | Background task launcher |
| `browser-automation` | Utility | Web browser automation |
| `code-cleanup` | Utility | Linting, formatting, dead code |
| `continuous-learning` | Utility | Self-improvement |
| `documentation` | Utility | Doc generation |
| `git-master` | Utility | Git operations |
| `human-writing` | Utility | Natural writing style |
| `security-scanner` | Utility | Secret/vuln scanning |
| `session-navigation` | Utility | Session management |
| `skill-creation` | Utility | Generate new skills |
| `test-automation` | Utility | Test generation |
| `visual-design` | Utility | UI/UX design |

### 3.4 Hooks (6 active)

| Event | Script | Role |
|---|---|---|
| `UserPromptSubmit` | `keyword-detector.py` | Detect keywords → invoke skills |
| `SessionStart` | `session-start.py` | Restore active modes (ralph/ultrawork/autopilot) |
| `PreToolUse` | `pre-tool-enforcer.py` | Todo status + tool-specific reminders |
| `PostToolUse` | `post-tool-verifier.py` | Failure detection + verification guidance |
| `SubagentStop` | `background-manager.py` | Background task completion tracking |
| `Stop` | `persistent-mode.py` | Prevent stopping in active modes |

### 3.5 Supporting Scripts

| Script | Purpose |
|---|---|
| `intelligent-router.py` | AI + keyword hybrid routing to select best droid |
| `state-manager.py` | Task state tracking (create, update, complete) |
| `background-manager.py` | Background task lifecycle management |
| `format-on-write.sh` | Auto-format on file write |
| `lint-on-edit.sh` | Auto-lint on file edit |
| `protect-files.sh` | Block edits to sensitive files |
| `notification.sh` | Desktop notifications |
| `session-summary.sh` | Session summary generation |

---

## 4. Key Workflows

### 4.1 Autopilot (fully autonomous)

```
User: "autopilot build a REST API"
  ↓
keyword-detector.py detects "autopilot"
  ↓
Injects: Skill tool → autopilot/SKILL.md
  ↓
Autopilot skill: analyze → plan → execute → review → fix
  ↓
Spawns droids: executor-med, verifier, etc. via Task tool
  ↓
persistent-mode.py prevents stopping until complete
```

### 4.2 Orchestrator (user-controlled)

```
User: /oh-my-droid-plan "design a caching layer"
  → prometheus droid creates strategic plan

User: /oh-my-droid-review
  → momus droid validates the plan

User: /oh-my-droid-orchestrator "execute the approved plan"
  → orchestrator droid delegates subtasks to appropriate droids
```

### 4.3 Ralph (persistent execution)

```
User: "ralph fix all test failures"
  ↓
keyword-detector.py detects "ralph"
  ↓
ralph/SKILL.md: execute → verify → fix loop (max 3x)
  ↓
persistent-mode.py blocks stopping until verified complete
```

---

## 5. Development Guide

### 5.1 Adding a New Droid

1. Create `droids/<name>.md` with YAML frontmatter
2. Set `name`, `description`, `model`, `tools`
3. Write the system prompt body
4. Reference the droid in relevant commands/skills

```markdown
---
name: my-new-droid
description: What it does (under 500 chars)
model: inherit
tools: ["Read", "Edit", "Execute"]
---

You are **my-new-droid**. Your instructions here.
```

### 5.2 Adding a New Command

1. Create `commands/oh-my-droid-<name>.md`
2. Add `description` frontmatter
3. Delegate to a droid or write inline prompt
4. Use `$ARGUMENTS` for user input

```markdown
---
description: What /oh-my-droid-<name> does
argument-hint: <what user should provide>
---

Delegate this to the **<droid-name>** droid.

Task: $ARGUMENTS
```

### 5.3 Adding a New Skill

1. Create `skills/<name>/SKILL.md`
2. Add `name` and `description` frontmatter
3. Write skill instructions referencing droids by name
4. If keyword-activated, add detection pattern to `keyword-detector.py`

```markdown
---
name: my-skill
description: Use when <trigger condition>. Does <what>.
---

You are **my-skill**. Instructions here.
Reference droids: executor-med, verifier, etc.
```

### 5.4 Adding a New Hook

1. Create the script in `hooks/` (Python preferred)
2. Script reads JSON from stdin, outputs JSON to stdout
3. Register in `hooks/hooks.json`

```python
#!/usr/bin/env python3
import json, sys

def main():
    try:
        data = json.loads(sys.stdin.read())
        # Your logic here
        print(json.dumps({
            "continue": True,
            "hookSpecificOutput": {
                "hookEventName": "EventName",
                "additionalContext": "your message"
            }
        }))
    except Exception:
        print(json.dumps({"continue": True, "suppressOutput": True}))

if __name__ == "__main__":
    main()
```

Register in `hooks/hooks.json`:
```json
{
  "EventName": [{
    "matcher": "*",
    "hooks": [{
      "type": "command",
      "command": "python3 \"${DROID_PLUGIN_ROOT}/hooks/my-hook.py\"",
      "timeout": 5
    }]
  }]
}
```

### 5.5 Testing Locally

```bash
# Install from local directory
droid plugin marketplace add /path/to/oh-my-droid-marketplace
droid plugin install oh-my-droid@oh-my-droid --scope user

# Test a command
# Type /oh-my-droid-plan "my task" in a droid session

# Test a hook script directly
echo '{"prompt":"autopilot build API","cwd":"/tmp"}' | python3 hooks/keyword-detector.py
```

### 5.6 Validation Checklist

Before committing changes:

- [ ] All `.md` files have required YAML frontmatter (`name` for droids/skills, `description` for commands)
- [ ] All Python scripts pass syntax check: `python3 -m py_compile hooks/script.py`
- [ ] No hardcoded absolute paths (use `${DROID_PLUGIN_ROOT}` in hooks.json)
- [ ] No "agent" terminology - use "droid" consistently
- [ ] Droid names are lowercase with hyphens (e.g., `executor-med`, not `executor/med`)
- [ ] Tool names in droid frontmatter are case-sensitive and valid (Read, Edit, Execute, etc.)
- [ ] hooks.json is valid JSON
- [ ] New droids referenced by commands/skills actually exist in `droids/`

---

## 6. Naming Conventions

| Component | Convention | Example |
|---|---|---|
| Droid names | lowercase-hyphen | `executor-med`, `basic-reader` |
| Command files | `oh-my-droid-<name>.md` | `oh-my-droid-plan.md` |
| Skill dirs | lowercase-hyphen | `skills/autopilot/SKILL.md` |
| Hook scripts | lowercase-hyphen.py | `keyword-detector.py` |
| Terminology | Always "droid", never "agent" | "Spawning droid: executor-med" |

---

## 7. State Management

oh-my-droid uses `.omd/state/` for persistent state across sessions.

```
.omd/
├── state/
│   ├── ralph-state.json          # Active ralph mode
│   ├── autopilot-state.json      # Active autopilot mode
│   ├── ultrawork-state.json      # Active ultrawork mode
│   ├── subagent-tracking.json    # Running droid tracker
│   └── sessions/
│       └── <session-id>/
│           └── *-state.json      # Session-scoped state
└── todos.json                    # Pending tasks
```

State is managed by:
- `keyword-detector.py` - Creates state when mode activated
- `session-start.py` - Restores state on session start
- `persistent-mode.py` - Reads state to decide if stopping is allowed
- `state-manager.py` - General-purpose CRUD for task state

---

## 8. Quick Reference Links

- [Building Plugins](https://docs.factory.ai/guides/building/building-plugins)
- [Custom Droids](https://docs.factory.ai/cli/configuration/custom-droids)
- [Skills](https://docs.factory.ai/cli/configuration/skills)
- [Custom Slash Commands](https://docs.factory.ai/cli/configuration/custom-slash-commands)
- [Hooks Guide](https://docs.factory.ai/cli/configuration/hooks-guide)
- [Hooks Reference](https://docs.factory.ai/reference/hooks-reference)
