---
name: diagnose-and-fix-code-error
description: Diagnose and fix a runtime or code error: gather the message and stack trace, trace it to the relevant source, isolate the true root cause (parameter mismatch, type error, bad logic, upstream data), propose a precise fix, apply it, and verify. Use whenever the user reports an error, exception, stack trace, crash, or says code is broken.
---

# Diagnose and Fix a Code Error

Debug a code error systematically by analyzing error messages, reading relevant files, identifying root causes, and implementing fixes.

## Workflow

### 1. Gather Error Information

Ask the user for:

- The complete error message (including stack trace if available)
- What they were trying to do when the error occurred
- Any relevant context (which file/function they were running, what inputs they used)

If the user has already provided the error in their message, proceed directly to step 2.

### 2. Identify Relevant Files

Based on the error message, determine which files need to be examined:

- **Function/file mentioned in error**: Read the file where the error occurred
- **Stack trace locations**: Read files mentioned in the stack trace (bottom-up priority)
- **Related functions**: Identify and read files that call or are called by the error location
- **Configuration/orchestration**: Check orchestrator or configuration files that may pass incorrect parameters

Open and inspect the implicated files (read several at once when your environment allows) so you have full context before reasoning about the cause.

### 3. Analyze Root Cause

Review the code to identify:

- **Immediate cause**: What specific line or condition triggered the error?
- **Parameter mismatch**: Are required parameters missing or NULL when they shouldn't be?
- **Type errors**: Are values of the wrong type being passed?
- **Logic errors**: Are conditions or calculations incorrect?
- **Upstream issues**: Is the error caused by incorrect data flowing from a caller?

Look for patterns like (e.g. in an R project):

- Required parameter validation (`if (is.null(x)) stop(...)`)
- Parameter passing in function calls
- Conditional logic that determines code paths
- Default values that may be problematic

### 4. Propose Solution

Explain the fix clearly:

- **What's wrong**: Describe the root cause in simple terms
- **Why it's wrong**: Explain why this causes the error
- **How to fix it**: Propose the specific code changes needed
- **Why this fixes it**: Explain how the fix resolves the issue

### 5. Implement Fix

Apply the fix to the source to make the necessary changes:

- Make precise edits that address the root cause
- Add explanatory comments if the fix is non-obvious
- Consider edge cases that might trigger similar errors
- Update multiple locations if the same pattern appears elsewhere

### 6. Verify Fix

After implementing:

- Show the user the changed code segments
- Explain what was fixed at each location (with file:line references)
- Suggest how to test the fix
- Check if similar issues might exist elsewhere in the codebase

## Example Flow

```
User: "I'm getting 'Error: check_date is required' when running run_report()"

Step 1: Gather context - user provided error, identify it's from check_incomplete_aircraft
Step 2: Read relevant files - check_incomplete_aircraft.r, orchestrator.r, run_checks.r
Step 3: Analyze - find that orchestrator.r passes check_date=NULL during initialization
Step 4: Propose - pass date_range_end as check_date in run_aggregate_initialization()
Step 5: Implement - edit orchestrator.r to pass date_range_end
Step 6: Verify - explain the fix and suggest re-running the code
```

(Illustrative; the same six steps apply to any language or stack.)

## Key Principles

- **Read before proposing**: Always read the actual code before suggesting fixes
- **Root cause, not symptoms**: Fix the underlying issue, not just the immediate error
- **Parallel when possible**: Read multiple files at once to be efficient
- **Explain clearly**: User should understand both the problem and the solution
- **Test suggestions**: Provide clear instructions for verifying the fix works
- **Check for patterns**: If you fix one instance, look for similar issues elsewhere

## Special Cases

### Missing Dependencies

If error is about missing packages/libraries:

- Check import/library statements
- Verify package is in requirements/dependencies
- Suggest installation command

### Data-Related Errors

If error involves data frames, columns, or types:

- Check that required columns exist in the data
- Verify data types match expectations
- Look for filtering that might remove needed data

### Configuration Errors

If error relates to paths, settings, or environment:

- Check file paths are correct for the environment
- Verify working directory assumptions
- Look for hardcoded values that should be parameters

### Logic Errors

If code runs but produces wrong results:

- Trace data flow through the system
- Check calculations and transformations
- Verify conditional logic and edge cases
