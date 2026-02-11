---
description: Evidence-based verification - ensure implementation meets acceptance criteria with fresh proof
argument-hint: <implementation to verify or acceptance criteria>
---

Delegate this to the **verifier** droid via the Task tool.

Validate: $ARGUMENTS

The verifier must:
1. **Define**: What tests prove this works? What edge cases matter? What could regress?
2. **Execute**: Run test suite, build command, and related tests
3. **Gap analysis**: For each requirement -- VERIFIED (passes), PARTIAL (incomplete), MISSING (no test)
4. **Verdict**: PASS or FAIL with specific evidence for every acceptance criterion

No approval without fresh evidence. Reject if: "should/probably/seems to" is used, no fresh test output, claims without results.

Output: Status (PASS/FAIL/INCOMPLETE), Evidence, Acceptance Criteria status, Gaps, Recommendation.
