#!/usr/bin/env python3
"""
Project Memory for oh-my-droid

Auto-detects project environment (languages, frameworks, build commands,
conventions) and persists to .omd/project-memory.json.
Provides context injection for SessionStart, learning from PostToolUse,
and state preservation for PreCompact.

Equivalent to oh-my-claudecode's project-memory system.
"""

import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Optional

OMD_DIR = ".omd"
MEMORY_FILE = "project-memory.json"
NOTEPAD_FILE = "notepad.md"
CACHE_EXPIRY_SECONDS = 3600  # 1 hour

# --- Detection ---

CONFIG_PATTERNS = {
    "package.json": {"language": "javascript", "packageManager": "npm"},
    "yarn.lock": {"packageManager": "yarn"},
    "pnpm-lock.yaml": {"packageManager": "pnpm"},
    "bun.lockb": {"packageManager": "bun"},
    "tsconfig.json": {"language": "typescript"},
    "pyproject.toml": {"language": "python"},
    "setup.py": {"language": "python"},
    "requirements.txt": {"language": "python", "packageManager": "pip"},
    "Pipfile": {"language": "python", "packageManager": "pipenv"},
    "poetry.lock": {"language": "python", "packageManager": "poetry"},
    "Cargo.toml": {"language": "rust", "packageManager": "cargo"},
    "go.mod": {"language": "go"},
    "Gemfile": {"language": "ruby", "packageManager": "bundler"},
    "build.gradle": {"language": "java", "packageManager": "gradle"},
    "build.gradle.kts": {"language": "kotlin", "packageManager": "gradle"},
    "pom.xml": {"language": "java", "packageManager": "maven"},
    "pubspec.yaml": {"language": "dart", "packageManager": "pub"},
    "Makefile": {},
    "Dockerfile": {},
    "docker-compose.yml": {},
    "docker-compose.yaml": {},
    ".env": {},
    ".env.example": {},
}

FRAMEWORK_MARKERS = {
    "next.config.js": {"name": "Next.js", "category": "fullstack"},
    "next.config.mjs": {"name": "Next.js", "category": "fullstack"},
    "next.config.ts": {"name": "Next.js", "category": "fullstack"},
    "nuxt.config.ts": {"name": "Nuxt", "category": "fullstack"},
    "svelte.config.js": {"name": "SvelteKit", "category": "fullstack"},
    "angular.json": {"name": "Angular", "category": "frontend"},
    "vite.config.ts": {"name": "Vite", "category": "build"},
    "vite.config.js": {"name": "Vite", "category": "build"},
    "webpack.config.js": {"name": "Webpack", "category": "build"},
    "tailwind.config.js": {"name": "Tailwind CSS", "category": "frontend"},
    "tailwind.config.ts": {"name": "Tailwind CSS", "category": "frontend"},
    "jest.config.js": {"name": "Jest", "category": "testing"},
    "jest.config.ts": {"name": "Jest", "category": "testing"},
    "vitest.config.ts": {"name": "Vitest", "category": "testing"},
    "pytest.ini": {"name": "pytest", "category": "testing"},
    "setup.cfg": {"name": "setuptools", "category": "build"},
    "manage.py": {"name": "Django", "category": "backend"},
    "app.py": {"name": "Flask", "category": "backend"},
    "fastapi": {"name": "FastAPI", "category": "backend"},
    "Procfile": {"name": "Heroku", "category": "build"},
    "serverless.yml": {"name": "Serverless", "category": "build"},
    "prisma": {"name": "Prisma", "category": "backend"},
    ".eslintrc.json": {"name": "ESLint", "category": "build"},
    ".eslintrc.js": {"name": "ESLint", "category": "build"},
    "eslint.config.js": {"name": "ESLint", "category": "build"},
    ".prettierrc": {"name": "Prettier", "category": "build"},
}


def detect_project_environment(project_root: str) -> dict:
    root = Path(project_root)
    memory = {
        "version": "1.0.0",
        "lastScanned": int(time.time()),
        "projectRoot": project_root,
        "techStack": {
            "languages": [],
            "frameworks": [],
            "packageManager": None,
            "runtime": None,
        },
        "build": {
            "buildCommand": None,
            "testCommand": None,
            "lintCommand": None,
            "devCommand": None,
            "scripts": {},
        },
        "conventions": {
            "namingStyle": None,
            "importStyle": None,
            "testPattern": None,
            "fileOrganization": None,
        },
        "structure": {
            "isMonorepo": False,
            "workspaces": [],
            "mainDirectories": [],
        },
        "hotPaths": [],
        "userDirectives": [],
    }

    languages = set()
    frameworks = []
    pkg_manager = None

    # Detect from config files
    for filename, indicators in CONFIG_PATTERNS.items():
        if (root / filename).exists():
            if "language" in indicators:
                languages.add(indicators["language"])
            if "packageManager" in indicators:
                pkg_manager = indicators["packageManager"]

    # Detect frameworks
    for filename, info in FRAMEWORK_MARKERS.items():
        if (root / filename).exists():
            frameworks.append(info)

    # Parse package.json for scripts + dependencies
    pkg_json_path = root / "package.json"
    if pkg_json_path.exists():
        try:
            pkg = json.loads(pkg_json_path.read_text())
            scripts = pkg.get("scripts", {})
            memory["build"]["scripts"] = scripts
            memory["build"]["buildCommand"] = _find_script(scripts, ["build"])
            memory["build"]["testCommand"] = _find_script(scripts, ["test", "test:unit"])
            memory["build"]["lintCommand"] = _find_script(scripts, ["lint", "lint:fix"])
            memory["build"]["devCommand"] = _find_script(scripts, ["dev", "start:dev", "serve"])

            # Detect frameworks from dependencies
            all_deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            for dep, framework in [
                ("react", {"name": "React", "category": "frontend"}),
                ("vue", {"name": "Vue", "category": "frontend"}),
                ("svelte", {"name": "Svelte", "category": "frontend"}),
                ("express", {"name": "Express", "category": "backend"}),
                ("fastify", {"name": "Fastify", "category": "backend"}),
                ("nestjs", {"name": "NestJS", "category": "backend"}),
                ("@nestjs/core", {"name": "NestJS", "category": "backend"}),
            ]:
                if dep in all_deps:
                    if not any(f["name"] == framework["name"] for f in frameworks):
                        frameworks.append(framework)

            # Detect monorepo
            if "workspaces" in pkg:
                memory["structure"]["isMonorepo"] = True
                ws = pkg["workspaces"]
                memory["structure"]["workspaces"] = ws if isinstance(ws, list) else ws.get("packages", [])
        except (json.JSONDecodeError, KeyError):
            pass

    # Parse pyproject.toml for scripts
    pyproject_path = root / "pyproject.toml"
    if pyproject_path.exists():
        try:
            content = pyproject_path.read_text()
            if "pytest" in content:
                memory["build"]["testCommand"] = "pytest"
                if not any(f["name"] == "pytest" for f in frameworks):
                    frameworks.append({"name": "pytest", "category": "testing"})
            if "ruff" in content:
                memory["build"]["lintCommand"] = "ruff check ."
            if "black" in content:
                if not memory["build"]["lintCommand"]:
                    memory["build"]["lintCommand"] = "black ."
        except Exception:
            pass

    # Detect main directories
    main_dirs = []
    for d in sorted(root.iterdir()):
        if d.is_dir() and not d.name.startswith(".") and d.name not in (
            "node_modules", "__pycache__", "dist", "build", ".git", "venv", ".venv",
            "target", "vendor", "coverage",
        ):
            main_dirs.append(d.name)
    memory["structure"]["mainDirectories"] = main_dirs[:20]

    # Detect test patterns
    test_dirs = [d for d in main_dirs if d in ("test", "tests", "__tests__", "spec")]
    if test_dirs:
        memory["conventions"]["testPattern"] = test_dirs[0]

    # Build final language list
    memory["techStack"]["languages"] = [
        {"name": lang, "confidence": "high"} for lang in sorted(languages)
    ]
    memory["techStack"]["frameworks"] = frameworks
    memory["techStack"]["packageManager"] = pkg_manager

    return memory


def _find_script(scripts: dict, keys: list) -> Optional[str]:
    for key in keys:
        if key in scripts:
            return f"npm run {key}" if scripts else None
    return None


# --- Storage ---

def get_memory_dir(project_root: str) -> Path:
    return Path(project_root) / OMD_DIR


def get_memory_path(project_root: str) -> Path:
    return get_memory_dir(project_root) / MEMORY_FILE


def load_memory(project_root: str) -> Optional[dict]:
    path = get_memory_path(project_root)
    try:
        if path.exists():
            return json.loads(path.read_text())
    except Exception:
        pass
    return None


def save_memory(project_root: str, memory: dict):
    omd_dir = get_memory_dir(project_root)
    omd_dir.mkdir(parents=True, exist_ok=True)
    get_memory_path(project_root).write_text(json.dumps(memory, indent=2, ensure_ascii=False))


def should_rescan(memory: dict) -> bool:
    return (time.time() - memory.get("lastScanned", 0)) > CACHE_EXPIRY_SECONDS


# --- Context Formatting ---

def format_context_summary(memory: dict) -> str:
    parts = ["<project-memory>", ""]

    # Tech stack
    langs = [l["name"] for l in memory.get("techStack", {}).get("languages", [])]
    frameworks = [f["name"] for f in memory.get("techStack", {}).get("frameworks", [])]
    pkg_mgr = memory.get("techStack", {}).get("packageManager")

    if langs:
        parts.append(f"Languages: {', '.join(langs)}")
    if frameworks:
        parts.append(f"Frameworks: {', '.join(frameworks)}")
    if pkg_mgr:
        parts.append(f"Package Manager: {pkg_mgr}")

    # Build commands
    build = memory.get("build", {})
    cmds = []
    if build.get("buildCommand"):
        cmds.append(f"Build: `{build['buildCommand']}`")
    if build.get("testCommand"):
        cmds.append(f"Test: `{build['testCommand']}`")
    if build.get("lintCommand"):
        cmds.append(f"Lint: `{build['lintCommand']}`")
    if build.get("devCommand"):
        cmds.append(f"Dev: `{build['devCommand']}`")
    if cmds:
        parts.append("")
        parts.append("Build Commands:")
        parts.extend(f"  - {c}" for c in cmds)

    # Structure
    structure = memory.get("structure", {})
    if structure.get("isMonorepo"):
        parts.append(f"\nMonorepo: Yes (workspaces: {', '.join(structure.get('workspaces', []))})")
    main_dirs = structure.get("mainDirectories", [])
    if main_dirs:
        parts.append(f"\nMain directories: {', '.join(main_dirs[:10])}")

    # Conventions
    conventions = memory.get("conventions", {})
    conv_parts = []
    if conventions.get("testPattern"):
        conv_parts.append(f"Test dir: {conventions['testPattern']}")
    if conventions.get("namingStyle"):
        conv_parts.append(f"Naming: {conventions['namingStyle']}")
    if conv_parts:
        parts.append(f"\nConventions: {', '.join(conv_parts)}")

    # Hot paths
    hot_paths = memory.get("hotPaths", [])
    if hot_paths:
        top = sorted(hot_paths, key=lambda h: h.get("accessCount", 0), reverse=True)[:5]
        parts.append("\nFrequently accessed:")
        for hp in top:
            parts.append(f"  - {hp['path']} ({hp['accessCount']}x)")

    # User directives
    directives = memory.get("userDirectives", [])
    if directives:
        high_priority = [d for d in directives if d.get("priority") == "high"]
        if high_priority:
            parts.append("\nUser directives (high priority):")
            for d in high_priority[-5:]:
                parts.append(f"  - {d['directive']}")

    parts.append("")
    parts.append("</project-memory>")
    return "\n".join(parts)


# --- Learning ---

def learn_from_tool_output(tool_name: str, tool_input: dict, tool_output, project_root: str):
    memory = load_memory(project_root)
    if not memory:
        return

    changed = False

    # Track hot paths from Read/Edit/Grep
    if tool_name in ("Read", "Edit", "MultiEdit", "Create") and isinstance(tool_input, dict):
        file_path = tool_input.get("file_path", "")
        if file_path and project_root in file_path:
            rel_path = file_path.replace(project_root + "/", "")
            hot_paths = memory.get("hotPaths", [])
            existing = next((h for h in hot_paths if h["path"] == rel_path), None)
            if existing:
                existing["accessCount"] = existing.get("accessCount", 0) + 1
                existing["lastAccessed"] = int(time.time())
            else:
                hot_paths.append({
                    "path": rel_path,
                    "accessCount": 1,
                    "lastAccessed": int(time.time()),
                    "type": "file",
                })
            # Keep top 50
            memory["hotPaths"] = sorted(hot_paths, key=lambda h: h.get("accessCount", 0), reverse=True)[:50]
            changed = True

    if tool_name in ("Grep", "Glob") and isinstance(tool_input, dict):
        search_path = tool_input.get("path", "")
        if search_path and project_root in search_path:
            rel = search_path.replace(project_root + "/", "")
            hot_paths = memory.get("hotPaths", [])
            existing = next((h for h in hot_paths if h["path"] == rel), None)
            if existing:
                existing["accessCount"] = existing.get("accessCount", 0) + 1
                existing["lastAccessed"] = int(time.time())
            else:
                hot_paths.append({
                    "path": rel,
                    "accessCount": 1,
                    "lastAccessed": int(time.time()),
                    "type": "directory",
                })
            memory["hotPaths"] = sorted(hot_paths, key=lambda h: h.get("accessCount", 0), reverse=True)[:50]
            changed = True

    if changed:
        save_memory(project_root, memory)


# --- Notepad ---

def get_notepad_path(project_root: str) -> Path:
    return get_memory_dir(project_root) / NOTEPAD_FILE


def load_notepad(project_root: str) -> str:
    path = get_notepad_path(project_root)
    try:
        if path.exists():
            return path.read_text()
    except Exception:
        pass
    return ""


def set_priority_context(project_root: str, content: str):
    notepad = load_notepad(project_root)
    if "## Priority Context" in notepad:
        notepad = re.sub(
            r"## Priority Context\n[\s\S]*?(?=## |$)",
            f"## Priority Context\n{content}\n\n",
            notepad,
        )
    else:
        notepad = f"## Priority Context\n{content}\n\n{notepad}"

    path = get_notepad_path(project_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(notepad)


def add_working_memory(project_root: str, entry: str):
    notepad = load_notepad(project_root)
    timestamp = time.strftime("%Y-%m-%d %H:%M")
    new_entry = f"- [{timestamp}] {entry}\n"

    if "## Working Memory" in notepad:
        notepad = notepad.replace("## Working Memory\n", f"## Working Memory\n{new_entry}", 1)
    else:
        notepad += f"\n## Working Memory\n{new_entry}"

    path = get_notepad_path(project_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(notepad)


def get_priority_context(project_root: str) -> str:
    notepad = load_notepad(project_root)
    match = re.search(r"## Priority Context\n([\s\S]*?)(?=## |$)", notepad)
    if match:
        content = match.group(1).strip()
        clean = re.sub(r"<!--[\s\S]*?-->", "", content).strip()
        return clean
    return ""


# --- Hook Handlers ---

def handle_session_start(data: dict):
    """SessionStart: detect project environment and inject context."""
    directory = data.get("cwd", data.get("directory", os.getcwd()))
    messages = []

    # Load or detect memory
    memory = load_memory(directory)
    if not memory or should_rescan(memory):
        memory = detect_project_environment(directory)
        save_memory(directory, memory)

    # Check if we have useful info
    has_info = (
        memory.get("techStack", {}).get("languages")
        or memory.get("techStack", {}).get("frameworks")
        or memory.get("build", {}).get("buildCommand")
    )

    if has_info:
        messages.append(format_context_summary(memory))

    # Inject notepad priority context
    priority = get_priority_context(directory)
    if priority:
        messages.append(f"<notepad-context>\n[Priority Context]\n{priority}\n</notepad-context>")

    return "\n\n".join(messages) if messages else None


def handle_post_tool(data: dict):
    """PostToolUse: learn from tool usage patterns."""
    directory = data.get("cwd", data.get("directory", os.getcwd()))
    tool_name = data.get("tool_name", data.get("toolName", ""))
    tool_input = data.get("tool_input", data.get("toolInput", {}))
    tool_output = data.get("tool_response", data.get("toolOutput", ""))

    if not tool_name or not directory:
        return

    learn_from_tool_output(tool_name, tool_input, tool_output, directory)


def handle_pre_compact(data: dict):
    """PreCompact: preserve important state before compaction."""
    directory = data.get("cwd", data.get("directory", os.getcwd()))
    messages = []

    # Re-inject project memory
    memory = load_memory(directory)
    if memory:
        has_info = (
            memory.get("techStack", {}).get("languages")
            or memory.get("techStack", {}).get("frameworks")
            or memory.get("build", {}).get("buildCommand")
        )
        if has_info:
            messages.append(format_context_summary(memory))

    # Re-inject priority context
    priority = get_priority_context(directory)
    if priority:
        messages.append(f"<notepad-context>\n[Priority Context - Preserved across compact]\n{priority}\n</notepad-context>")

    # Re-inject hot paths
    if memory and memory.get("hotPaths"):
        top = sorted(memory["hotPaths"], key=lambda h: h.get("accessCount", 0), reverse=True)[:10]
        hot = "\n".join(f"  - {h['path']} ({h['accessCount']}x)" for h in top)
        messages.append(f"<hot-paths>\nFrequently accessed files (preserve across compact):\n{hot}\n</hot-paths>")

    return "\n\n".join(messages) if messages else None


# --- CLI ---

def main():
    """Dispatch based on first argument: session-start, post-tool, pre-compact."""
    action = sys.argv[1] if len(sys.argv) > 1 else "session-start"

    try:
        input_str = sys.stdin.read()
        data = json.loads(input_str) if input_str.strip() else {}
    except Exception:
        data = {}

    try:
        if action == "session-start":
            context = handle_session_start(data)
            if context:
                print(json.dumps({
                    "continue": True,
                    "hookSpecificOutput": {
                        "hookEventName": "SessionStart",
                        "additionalContext": context,
                    },
                }))
            else:
                print(json.dumps({"continue": True, "suppressOutput": True}))

        elif action == "post-tool":
            handle_post_tool(data)
            print(json.dumps({"continue": True, "suppressOutput": True}))

        elif action == "pre-compact":
            context = handle_pre_compact(data)
            if context:
                print(json.dumps({
                    "continue": True,
                    "hookSpecificOutput": {
                        "hookEventName": "PreCompact",
                        "additionalContext": context,
                    },
                }))
            else:
                print(json.dumps({"continue": True, "suppressOutput": True}))

        else:
            print(json.dumps({"continue": True, "suppressOutput": True}))

    except Exception:
        print(json.dumps({"continue": True, "suppressOutput": True}))


if __name__ == "__main__":
    main()
