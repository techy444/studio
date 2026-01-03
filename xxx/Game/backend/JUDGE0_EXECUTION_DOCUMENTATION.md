# Judge0 Execution Service - Documentation

## Overview

This document explains the Judge0-based code execution layer implemented for the CodeDuel Arena platform. The service provides safe, isolated, and fault-tolerant C++ code compilation and execution for both **Practice Mode** and **Battle Mode**.

---

## Architecture

### Components

1. **`judge0_service.py`** - Core Judge0 integration service
2. **`/api/code/execute`** - HTTP endpoint for code execution
3. **RapidAPI Judge0 CE** - External compilation and execution service

### Execution Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     Frontend (Monaco Editor)                     │
│                  User writes function code                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ 1. User code + Problem metadata
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              POST /api/code/generate-wrapper                     │
│              (Wrapper Generator - Already Exists)                │
│   • Takes user function code                                     │
│   • Wraps in full C++ program with I/O handling                  │
│   • Returns wrappedCode                                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ 2. Wrapped C++ code + stdin input
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  POST /api/code/execute                          │
│                  (NEW - Code Execution)                          │
│   • Accepts: wrappedCode, stdinInput, mode                       │
│   • Validates inputs                                             │
│   • Calls Judge0 service                                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ 3. Submit to Judge0
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                 judge0_service.execute_code()                    │
│                                                                   │
│   Step 1: Submit Code                                            │
│   ├─ POST to Judge0 API with source code and stdin              │
│   ├─ Set limits: 2s execution, 256MB memory                     │
│   └─ Receive submission token                                   │
│                                                                   │
│   Step 2: Poll for Results                                      │
│   ├─ GET submission status every 0.5s                           │
│   ├─ Check if still processing (status 1 or 2)                  │
│   ├─ Max polling timeout: 10 seconds                            │
│   └─ Return when completed or timeout                           │
│                                                                   │
│   Step 3: Parse Results                                         │
│   ├─ Extract stdout, stderr, compile_output                     │
│   ├─ Categorize status (accepted, error, TLE, etc.)             │
│   └─ Return structured result                                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ 4. Execution result
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend                                 │
│   • Receives: success, status, stdout, stderr, time, memory     │
│   • Displays results to user                                     │
│   • (Verdict logic handled separately by frontend/app)          │
└─────────────────────────────────────────────────────────────────┘
```

---

## API Specification

### Endpoint: POST `/api/code/execute`

**Purpose**: Execute wrapped C++ code using Judge0 for both Practice and Battle modes.

#### Request Body

```json
{
  "wrappedCode": "string (full C++ program)",
  "stdinInput": "string (optional, default: '')",
  "mode": "string ('practice' or 'battle')"
}
```

**Example Request**:
```json
{
  "wrappedCode": "#include <iostream>\n#include <vector>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        vector<int> result;\n        return result;\n    }\n};\n\nint main() {\n    // Input parsing and execution logic\n    return 0;\n}",
  "stdinInput": "[2,7,11,15]\n9",
  "mode": "practice"
}
```

#### Response

**Success Response** (200 OK):
```json
{
  "success": true,
  "status": "accepted",
  "stdout": "[0,1]",
  "stderr": "",
  "compile_output": "",
  "execution_time": 0.023,
  "memory": 4096,
  "status_id": 3,
  "error_message": ""
}
```

**Compilation Error Response** (200 OK):
```json
{
  "success": false,
  "status": "compilation_error",
  "stdout": "",
  "stderr": "",
  "compile_output": "error: expected ';' before '}' token\n   }\n   ^",
  "execution_time": 0.0,
  "memory": 0,
  "status_id": 6,
  "error_message": "Compilation failed: error: expected ';' before '}' token"
}
```

**Runtime Error Response** (200 OK):
```json
{
  "success": false,
  "status": "runtime_error",
  "stdout": "",
  "stderr": "Segmentation fault (core dumped)",
  "compile_output": "",
  "execution_time": 0.001,
  "memory": 2048,
  "status_id": 7,
  "error_message": "Runtime error: Runtime Error(SIGSEGV) - Segmentation fault"
}
```

**Time Limit Exceeded Response** (200 OK):
```json
{
  "success": false,
  "status": "time_limit_exceeded",
  "stdout": "",
  "stderr": "",
  "compile_output": "",
  "execution_time": 2.0,
  "memory": 1024,
  "status_id": 5,
  "error_message": "Time limit exceeded (>2.0s)"
}
```

---

## Error Handling

### Error Categories

| Status | Description | success | status_id |
|--------|-------------|---------|-----------|
| **Accepted** | Code compiled and ran successfully | `true` | 3 |
| **Compilation Error** | Code failed to compile | `false` | 6 |
| **Runtime Error** | Code crashed during execution | `false` | 7-12 |
| **Time Limit Exceeded** | Execution took too long | `false` | 5 |
| **Internal Error** | Judge0 system error | `false` | 13 |
| **Network Error** | Failed to connect to Judge0 API | `false` | 0 |
| **Timeout** | Polling timeout (10s exceeded) | `false` | 0 |

### Fault Tolerance

The service handles ALL failure scenarios:

1. **Network Failures**:
   - Connection timeout
   - DNS resolution errors
   - Network unreachable

2. **Judge0 API Failures**:
   - HTTP 4xx/5xx errors
   - Invalid API key
   - Rate limiting
   - Service unavailable

3. **Compilation Failures**:
   - Syntax errors
   - Missing headers
   - Type mismatches

4. **Runtime Failures**:
   - Segmentation faults (SIGSEGV)
   - Division by zero (SIGFPE)
   - Out of memory
   - Infinite loops (handled by TLE)

5. **System Failures**:
   - Judge0 internal errors
   - Resource exhaustion
   - Unexpected exceptions

All errors are caught, categorized, and returned with descriptive error messages. **No unhandled exceptions reach the API layer**.

---

## Execution Limits

| Parameter | Value | Purpose |
|-----------|-------|---------|
| **CPU Time Limit** | 2.0 seconds | Max execution time |
| **CPU Extra Time** | 0.5 seconds | Grace period for cleanup |
| **Wall Time Limit** | 5.0 seconds | Max compilation time |
| **Memory Limit** | 256 MB (262144 KB) | Max memory usage |
| **Polling Timeout** | 10.0 seconds | Max time to wait for results |
| **Polling Interval** | 0.5 seconds | Time between status checks |
| **Network Disabled** | Yes | No network access during execution |

---

## Usage Examples

### Example 1: Practice Mode - Valid Solution

**Step 1**: Generate wrapper
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

**Step 2**: Execute wrapped code
```bash
curl -X POST http://localhost:8001/api/code/execute \
  -H "Content-Type: application/json" \
  -d '{
    "wrappedCode": "<full wrapped C++ code from step 1>",
    "stdinInput": "[2,7,11,15]\n9",
    "mode": "practice"
  }'
```

**Expected Result**:
```json
{
  "success": true,
  "status": "accepted",
  "stdout": "[0,1]",
  "stderr": "",
  "compile_output": "",
  "execution_time": 0.015,
  "memory": 3584,
  "status_id": 3,
  "error_message": ""
}
```

### Example 2: Battle Mode - Compilation Error

**Request**:
```bash
curl -X POST http://localhost:8001/api/code/execute \
  -H "Content-Type: application/json" \
  -d '{
    "wrappedCode": "#include <iostream>\nint main() { missing_semicolon }",
    "stdinInput": "",
    "mode": "battle"
  }'
```

**Response**:
```json
{
  "success": false,
  "status": "compilation_error",
  "stdout": "",
  "stderr": "",
  "compile_output": "prog.cpp:2:35: error: expected ';' before '}' token\n int main() { missing_semicolon }\n                                   ^",
  "execution_time": 0.0,
  "memory": 0,
  "status_id": 6,
  "error_message": "Compilation failed: prog.cpp:2:35: error: expected ';' before '}' token"
}
```

---

## Mode-Agnostic Design

The execution service is **fully mode-agnostic**:

- **Practice Mode**: Frontend calls with `mode: "practice"`
- **Battle Mode**: Frontend calls with `mode: "battle"`

The `mode` parameter is used only for:
- Logging and debugging
- Future analytics
- Context tracking

**The execution logic is IDENTICAL for both modes**. This ensures:
- Consistent behavior
- No mode-specific bugs
- Easy testing and maintenance
- Shared code path = fewer bugs

---

## Environment Setup

### Required Environment Variables

Add to `/app/backend/.env`:

```bash
# Judge0 API Configuration (RapidAPI)
JUDGE0_API_URL=https://judge0-ce.p.rapidapi.com
JUDGE0_API_KEY=your-rapidapi-key-here
```

### Getting Judge0 API Key

1. Go to [RapidAPI Judge0 CE](https://rapidapi.com/judge0-official/api/judge0-ce)
2. Sign up / Log in
3. Subscribe to a plan (free tier available)
4. Copy your API key from the dashboard
5. Add to `.env` file

---

## Testing

### Manual Testing with curl

```bash
# Test execution endpoint (replace wrappedCode with actual wrapped code)
curl -X POST http://localhost:8001/api/code/execute \
  -H "Content-Type: application/json" \
  -d '{
    "wrappedCode": "#include <iostream>\nusing namespace std;\nint main() { cout << \"Hello, World!\" << endl; return 0; }",
    "stdinInput": "",
    "mode": "practice"
  }'
```

### Expected Output

```json
{
  "success": true,
  "status": "accepted",
  "stdout": "Hello, World!\n",
  "stderr": "",
  "compile_output": "",
  "execution_time": 0.012,
  "memory": 3072,
  "status_id": 3,
  "error_message": ""
}
```

---

## Integration Points

### Frontend Integration

**Practice Mode Flow**:
```javascript
// 1. Get user code from Monaco editor
const userCode = editor.getValue();

// 2. Generate wrapper
const wrapperResponse = await fetch('/api/code/generate-wrapper', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    userCode,
    language: 'cpp',
    problemMetadata: currentProblem.metadata
  })
});
const { wrappedCode } = await wrapperResponse.json();

// 3. Execute code
const executeResponse = await fetch('/api/code/execute', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    wrappedCode,
    stdinInput: testCase.input,
    mode: 'practice'
  })
});
const result = await executeResponse.json();

// 4. Display results
if (result.success) {
  console.log('Output:', result.stdout);
  console.log('Time:', result.execution_time, 's');
} else {
  console.error('Error:', result.error_message);
  console.error('Status:', result.status);
}
```

**Battle Mode Flow**:
Same as Practice Mode, just change `mode: 'battle'`.

---

## Future Enhancements

### Verdict Logic (To Be Implemented Separately)

The current service returns **raw execution results**. Verdict logic (comparing output with expected output) should be implemented separately:

```python
# Future endpoint: /api/code/verify
def verify_solution(execution_result, expected_output):
    if not execution_result['success']:
        return {'verdict': 'Error', 'message': execution_result['error_message']}
    
    if execution_result['stdout'].strip() == expected_output.strip():
        return {'verdict': 'Accepted', 'message': 'Correct output'}
    else:
        return {'verdict': 'Wrong Answer', 'message': 'Output does not match'}
```

### Batch Testing

For running multiple test cases:

```python
# Future endpoint: /api/code/batch-execute
async def batch_execute(wrapped_code, test_cases, mode):
    results = []
    for test_case in test_cases:
        result = await execute_code(wrapped_code, test_case.input, mode)
        results.append(result)
    return results
```

---

## Security Considerations

### Isolation

- Code execution happens in **Judge0's isolated sandbox**
- Network access is **disabled** during execution
- File system access is **restricted**
- No access to host system resources

### Resource Limits

- **CPU time**: 2 seconds max
- **Memory**: 256 MB max
- **Compilation time**: 5 seconds max

### Input Validation

- `wrappedCode` must not be empty
- `mode` must be 'practice' or 'battle'
- All inputs are sanitized before sending to Judge0

---

## Troubleshooting

### Common Issues

1. **"JUDGE0_API_KEY not found"**
   - Add `JUDGE0_API_KEY` to `.env` file
   - Restart backend server

2. **"Failed to connect to Judge0 API"**
   - Check internet connection
   - Verify Judge0 API URL is correct
   - Check if RapidAPI is accessible

3. **"Polling timeout after 10s"**
   - Judge0 service might be overloaded
   - Check RapidAPI plan limits
   - Try again after a few seconds

4. **"Invalid API key"**
   - Verify API key is correct
   - Check RapidAPI subscription status
   - Ensure API key has correct permissions

---

## Summary

The Judge0 execution service provides:

✅ **Safe**: Isolated sandbox execution  
✅ **Stable**: Comprehensive error handling  
✅ **Fault-tolerant**: Handles all failure scenarios  
✅ **Mode-agnostic**: Works for Practice AND Battle  
✅ **Production-ready**: No server crashes, no unhandled exceptions  
✅ **Well-documented**: Clear API spec and usage examples  

The service returns **raw execution results only**. Verdict logic and output comparison should be implemented separately based on your specific requirements.
