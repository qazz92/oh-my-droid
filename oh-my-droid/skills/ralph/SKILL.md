---
name: ralph
description: Persistent execution loop until task completion with verification. Wraps parallel execution with automatic retry on failure and mandatory verification before completion.
---

<Purpose>
Ralph is a persistence loop that keeps working on a task until it is fully complete and verified. It wraps parallel execution with session persistence, automatic retry on failure, and mandatory verification before completion.
</Purpose>

<Use_When>
- Task requires guaranteed completion with verification (not just "do your best")
- User says "ralph", "don't stop", "must complete", "finish this", or "keep going until done"
- Work may span multiple iterations and needs persistence across retries
- Task benefits from parallel execution with verification at the end
</Use_When>

<Do_Not_Use_When>
- User wants a full autonomous pipeline from idea to code -- use `autopilot` instead
- User wants to explore or plan before committing -- use prometheus droid
- User wants a quick one-shot fix -- delegate directly to executor-med
- User wants manual control over completion -- use `ultrawork` directly
</Do_Not_Use_When>

<Why_This_Exists>
Complex tasks often fail silently: partial implementations get declared "done", tests get skipped, edge cases get forgotten. Ralph prevents this by looping until work is genuinely complete, requiring fresh verification evidence before allowing completion.
</Why_This_Exists>

<Execution_Policy>
- Fire independent droid calls simultaneously -- never wait sequentially for independent work
- Always select the right droid tier for the task complexity
- Deliver the full implementation: no scope reduction, no partial completion, no deleting tests to make them pass
- State is tracked in `.omd/state/ralph-state.json`
</Execution_Policy>

<Parallel_Execution>
Factory Droid does NOT support native background execution (`run_in_background: true`). For TRUE parallel execution of independent tasks, use `background-manager.py`:

```bash
# Launch multiple droids in TRUE parallel (fire ALL before checking ANY)
python3 hooks/background-manager.py launch "Fix auth" "Fix auth module errors" executor-med "main"
python3 hooks/background-manager.py launch "Fix API" "Fix API route errors" executor-med "main"
python3 hooks/background-manager.py launch "Fix UI" "Fix frontend type errors" executor-med "main"

# Monitor all running tasks
python3 hooks/background-manager.py list

# Check specific task output when done
python3 hooks/background-manager.py output <task_id>
```

CRITICAL: Launch ALL independent tasks BEFORE checking any results. Do NOT launch-wait-launch sequentially.
</Parallel_Execution>

<Steps>
1. **Review progress**: Check TODO list and any prior iteration state
2. **Continue from where you left off**: Pick up incomplete tasks
3. **Delegate in parallel**: Route tasks to specialist droids at appropriate tiers
   - Simple changes: executor-low
   - Standard work: executor-med (DEFAULT)
   - Complex analysis: executor-high or hephaestus
4. **Verify completion with fresh evidence**:
   a. Identify what command proves the task is complete
   b. Run verification (test, build, lint)
   c. Read the output -- confirm it actually passed
   d. Check: zero pending/in_progress TODO items
5. **Droid verification** (mandatory):
   - Spawn **verifier** droid to independently check all acceptance criteria
   - For security-sensitive changes, also spawn **security-auditor**
6. **On approval**: Clean up `.omd/state/ralph-state.json`
7. **On rejection**: Fix the issues raised, then re-verify (max 3 attempts)
</Steps>

<Examples>
<Good>
Correct parallel delegation:
```
Task(subagent_type="executor-low", prompt="Add type export for UserConfig")
Task(subagent_type="executor-med", prompt="Implement the caching layer for API responses")
Task(subagent_type="executor-high", prompt="Refactor auth module to support OAuth2 flow")
```
Why good: Three independent tasks fired simultaneously at appropriate tiers.
</Good>

<Good>
Correct verification before completion:
```
1. Run: npm test           -> Output: "42 passed, 0 failed"
2. Run: npm run build      -> Output: "Build succeeded"
3. Spawn verifier droid    -> Verdict: "PASS - all criteria verified"
4. Clean up state files
```
Why good: Fresh evidence at each step, droid verification, then clean exit.
</Good>

<Bad>
Claiming completion without verification:
"All changes look good, the implementation should work correctly. Task complete."
Why bad: Uses "should" and "look good" -- no fresh test/build output, no droid verification.
</Bad>

<Bad>
Sequential execution of independent tasks:
```
Task(executor-low, "Add type export") -> wait ->
Task(executor-med, "Implement caching") -> wait ->
Task(executor-high, "Refactor auth")
```
Why bad: Independent tasks should run in parallel, not sequentially.
</Bad>
</Examples>

<Escalation_And_Stop_Conditions>
- Stop and report when a fundamental blocker requires user input (missing credentials, unclear requirements)
- Stop when the user says "stop", "cancel", or "abort"
- If the same issue recurs across 3+ attempts, report it as a fundamental problem
- If verification droid rejects, fix issues and re-verify (do not stop)
</Escalation_And_Stop_Conditions>

<Final_Checklist>
- [ ] All requirements from the original task are met (no scope reduction)
- [ ] Zero pending or in_progress TODO items
- [ ] Fresh test run output shows all tests pass
- [ ] Fresh build output shows success
- [ ] Verifier droid approved (mandatory)
- [ ] State files cleaned up
</Final_Checklist>
