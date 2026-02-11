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
- User wants to explore options or brainstorm -- respond conversationally or use prometheus droid
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

<Steps>
1. **Phase 0 - Expansion**: Turn the user's idea into a detailed spec
   - Spawn **prometheus** droid: Extract requirements and create technical specification
   - Output: `.omd/autopilot/spec.md`

2. **Phase 1 - Planning**: Create an implementation plan from the spec
   - Spawn **prometheus** droid: Create plan (direct mode, no interview)
   - Spawn **momus** droid: Validate plan for gaps and risks
   - Output: `.omd/plans/autopilot-impl.md`

3. **Phase 2 - Execution**: Implement the plan using appropriate droids
   - **executor-low**: Simple, low-risk tasks (config changes, small edits)
   - **executor-med**: Standard implementation tasks (default)
   - **executor-high**: Complex implementation requiring broad tool access
   - **hephaestus**: Architecture-level, system design tasks
   - Run independent tasks in parallel via Task tool

4. **Phase 3 - QA**: Cycle until all checks pass
   - Build, lint, typecheck, run tests
   - Fix failures and retry
   - Max 5 cycles; stop early if the same error repeats 3 times (fundamental issue)

5. **Phase 4 - Validation**: Multi-perspective review in parallel
   - Spawn **code-reviewer** droid: Code quality and patterns
   - Spawn **security-auditor** droid: Vulnerability check
   - Spawn **verifier** droid: Functional correctness
   - All must approve; fix and re-validate on rejection

6. **Phase 5 - Cleanup**: Delete state files on successful completion
   - Remove `.omd/state/autopilot-state.json` and related state files
</Steps>

<Droid_Selection_Guide>
| Task Type | Droid | When to Use |
|-----------|-------|-------------|
| Requirements, planning | prometheus | Phase 0, Phase 1 |
| Plan validation | momus | Phase 1 |
| Simple tasks | executor-low | Config changes, small file edits |
| Standard tasks | executor-med | Implementation, bug fixes, features (default) |
| Complex tasks | executor-high | Multi-file changes, refactoring |
| Architecture | hephaestus | System design, complex architecture |
| Code review | code-reviewer | Phase 4 quality review |
| Security review | security-auditor | Phase 4 vulnerability check |
| Verification | verifier | Phase 4 functional correctness |
</Droid_Selection_Guide>

<Examples>
<Good>
User: "autopilot build a REST API for bookstore inventory with CRUD using TypeScript"
Why: Specific domain, clear features, technology constraint. Enough context to expand into a full spec.
</Good>

<Good>
User: "build me a CLI tool that tracks daily habits with streak counting"
Why: Clear product concept with a specific feature. Autopilot has enough to work with.
</Good>

<Bad>
User: "fix the bug in the login page"
Why: Single focused fix. Use ralph or direct executor-med delegation instead.
</Bad>

<Bad>
User: "what are some good approaches for adding caching?"
Why: Exploration request. Respond conversationally or use prometheus droid.
</Bad>
</Examples>

<Escalation_And_Stop_Conditions>
- Stop and report when the same QA error persists across 3 cycles (fundamental issue requiring human input)
- Stop and report when validation keeps failing after 3 re-validation rounds
- Stop when the user says "stop", "cancel", or "abort"
- If requirements are too vague and expansion produces an unclear spec, pause and ask the user for clarification before proceeding
</Escalation_And_Stop_Conditions>

<Final_Checklist>
- [ ] All phases completed (Expansion, Planning, Execution, QA, Validation)
- [ ] All validators approved in Phase 4
- [ ] Tests pass (verified with fresh test run output)
- [ ] Build succeeds (verified with fresh build output)
- [ ] State files cleaned up
- [ ] User informed of completion with summary of what was built
</Final_Checklist>
