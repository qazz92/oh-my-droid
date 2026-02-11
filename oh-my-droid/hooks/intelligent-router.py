#!/usr/bin/env python3
"""
Intelligent Router for oh-my-droid

Analyzes tasks using droid exec and routes to appropriate droid.
Hybrid approach: AI analysis (primary) + Keyword fallback (secondary).
"""

import subprocess
import json
import sys
from typing import Optional

# Available droids and capabilities
DROIDS = {
    "basic-searcher": "Search code/files (low complexity)",
    "basic-reader": "Read/explain code (low complexity)",
    "executor-low": "Simple changes (low complexity)",
    "executor-med": "Implement/fix/debug (medium)",
    "executor-high": "Complex implementation (high)",
    "hephaestus": "Complex/build/architecture (very high)",
    "code-reviewer": "Review/audit code",
    "verifier": "Verify/test validation",
    "explorer": "Fast code search",
    "librarian": "Research specialist",
    "test-engineer": "Test creation",
    "security-auditor": "Security review",
    "orchestrator": "Task orchestration",
}

# Keyword-based routing (fallback)
KEYWORD_DROIDS = {
    "search|find|list": "basic-searcher",
    "read|explain|show": "basic-reader",
    "debug|fix|refactor": "executor-med",
    "build|implement|create|write": "executor-med",
    "review|audit|check": "code-reviewer",
    "verify|validate|test": "verifier",
    "architecture|design|system|api": "hephaestus",
    "complex|architecture|microservices": "executor-high",
}

# Default routing result
DEFAULT_ROUTING = {
    "droid": "executor-med",
    "autonomy": "medium",
    "confidence": 0.5,
    "reason": "Default routing - no specific patterns detected"
}

ROUTER_ERROR = {
    "droid": "executor-med",
    "autonomy": "medium",
    "confidence": 0.0,
    "reason": "Router error - using default",
}


def route_by_keywords(prompt: str) -> Optional[dict]:
    """Route based on keyword matching (fallback)"""
    prompt_lower = prompt.lower()

    for pattern, droid in KEYWORD_DROIDS.items():
        if any(kw in prompt_lower for kw in pattern.split('|')):
            return {
                "droid": droid,
                "autonomy": "medium",
                "confidence": 0.6,
                "reason": f"Keyword matched: {pattern}"
            }

    return None


def route_by_ai(prompt: str) -> dict:
    """Route using AI analysis via droid exec"""
    analysis_prompt = f'''
Analyze the task and output ONLY valid JSON:

Task: "{prompt}"

Available droids:
{chr(10).join([f"{k}: {v}" for k, v in DROIDS.items()])}

Output JSON format:
{{
    "droid": "basic-searcher|basic-reader|executor-low|executor-med|executor-high|hephaestus|code-reviewer|verifier",
    "autonomy": "low|medium|high",
    "confidence": 0.0-1.0,
    "reason": "brief explanation of why this droid was chosen"
}}

Rules:
1. Choose droid based on task complexity
2. Simple search/read tasks → basic-* droids (autonomy: low)
3. Simple implementation → executor-low (autonomy: low)
4. Standard implementation/fix → executor-med (autonomy: medium)
5. Complex implementation → executor-high (autonomy: high)
6. Very complex architecture/build → hephaestus (autonomy: high)
7. Review tasks → code-reviewer
8. Verification → verifier
'''

    try:
        result = subprocess.run([
            'droid', 'exec', '--auto', 'low', '--', analysis_prompt
        ], capture_output=True, text=True, timeout=120)

        if result.returncode == 0:
            # Parse JSON from output
            output = result.stdout.strip()
            for line in output.split('\n'):
                if '{' in line:
                    try:
                        json_start = line.index('{')
                        parsed = json.loads(line[json_start:])
                        # Validate droid name
                        if parsed.get('droid') in DROIDS:
                            return parsed
                    except (json.JSONDecodeError, KeyError):
                        pass

        # If AI analysis fails, return default
        return DEFAULT_ROUTING.copy()

    except subprocess.TimeoutExpired:
        return {
            "droid": "executor-med",
            "autonomy": "medium",
            "confidence": 0.3,
            "reason": "AI analysis timed out - using default"
        }
    except Exception as e:
        return {
            "droid": "executor-med",
            "autonomy": "medium",
            "confidence": 0.0,
            "reason": f"Router error: {str(e)[:50]}"
        }


def route(prompt: str) -> dict:
    """Main routing function - tries AI first, falls back to keywords"""
    # Try AI-based routing first
    ai_result = route_by_ai(prompt)

    # If AI has low confidence, supplement with keyword matching
    if ai_result['confidence'] < 0.7:
        keyword_result = route_by_keywords(prompt)
        if keyword_result:
            # Combine: use AI autonomy but keyword droid suggestion
            return {
                "droid": keyword_result['droid'],
                "autonomy": ai_result['autonomy'],
                "confidence": max(ai_result['confidence'], keyword_result['confidence']),
                "reason": f"Hybrid: AI ({keyword_result['confidence']:.1f}) + Keyword match"
            }

    return ai_result


def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        # No arguments - output routing info
        print(json.dumps({
            "version": "1.0.0",
            "available_droids": DROIDS,
            "usage": "intelligent-router.py \"<task>\""
        }, indent=2))
        sys.exit(0)

    # Just route and output result
    prompt = ' '.join(sys.argv[1:])
    routing = route(prompt)
    print(json.dumps(routing, indent=2))


if __name__ == "__main__":
    main()
