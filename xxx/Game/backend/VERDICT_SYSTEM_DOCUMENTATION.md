# Verdict System - Complete Documentation

## Overview

This document explains the **LeetCode-style verdict system** implemented for the CodeDuel Arena platform. The verdict system executes user code against test cases, compares outputs, and returns verdicts like "Accepted", "Wrong Answer", "Compilation Error", etc.

---

## Architecture

### Components

1. **`verdict_service.py`** - Core verdict logic service
2. **`/api/code/verdict`** - HTTP endpoint for verdict requests
3. **`submissions_collection`** - MongoDB collection for storing submission history
4. **Judge0 Service** - Code execution engine (already exists)

### System Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     User submits code                            │
│              (Frontend calls /api/code/verdict)                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ POST /api/code/verdict
                             │ { problemId, wrappedCode, mode, action }
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AUTHENTICATION CHECK                          │
│   • SUBMIT → JWT Required (401 if missing)                      │
│   • RUN → Optional (works as guest)                             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  FETCH PROBLEM & TEST CASES                      │
│   • Fetch problem from problems_collection                       │
│   • If action == "run" → Use sampleTestCases                    │
│   • If action == "submit" → Use hiddenTestCases                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              EXECUTE CODE AGAINST TEST CASES                     │
│                (STOP ON FIRST FAILURE)                           │
│                                                                   │
│   For each test case:                                            │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │ 1. Format input for Judge0                              │  │
│   │ 2. Execute code with Judge0 (retry once on failure)     │  │
│   │ 3. Check for errors:                                    │  │
│   │    • Compilation Error → STOP, return verdict           │  │
│   │    • Runtime Error → STOP, return verdict               │  │
│   │    • Time Limit Exceeded → STOP, return verdict         │  │
│   │    • Internal Error → STOP, return verdict              │  │
│   │ 4. Compare output with expectedOutput                   │  │
│   │    • Normalize whitespace and line breaks               │  │
│   │    • If mismatch → Wrong Answer, STOP                   │  │
│   │    • If match → Continue to next test                   │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                   │
│   All tests passed → Verdict: "Accepted"                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  STORE SUBMISSION (SUBMIT only)                  │
│   • Store in submissions_collection                              │
│   • userId (or "guest"), problemId, verdict, etc.               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     RETURN RESPONSE                              │
│   • RUN: Detailed test results with inputs/outputs              │
│   • SUBMIT: Only verdict and counts (no outputs)                │
└─────────────────────────────────────────────────────────────────┘
```

---

## API Specification

### Endpoint: POST `/api/code/verdict`

**Purpose**: Execute code against test cases and return LeetCode-style verdict

#### Authentication

| Action | Auth Required | Behavior |
|--------|---------------|----------|
| **RUN** | Optional | Works as guest if no token provided |
| **SUBMIT** | Required | Returns 401 if JWT token missing |

#### Request Body

```json
{
  "problemId": "two-sum",
  "wrappedCode": "full C++ program as string",
  "mode": "practice",
  "action": "run",
  "battleId": "optional-battle-id"
}
```

**Field Descriptions:**

| Field | Type | Required | Values | Description |
|-------|------|----------|--------|-------------|
| `problemId` | string | Yes | Any valid problem ID | Problem to test against |
| `wrappedCode` | string | Yes | Full C++ program | Wrapped code from wrapper generator |
| `mode` | string | Yes | `"practice"` or `"battle"` | Execution mode |
| `action` | string | Yes | `"run"` or `"submit"` | Test type |
| `battleId` | string | No | UUID string | Battle ID (for battle mode only) |

#### Response for RUN

```json
{
  "success": true,
  "action": "run",
  "verdict": "Accepted",
  "testResults": [
    {
      "testCase": 1,
      "input": "[2,7,11,15], 9",
      "expectedOutput": "[0,1]",
      "actualOutput": "[0,1]",
      "passed": true,
      "verdict": "Accepted",
      "executionTime": 0.023,
      "memory": 4096,
      "error": null
    },
    {
      "testCase": 2,
      "input": "[3,2,4], 6",
      "expectedOutput": "[1,2]",
      "actualOutput": "[1,2]",
      "passed": true,
      "verdict": "Accepted",
      "executionTime": 0.018,
      "memory": 3584,
      "error": null
    }
  ],
  "testsPassed": 2,
  "totalTests": 2,
  "executionTime": 0.041,
  "memory": 4096,
  "error_message": null
}
```

#### Response for SUBMIT (All Passed)

```json
{
  "success": true,
  "action": "submit",
  "verdict": "Accepted",
  "testsPassed": 5,
  "totalTests": 5,
  "executionTime": 0.125,
  "memory": 4096,
  "error_message": null,
  "submissionId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

#### Response for SUBMIT (Failed)

```json
{
  "success": false,
  "action": "submit",
  "verdict": "Wrong Answer",
  "testsPassed": 2,
  "totalTests": 5,
  "executionTime": 0.055,
  "memory": 3584,
  "error_message": "Output does not match expected output",
  "submissionId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

#### Error Responses

**401 Unauthorized** (SUBMIT without token):
```json
{
  "detail": "Authentication required for SUBMIT action"
}
```

**400 Bad Request** (Invalid input):
```json
{
  "detail": "problemId is required"
}
```

**500 Internal Server Error** (System error):
```json
{
  "detail": "Verdict system error: <error message>"
}
```

---

## Verdict Rules

### Verdict Priority (Stop on First Failure)

The system checks errors in this exact order and **stops at the first failure**:

1. **Compilation Error**
   - Triggered when: Code fails to compile
   - Judge0 status: `compilation_error`
   - Example: Missing semicolon, syntax error

2. **Runtime Error**
   - Triggered when: Code crashes during execution
   - Judge0 status: `runtime_error`
   - Example: Segmentation fault, division by zero

3. **Time Limit Exceeded**
   - Triggered when: Execution takes longer than 2 seconds
   - Judge0 status: `time_limit_exceeded`
   - Example: Infinite loop, inefficient algorithm

4. **Wrong Answer**
   - Triggered when: Output doesn't match expected output
   - Comparison: After normalizing whitespace
   - Example: `[0,1]` vs `[1,0]`

5. **Accepted**
   - Triggered when: ALL test cases pass
   - All outputs match expected outputs

6. **Internal Error**
   - Triggered when: Judge0 service fails or network error
   - Retry: Automatically retries once on network failure

### Stop on First Failure Behavior

**Example 1: Compilation Error**
```
Test Case 1: Not executed (compilation failed)
Test Case 2: Not executed
Test Case 3: Not executed
Test Case 4: Not executed
Test Case 5: Not executed

Verdict: "Compilation Error"
Tests Passed: 0 / 5
```

**Example 2: Wrong Answer on Test 3**
```
Test Case 1: Passed ✓
Test Case 2: Passed ✓
Test Case 3: Failed ✗ (Output mismatch)
Test Case 4: Not executed (stopped after first failure)
Test Case 5: Not executed

Verdict: "Wrong Answer"
Tests Passed: 2 / 5
```

**Example 3: All Passed**
```
Test Case 1: Passed ✓
Test Case 2: Passed ✓
Test Case 3: Passed ✓
Test Case 4: Passed ✓
Test Case 5: Passed ✓

Verdict: "Accepted"
Tests Passed: 5 / 5
```

---

## Output Comparison

### Normalization Logic

Before comparing outputs, both actual and expected outputs are normalized:

1. **Trim whitespace**: Leading and trailing spaces removed
2. **Split into lines**: Split by newline character
3. **Trim each line**: Remove spaces from each line
4. **Remove empty lines**: Filter out blank lines
5. **Join with single newline**: Rejoin normalized lines

**Example:**

```
Input:        "  [0, 1]  \n\n  "
Normalized:   "[0, 1]"

Input:        "[0,1]\n"
Normalized:   "[0,1]"

Comparison:   "[0, 1]" ≠ "[0,1]"  → Wrong Answer
```

### Comparison Examples

| Actual Output | Expected Output | Match? | Reason |
|---------------|-----------------|--------|--------|
| `[0,1]` | `[0,1]` | ✅ Yes | Exact match |
| `[0, 1]` | `[0,1]` | ❌ No | Space difference |
| `[0,1]\n` | `[0,1]` | ✅ Yes | Trailing newline ignored |
| `  [0,1]  ` | `[0,1]` | ✅ Yes | Whitespace trimmed |
| `true` | `true` | ✅ Yes | Exact match |
| `True` | `true` | ❌ No | Case sensitive |
| `42` | `42.0` | ❌ No | Different format |

---

## Test Case Selection

### RUN vs SUBMIT

| Action | Test Cases Used | Visibility | Purpose |
|--------|----------------|------------|---------|
| **RUN** | `sampleTestCases` | Visible to user | Debugging and testing |
| **SUBMIT** | `hiddenTestCases` | Hidden from user | Final grading |

### Sample Test Cases (for RUN)

- **Count**: 1-2 per problem
- **Difficulty**: Simple, easy-to-understand
- **Purpose**: Help users debug their code
- **Response**: Includes inputs, expected outputs, and actual outputs

### Hidden Test Cases (for SUBMIT)

- **Count**: 3-5 per problem
- **Difficulty**: Comprehensive edge cases
- **Coverage**: Boundary conditions, edge values, special cases
- **Response**: Only verdict and count (no outputs shown)

---

## Retry Logic

### Judge0 Network Failure Handling

The verdict system automatically retries Judge0 execution on network failures:

```python
Attempt 1: Execute code
    ↓
Network timeout / connection error
    ↓
Wait 1 second
    ↓
Attempt 2: Execute code
    ↓
If still fails → Return "Internal Error"
```

**Retry Conditions:**
- `timeout` - Judge0 API request timed out
- `connection_error` - Failed to connect to Judge0
- `polling_timeout` - Polling timeout exceeded

**Non-Retry Errors:**
- `compilation_error` - Code issue, not network issue
- `runtime_error` - Code issue, not network issue
- `time_limit_exceeded` - Code issue, not network issue

---

## Submission Storage

### Database Schema

Submissions are stored in `submissions_collection`:

```javascript
{
  "_id": "uuid",
  "userId": "user-uuid" or "guest",
  "problemId": "two-sum",
  "mode": "practice",
  "action": "submit",
  "verdict": "Accepted",
  "testsPassed": 5,
  "totalTests": 5,
  "executionTime": 0.125,
  "memory": 4096,
  "submittedAt": "2025-01-15T10:30:00.000Z",
  "battleId": "battle-uuid" or null
}
```

### Storage Rules

| Action | Stored? | Why |
|--------|---------|-----|
| **RUN** | ❌ No | Temporary debugging, not permanent |
| **SUBMIT** | ✅ Yes | Official submission, needs history |

### Indexes

```javascript
// Composite index for user submission history
submissions_collection.create_index([("userId", 1), ("problemId", 1), ("submittedAt", -1)])

// Index for battle submissions
submissions_collection.create_index("battleId")
```

---

## Mode Handling

### Practice Mode vs Battle Mode

The verdict logic is **identical** for both modes. The `mode` parameter is used only for:

1. **Context tracking** - Knowing which mode the user was in
2. **Storage** - Storing mode in submission record
3. **Future features** - Potential mode-specific logic later

**Current Behavior:**
```
Practice Mode: Same verdict logic
Battle Mode: Same verdict logic
```

**Future Possibilities:**
- Battle mode time bonuses
- Battle mode scoring system
- Battle mode leaderboards

---

## Usage Examples

### Example 1: RUN with Valid Solution (Practice Mode)

**Step 1: Generate wrapper**
```bash
curl -X POST http://localhost:8001/api/code/generate-wrapper \
  -H "Content-Type: application/json" \
  -d '{
    "userCode": "vector<int> result;\nresult.push_back(0);\nresult.push_back(1);\nreturn result;",
    "language": "cpp",
    "problemMetadata": {
      "functionName": "twoSum",
      "className": "Solution",
      "returnType": "vector<int>",
      "parameters": [
        {"name": "nums", "type": "vector<int>&"},
        {"name": "target", "type": "int"}
      ],
      "inputFormat": ["array_int", "int"],
      "outputFormat": "array_int"
    }
  }'
```

**Step 2: Get verdict**
```bash
curl -X POST http://localhost:8001/api/code/verdict \
  -H "Content-Type: application/json" \
  -d '{
    "problemId": "two-sum",
    "wrappedCode": "<wrapped code from step 1>",
    "mode": "practice",
    "action": "run"
  }'
```

**Response:**
```json
{
  "success": true,
  "action": "run",
  "verdict": "Accepted",
  "testResults": [
    {
      "testCase": 1,
      "input": "[2,7,11,15], 9",
      "expectedOutput": "[0,1]",
      "actualOutput": "[0,1]",
      "passed": true,
      "verdict": "Accepted",
      "executionTime": 0.023,
      "memory": 4096
    }
  ],
  "testsPassed": 1,
  "totalTests": 1,
  "executionTime": 0.023,
  "memory": 4096
}
```

### Example 2: SUBMIT with Authentication (Practice Mode)

```bash
curl -X POST http://localhost:8001/api/code/verdict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{
    "problemId": "two-sum",
    "wrappedCode": "<wrapped code>",
    "mode": "practice",
    "action": "submit"
  }'
```

**Response:**
```json
{
  "success": true,
  "action": "submit",
  "verdict": "Accepted",
  "testsPassed": 5,
  "totalTests": 5,
  "executionTime": 0.125,
  "memory": 4096,
  "submissionId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

### Example 3: SUBMIT in Battle Mode

```bash
curl -X POST http://localhost:8001/api/code/verdict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{
    "problemId": "reverse-string",
    "wrappedCode": "<wrapped code>",
    "mode": "battle",
    "action": "submit",
    "battleId": "battle-12345"
  }'
```

**Response:**
```json
{
  "success": false,
  "action": "submit",
  "verdict": "Wrong Answer",
  "testsPassed": 2,
  "totalTests": 4,
  "executionTime": 0.055,
  "memory": 3584,
  "error_message": "Output does not match expected output",
  "submissionId": "b2c3d4e5-f6g7-8901-bcde-fg2345678901"
}
```

---

## Frontend Integration

### Complete Flow

```javascript
// Step 1: Get user code from Monaco editor
const userCode = editor.getValue();

// Step 2: Generate wrapper
const wrapperResponse = await fetch('/api/code/generate-wrapper', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    userCode,
    language: 'cpp',
    problemMetadata: currentProblem.metadata
  })
});
const { wrappedCode } = await wrapperResponse.json();

// Step 3: Get verdict
const verdictResponse = await fetch('/api/code/verdict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${userToken}`  // Optional for RUN
  },
  body: JSON.stringify({
    problemId: 'two-sum',
    wrappedCode,
    mode: 'practice',
    action: 'run'  // or 'submit'
  })
});
const verdict = await verdictResponse.json();

// Step 4: Display results
if (verdict.action === 'run') {
  // Show detailed test results
  verdict.testResults.forEach(test => {
    console.log(`Test ${test.testCase}: ${test.passed ? '✓' : '✗'}`);
    console.log(`Input: ${test.input}`);
    console.log(`Expected: ${test.expectedOutput}`);
    console.log(`Actual: ${test.actualOutput}`);
  });
} else {
  // Show only verdict for submit
  console.log(`Verdict: ${verdict.verdict}`);
  console.log(`Tests Passed: ${verdict.testsPassed}/${verdict.totalTests}`);
}
```

---

## Testing

### Manual Testing with curl

**Test 1: RUN without authentication**
```bash
curl -X POST http://localhost:8001/api/code/verdict \
  -H "Content-Type: application/json" \
  -d '{
    "problemId": "two-sum",
    "wrappedCode": "#include <iostream>\n#include <vector>\nusing namespace std;\nclass Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        vector<int> result;\n        result.push_back(0);\n        result.push_back(1);\n        return result;\n    }\n};\nint main() { return 0; }",
    "mode": "practice",
    "action": "run"
  }'
```

**Test 2: SUBMIT without authentication (should fail)**
```bash
curl -X POST http://localhost:8001/api/code/verdict \
  -H "Content-Type: application/json" \
  -d '{
    "problemId": "two-sum",
    "wrappedCode": "<code>",
    "mode": "practice",
    "action": "submit"
  }'
```

**Expected:** 401 Unauthorized

---

## Troubleshooting

### Common Issues

**Issue 1: "Authentication required for SUBMIT action"**
- **Cause**: JWT token missing for SUBMIT action
- **Solution**: Add `Authorization: Bearer <token>` header

**Issue 2: "Problem not found in database"**
- **Cause**: Invalid problemId
- **Solution**: Verify problem exists in problems_collection

**Issue 3: "No test cases found for action 'run'"**
- **Cause**: Problem missing sampleTestCases
- **Solution**: Run `python problem_test_cases.py` to populate test cases

**Issue 4: "Judge0 service unavailable after 2 attempts"**
- **Cause**: Judge0 API network issue
- **Solution**: Check Judge0 API key and network connectivity

**Issue 5: "Wrong Answer" but output looks correct**
- **Cause**: Whitespace or formatting difference
- **Solution**: Check normalized output (trim spaces, line breaks)

---

## Summary

✅ **Complete verdict system implemented**
- LeetCode-style judging logic
- Stop on first failure (industry standard)
- Retry logic for network failures
- Authentication handling (SUBMIT requires JWT)
- Guest support for RUN
- Submission storage
- Battle mode support

✅ **Key Features**
- **Test Case Selection**: Automatic based on RUN/SUBMIT
- **Output Comparison**: Normalized whitespace handling
- **Verdict Rules**: Compilation Error → Runtime Error → TLE → Wrong Answer → Accepted
- **Mode-Agnostic**: Same logic for Practice and Battle
- **Retry Logic**: Automatic retry on network failure
- **Submission History**: Stored for SUBMIT only

✅ **Production Ready**
- Comprehensive error handling
- No unhandled exceptions
- Clear API documentation
- Complete testing examples

The verdict system is now ready for integration with your frontend! 🚀
