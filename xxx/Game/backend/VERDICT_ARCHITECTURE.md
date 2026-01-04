# Verdict System Architecture - Visual Guide

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Monaco Code Editor                                     │    │
│  │  - User writes code: twoSum(nums, target) {...}        │    │
│  └────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              │ User clicks "RUN" or "SUBMIT"    │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Frontend Logic                                         │    │
│  │  1. Get user code from editor                          │    │
│  │  2. Call /api/code/generate-wrapper                    │    │
│  │  3. Call /api/code/verdict                             │    │
│  └────────────────────────────────────────────────────────┘    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTP POST /api/code/verdict
                         │ { problemId, wrappedCode, mode, action }
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                         BACKEND                                  │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  FastAPI Endpoint: /api/code/verdict                   │    │
│  │  - Validates inputs                                     │    │
│  │  - Checks authentication (SUBMIT only)                 │    │
│  │  - Calls verdict_service.get_verdict()                 │    │
│  └────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  verdict_service.py                                     │    │
│  │  - Fetches problem from MongoDB                        │    │
│  │  - Selects test cases (sample vs hidden)              │    │
│  │  - Executes against each test case                    │    │
│  │  - Compares outputs                                    │    │
│  │  - Stores submission (SUBMIT only)                     │    │
│  └────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  judge0_service.py                                      │    │
│  │  - Submits code to Judge0 API                          │    │
│  │  - Polls for results                                   │    │
│  │  - Handles retries on network failure                  │    │
│  │  - Returns execution result                            │    │
│  └────────────────────────────────────────────────────────┘    │
│                              │                                   │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  MongoDB Collections                                    │    │
│  │  - problems_collection (test cases)                    │    │
│  │  - submissions_collection (results)                    │    │
│  └────────────────────────────────────────────────────────┘    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Judge0 API Call
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    JUDGE0 (External Service)                     │
│  - Compiles C++ code                                             │
│  - Executes in isolated sandbox                                  │
│  - Returns: stdout, stderr, execution_time, memory              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Detailed Verdict Flow

```
START: User submits code
│
├─ Step 1: API Request Validation
│   ├─ Check problemId is provided ✓
│   ├─ Check wrappedCode is not empty ✓
│   ├─ Check mode is "practice" or "battle" ✓
│   └─ Check action is "run" or "submit" ✓
│
├─ Step 2: Authentication Check
│   ├─ If action == "submit"
│   │   ├─ JWT token required
│   │   ├─ If missing → Return 401 Unauthorized
│   │   └─ If valid → Extract userId
│   └─ If action == "run"
│       └─ Optional auth (userId = null if not provided)
│
├─ Step 3: Fetch Problem from Database
│   ├─ Query: problems_collection.find_one({"problem_id": problemId})
│   └─ If not found → Return "Problem not found" error
│
├─ Step 4: Select Test Cases
│   ├─ If action == "run"
│   │   └─ testCases = problem.sampleTestCases (1-2 cases)
│   └─ If action == "submit"
│       └─ testCases = problem.hiddenTestCases (3-5 cases)
│
├─ Step 5: Execute Code Against Each Test Case (STOP ON FIRST FAILURE)
│   │
│   FOR EACH test_case IN testCases:
│   │
│   ├─ 5a. Format Input
│   │   └─ Convert "[1,2,3], 5" → "[1,2,3]\n5"
│   │
│   ├─ 5b. Execute Code via Judge0 (with retry)
│   │   ├─ Attempt 1: judge0_execute_code()
│   │   ├─ If network error → Wait 1s → Attempt 2
│   │   └─ If still fails → Return "Internal Error"
│   │
│   ├─ 5c. Check for Errors (Priority Order)
│   │   │
│   │   ├─ Compilation Error?
│   │   │   ├─ Yes → verdict = "Compilation Error"
│   │   │   └─ STOP (break loop)
│   │   │
│   │   ├─ Runtime Error?
│   │   │   ├─ Yes → verdict = "Runtime Error"
│   │   │   └─ STOP (break loop)
│   │   │
│   │   ├─ Time Limit Exceeded?
│   │   │   ├─ Yes → verdict = "Time Limit Exceeded"
│   │   │   └─ STOP (break loop)
│   │   │
│   │   └─ Internal Error?
│   │       ├─ Yes → verdict = "Internal Error"
│   │       └─ STOP (break loop)
│   │
│   ├─ 5d. Compare Output
│   │   ├─ Normalize actual output (trim, remove empty lines)
│   │   ├─ Normalize expected output (trim, remove empty lines)
│   │   └─ If actual != expected
│   │       ├─ verdict = "Wrong Answer"
│   │       └─ STOP (break loop)
│   │
│   └─ 5e. Test Passed
│       ├─ testsPassed += 1
│       └─ Continue to next test case
│
├─ Step 6: Determine Final Verdict
│   └─ If ALL tests passed → verdict = "Accepted"
│
├─ Step 7: Store Submission (SUBMIT only)
│   ├─ If action == "submit"
│   │   └─ submissions_collection.insert_one({
│   │       userId, problemId, mode, action, verdict,
│   │       testsPassed, totalTests, executionTime, memory,
│   │       submittedAt, battleId
│   │     })
│   └─ If action == "run"
│       └─ Skip storage (temporary test)
│
└─ Step 8: Return Response
    ├─ If action == "run"
    │   └─ Return: verdict + detailed test results (with inputs/outputs)
    └─ If action == "submit"
        └─ Return: verdict + counts only (no outputs)
│
END
```

---

## Verdict Determination Logic

```
┌─────────────────────────────────────────────────────────────────┐
│                  VERDICT PRIORITY HIERARCHY                      │
│                  (Checked in this exact order)                   │
└─────────────────────────────────────────────────────────────────┘

Priority 1: COMPILATION ERROR
    ├─ Condition: Judge0 status == "compilation_error"
    ├─ Trigger: Syntax error, missing header, type mismatch
    ├─ Action: STOP immediately (no tests run)
    └─ Message: Compile output from Judge0

        ▼

Priority 2: RUNTIME ERROR
    ├─ Condition: Judge0 status == "runtime_error"
    ├─ Trigger: Segfault, division by zero, out of bounds
    ├─ Action: STOP on first occurrence
    └─ Message: stderr from Judge0

        ▼

Priority 3: TIME LIMIT EXCEEDED
    ├─ Condition: Judge0 status == "time_limit_exceeded"
    ├─ Trigger: Execution > 2 seconds
    ├─ Action: STOP on first occurrence
    └─ Message: "Time limit exceeded (>2.0s)"

        ▼

Priority 4: INTERNAL ERROR
    ├─ Condition: Judge0 network failure (after retry)
    ├─ Trigger: Connection timeout, API unavailable
    ├─ Action: STOP on first occurrence
    └─ Message: "Judge0 service unavailable"

        ▼

Priority 5: WRONG ANSWER
    ├─ Condition: actual output ≠ expected output
    ├─ Trigger: Logic error in code
    ├─ Action: STOP on first occurrence
    └─ Message: "Output does not match expected output"

        ▼

Priority 6: ACCEPTED
    ├─ Condition: ALL tests passed
    └─ Action: Return success

┌─────────────────────────────────────────────────────────────────┐
│                  STOP ON FIRST FAILURE                           │
│  As soon as any error is detected, execution stops               │
│  Remaining test cases are NOT executed                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Test Case Selection Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    ACTION: RUN                                   │
└─────────────────────────────────────────────────────────────────┘

User Code → Wrapped Code → Execute against SAMPLE test cases
                                       │
                                       ▼
                        ┌──────────────────────────┐
                        │  sampleTestCases (1-2)   │
                        │  - Visible to user       │
                        │  - Simple cases          │
                        │  - For debugging         │
                        └──────────────────────────┘
                                       │
                                       ▼
                        Return detailed results:
                        - Test case number
                        - Input (visible)
                        - Expected output (visible)
                        - Actual output (visible)
                        - Passed/Failed
                        - Execution time
                        - Memory usage

┌─────────────────────────────────────────────────────────────────┐
│                    ACTION: SUBMIT                                │
└─────────────────────────────────────────────────────────────────┘

User Code → Wrapped Code → Execute against HIDDEN test cases
                                       │
                                       ▼
                        ┌──────────────────────────┐
                        │ hiddenTestCases (3-5)    │
                        │  - NOT visible to user   │
                        │  - Edge cases            │
                        │  - For grading           │
                        └──────────────────────────┘
                                       │
                                       ▼
                        Return only verdict:
                        - Final verdict
                        - Tests passed count
                        - Total tests count
                        - Total execution time
                        - Max memory
                        - NO inputs/outputs shown

                                       │
                                       ▼
                        Store in submissions_collection
```

---

## Output Comparison Algorithm

```
┌─────────────────────────────────────────────────────────────────┐
│              OUTPUT NORMALIZATION PROCESS                        │
└─────────────────────────────────────────────────────────────────┘

Original Output:
"  [0, 1]  \n\n  "

Step 1: Trim leading/trailing whitespace
→ "[0, 1]  \n\n  " → "[0, 1]"

Step 2: Split by newline
→ ["[0, 1]"]

Step 3: Trim each line
→ ["[0, 1]"]

Step 4: Remove empty lines
→ ["[0, 1]"]

Step 5: Join with single newline
→ "[0, 1]"

┌─────────────────────────────────────────────────────────────────┐
│              COMPARISON EXAMPLES                                 │
└─────────────────────────────────────────────────────────────────┘

Example 1: Match
    Actual:   "  [0,1]\n  "
    Expected: "[0,1]"
    Result:   ✓ MATCH (after normalization)

Example 2: No Match (spacing)
    Actual:   "[0, 1]"
    Expected: "[0,1]"
    Result:   ✗ NO MATCH (space matters)

Example 3: Match (trailing newline ignored)
    Actual:   "[0,1]\n\n"
    Expected: "[0,1]"
    Result:   ✓ MATCH

Example 4: No Match (case sensitive)
    Actual:   "True"
    Expected: "true"
    Result:   ✗ NO MATCH
```

---

## Retry Logic Flow

```
┌─────────────────────────────────────────────────────────────────┐
│              JUDGE0 EXECUTION WITH RETRY                         │
└─────────────────────────────────────────────────────────────────┘

Attempt 1:
    ├─ Call Judge0 API
    │
    ├─ Success?
    │   └─ Yes → Return result
    │
    └─ Network error? (timeout, connection_error, polling_timeout)
        ├─ Yes → Continue to Attempt 2
        └─ No (compilation/runtime error) → Return result immediately

        ▼

Wait 1 second (retry delay)

        ▼

Attempt 2:
    ├─ Call Judge0 API again
    │
    ├─ Success?
    │   └─ Yes → Return result
    │
    └─ Failed again?
        └─ Return "Internal Error"

┌─────────────────────────────────────────────────────────────────┐
│              RETRY CONDITIONS                                    │
└─────────────────────────────────────────────────────────────────┘

✅ RETRY on:
    - timeout (Judge0 API request timed out)
    - connection_error (Failed to connect to Judge0)
    - polling_timeout (Polling timeout exceeded)

❌ DO NOT RETRY on:
    - compilation_error (Code issue)
    - runtime_error (Code issue)
    - time_limit_exceeded (Code issue)
    - accepted (Success)
```

---

## Database Schema

```
┌─────────────────────────────────────────────────────────────────┐
│              submissions_collection                              │
└─────────────────────────────────────────────────────────────────┘

{
  "_id": "uuid",
  "userId": "user-uuid" | "guest",
  "problemId": "two-sum",
  "mode": "practice" | "battle",
  "action": "submit",
  "verdict": "Accepted" | "Wrong Answer" | "Compilation Error" | ...,
  "testsPassed": 5,
  "totalTests": 5,
  "executionTime": 0.125,
  "memory": 4096,
  "submittedAt": "2025-01-15T10:30:00.000Z",
  "battleId": "battle-uuid" | null
}

Indexes:
  - (userId, problemId, submittedAt) - Composite index for user history
  - battleId - Index for battle submissions
```

---

## API Response Formats

```
┌─────────────────────────────────────────────────────────────────┐
│              RUN RESPONSE (Detailed)                             │
└─────────────────────────────────────────────────────────────────┘

{
  "success": true,
  "action": "run",
  "verdict": "Accepted",
  "testResults": [
    {
      "testCase": 1,
      "input": "[2,7,11,15], 9",        ← VISIBLE
      "expectedOutput": "[0,1]",         ← VISIBLE
      "actualOutput": "[0,1]",           ← VISIBLE
      "passed": true,
      "verdict": "Accepted",
      "executionTime": 0.023,
      "memory": 4096
    }
  ],
  "testsPassed": 2,
  "totalTests": 2,
  "executionTime": 0.041,
  "memory": 4096
}

┌─────────────────────────────────────────────────────────────────┐
│              SUBMIT RESPONSE (Summary Only)                      │
└─────────────────────────────────────────────────────────────────┘

{
  "success": true,
  "action": "submit",
  "verdict": "Accepted",
  "testsPassed": 5,                     ← ONLY COUNT
  "totalTests": 5,                      ← ONLY COUNT
  "executionTime": 0.125,
  "memory": 4096,
  "submissionId": "uuid"                ← STORED
}

Note: NO test results, inputs, or outputs for SUBMIT
```

---

## Error Handling Matrix

| Error Type | HTTP Status | Response | Retry? |
|------------|-------------|----------|--------|
| Missing problemId | 400 | "problemId is required" | No |
| Empty wrappedCode | 400 | "wrappedCode cannot be empty" | No |
| Invalid mode | 400 | "mode must be 'practice' or 'battle'" | No |
| Invalid action | 400 | "action must be 'run' or 'submit'" | No |
| SUBMIT without auth | 401 | "Authentication required" | No |
| Invalid JWT token | 401 | "Invalid or expired token" | No |
| Problem not found | 500 | "Problem not found" | No |
| Judge0 network error | - | "Internal Error" verdict | Yes (once) |
| Compilation error | 200 | "Compilation Error" verdict | No |
| Runtime error | 200 | "Runtime Error" verdict | No |
| Time limit exceeded | 200 | "Time Limit Exceeded" verdict | No |
| Wrong answer | 200 | "Wrong Answer" verdict | No |

---

## Summary

This verdict system implements a complete LeetCode-style judging platform with:

✅ **Authentication**: JWT for SUBMIT, optional for RUN  
✅ **Test Case Selection**: Automatic based on action  
✅ **Stop on First Failure**: Efficient execution  
✅ **Retry Logic**: Handles transient network failures  
✅ **Output Normalization**: Fair comparison  
✅ **Submission Storage**: Complete history tracking  
✅ **Mode Support**: Same logic for Practice and Battle  

The system is production-ready and fully integrated! 🚀
