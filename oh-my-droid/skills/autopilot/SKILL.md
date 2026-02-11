---
name: autopilot
description: Full autonomous execution from idea to working code. Handles the full lifecycle - requirements, planning, parallel implementation, QA cycling, and multi-perspective validation.
---

<Purpose>
Autopilot takes a brief product idea and autonomously handles the full lifecycle: requirements analysis, technical design, planning, parallel implementation, QA cycling, and multi-perspective validation. It produces working, verified code from a short description.
</Purpose>

<Use_When>
- User wants end-to-end autonomous execution from an idea to working code
- User says "autopilot", "auto pilot", "autonomous", "build me", "create me", "make me", "full auto", "handle it all"
- Task requires multiple phases: planning, coding, testing, and validation
- User wants hands-off execution and is willing to let the system run to completion
</Use_When>

<Do_Not_Use_When>
- User wants to explore or brainstorm -- respond conversationally or use prometheus droid
- User says "just explain", "draft only", "what would you suggest" -- respond conversationally
- User wants a single focused code change -- use ralph skill or delegate to executor-med directly
- User wants to review or critique an existing plan -- use momus droid
- Task is a quick fix or small bug -- use direct executor delegation
</Do_Not_Use_When>

<Execution_Policy>
- Each phase must complete before the next begins
- Parallel execution is used within phases where possible (Phase 2 and Phase 4)
- QA cycles repeat up to 5 times; if the same error persists 3 times, stop and report the fundamental issue
- Validation requires approval from all reviewers; rejected items get fixed and re-validated
- State is tracked in `.omd/state/autopilot-state.json`
</Execution_Policy>

<Task_Tool_Usage>
CRITICAL: When spawning droids, you MUST use the Task tool with these EXACT parameters:
- `subagent_type`: The droid name exactly as listed below (e.g., "prometheus", "verifier")
- `description`: A short 3-5 word label
- `prompt`: The full task instructions

Example:
```
Task(subagent_type="prometheus", description="Create implementation plan", prompt="Create a detailed implementation plan for: ...")
Task(subagent_type="momus", description="Validate the plan", prompt="Review this plan for gaps and risks: ...")
Task(subagent_type="executor-med", description="Implement user auth", prompt="Implement user authentication: ...")
Task(subagent_type="verifier", description="Verify implementation", prompt="Verify that the implementation meets these criteria: ...")
Task(subagent_type="code-reviewer", description="Review code quality", prompt="Review the following changes for quality: ...")
Task(subagent_type="security-auditor", description="Security review", prompt="Check for security vulnerabilities: ...")
```

ALL THREE parameters (subagent_type, description, prompt) are REQUIRED for every Task call.
</Task_Tool_Usage>

<Steps>
1. **Phase 0 - Expansion**: Turn the user's idea into a detailed spec
   ```
   Task(subagent_type="prometheus", description="Extract requirements", prompt="Analyze this idea and create a detailed technical spec: <user's idea>")
   ```
   - Output: `.omd/autopilot/spec.md`

2. **Phase 1 - Planning**: Create implementation plan from spec
   ```
   Task(subagent_type="prometheus", description="Create impl plan", prompt="Create a detailed implementation plan from this spec: <spec content>")
   ```
   Then validate:
   ```
   Task(subagent_type="momus", description="Validate the plan", prompt="Review this implementation plan for gaps, risks, and feasibility: <plan content>")
   ```
   - Output: `.omd/plans/autopilot-impl.md`

3. **Phase 2 - Execution**: Implement using appropriate droids
   - Simple tasks: `Task(subagent_type="executor-low", description="...", prompt="...")`
   - Standard tasks: `Task(subagent_type="executor-med", description="...", prompt="...")`
   - Complex tasks: `Task(subagent_type="executor-high", description="...", prompt="...")`
   - Architecture: `Task(subagent_type="hephaestus", description="...", prompt="...")`
   - Run independent tasks in parallel (multiple Task calls at once)

4. **Phase 3 - QA**: Cycle until all checks pass
   - Build, lint, typecheck, run tests
   - Fix failures and retry
   - Max 5 cycles; stop early if the same error repeats 3 times

5. **Phase 4 - Validation**: Multi-perspective review in parallel
   ```
   Task(subagent_type="code-reviewer", description="Code quality review", prompt="Review these changes for quality: <changes>")
   Task(subagent_type="security-auditor", description="Security review", prompt="Check for security vulnerabilities: <changes>")
   Task(subagent_type="verifier", description="Verify implementation", prompt="Verify this implementation meets acceptance criteria: <criteria>")
   ```
   - All must approve; fix and re-validate on rejection

6. **Phase 5 - Cleanup**: Delete state files on successful completion
   - Remove `.omd/state/autopilot-state.json` and related state files
</Steps>

<Droid_Selection_Guide>
| Task Type | subagent_type | When to Use |
|-----------|---------------|-------------|
| Requirements, planning | `prometheus` | Phase 0, Phase 1 |
| Plan validation | `momus` | Phase 1 |
| Simple tasks | `executor-low` | Config changes, small file edits |
| Standard tasks | `executor-med` | Implementation, bug fixes, features (default) |
| Complex tasks | `executor-high` | Multi-file changes, refactoring |
| Architecture | `hephaestus` | System design, complex architecture |
| Code review | `code-reviewer` | Phase 4 quality review |
| Security review | `security-auditor` | Phase 4 vulnerability check |
| Verification | `verifier` | Phase 4 functional correctness |
</Droid_Selection_Guide>

<Examples>
<Good>
User: "autopilot build a REST API for bookstore inventory with CRUD using TypeScript"
Why: Specific domain, clear features, technology constraint. Enough context to expand into a full spec.
</Good>

<Good>
Correct Task tool usage:
```
Task(subagent_type="prometheus", description="Create API spec", prompt="Analyze and create detailed spec for: REST API for bookstore inventory with CRUD using TypeScript")
Task(subagent_type="momus", description="Validate API plan", prompt="Review this plan for gaps: ...")
Task(subagent_type="executor-med", description="Create user endpoints", prompt="Implement the /api/users CRUD endpoints: ...")
Task(subagent_type="executor-med", description="Create book endpoints", prompt="Implement the /api/books CRUD endpoints: ...")
Task(subagent_type="verifier", description="Verify API works", prompt="Run tests and verify all CRUD endpoints work: ...")
```
Why: All three required params present, correct subagent_type names, independent tasks fired in parallel.
</Good>

<Bad>
Task(subagent_type="verify", description="Check it", prompt="...")
Why: "verify" is not a valid droid name. Use "verifier".
</Bad>

<Bad>
Task(subagent_type="verifier", prompt="Verify the changes")
Why: Missing required `description` parameter.
</Bad>
</Examples>

<Escalation_And_Stop_Conditions>
- Stop and report when the same QA error persists across 3 cycles (fundamental issue requiring human input)
- Stop and report when validation keeps failing after 3 re-validation rounds
- Stop when the user says "stop", "cancel", or "abort"
- If requirements are too vague, pause and ask the user for clarification before proceeding
</Escalation_And_Stop_Conditions>

<Final_Checklist>
- [ ] All phases completed (Expansion, Planning, Execution, QA, Validation)
- [ ] All validators approved in Phase 4
- [ ] Tests pass (verified with fresh test run output)
- [ ] Build succeeds (verified with fresh build output)
- [ ] State files cleaned up
- [ ] User informed of completion with summary of what was built
</Final_Checklist>
