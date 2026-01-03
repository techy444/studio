# Judge0 "Web Server Error" Fix

## Problem
The endpoint was returning `HTTP 500 Internal Server Error` with message "Web server returned an unknown error" when Judge0 API key was not configured.

## Root Cause
The `Judge0Service.__init__()` was raising a `ValueError` during initialization when the API key was missing. This caused the entire endpoint to crash with a 500 error instead of returning a proper error response.

## Solution Applied

### 1. Changed Service Initialization
**Before:**
```python
def __init__(self):
    self.api_key = os.getenv('JUDGE0_API_KEY', '')
    if not self.api_key:
        raise ValueError("JUDGE0_API_KEY not found...")  # ❌ Crashes on init
```

**After:**
```python
def __init__(self):
    self.api_key = os.getenv('JUDGE0_API_KEY', '')
    # Don't raise error - handle during execution instead  # ✅ Deferred validation
```

### 2. Added Runtime Validation
Added API key check at the beginning of `execute_code()`:
```python
def execute_code(self, source_code, stdin_input, mode):
    # Check if API key is configured
    if not self.api_key:
        return {
            "success": False,
            "status": "configuration_error",
            "error_message": "JUDGE0_API_KEY not configured..."
        }
    # ... rest of execution
```

### 3. Proper HTTP Status Codes
Updated endpoint to return correct status codes:
```python
result = judge0_execute_code(...)

# Check for configuration error
if result.get("status") == "configuration_error":
    raise HTTPException(
        status_code=503,  # ✅ Service Unavailable
        detail=result.get("error_message")
    )

return result
```

## HTTP Status Codes Now Returned

| Scenario | Status Code | Response |
|----------|-------------|----------|
| Missing API key | `503 Service Unavailable` | Clear configuration error message |
| Empty code | `400 Bad Request` | "wrappedCode cannot be empty" |
| Invalid mode | `400 Bad Request` | "mode must be 'practice' or 'battle'" |
| Judge0 API error | `200 OK` | `{"success": false, "status": "submission_failed"}` |
| Compilation error | `200 OK` | `{"success": false, "status": "compilation_error"}` |
| Runtime error | `200 OK` | `{"success": false, "status": "runtime_error"}` |
| Success | `200 OK` | `{"success": true, "status": "accepted"}` |

## Testing Results

### Test 1: Missing API Key
```bash
curl -X POST http://localhost:8001/api/code/execute \
  -H "Content-Type: application/json" \
  -d '{"wrappedCode": "int main() {}", "stdinInput": "", "mode": "practice"}'
```
**Response:**
```
HTTP/1.1 503 Service Unavailable
{"detail":"JUDGE0_API_KEY not configured. Please add your Judge0 API key to the .env file."}
```
✅ **Fixed:** Now returns 503 instead of 500

### Test 2: Empty Code
```bash
curl -X POST http://localhost:8001/api/code/execute \
  -H "Content-Type: application/json" \
  -d '{"wrappedCode": "", "stdinInput": "", "mode": "practice"}'
```
**Response:**
```
HTTP/1.1 400 Bad Request
{"detail":"wrappedCode cannot be empty"}
```
✅ **Working:** Proper validation error

### Test 3: Invalid Mode
```bash
curl -X POST http://localhost:8001/api/code/execute \
  -H "Content-Type: application/json" \
  -d '{"wrappedCode": "int main() {}", "stdinInput": "", "mode": "invalid"}'
```
**Response:**
```
HTTP/1.1 400 Bad Request
{"detail":"mode must be 'practice' or 'battle'"}
```
✅ **Working:** Proper validation error

## Benefits

1. ✅ **No more 500 errors** for configuration issues
2. ✅ **Clear error messages** guide users to fix the problem
3. ✅ **Proper HTTP semantics** (503 for service unavailable, 400 for bad requests)
4. ✅ **Server starts successfully** even without API key
5. ✅ **Frontend can handle errors** properly based on status codes

## Next Steps

To use the Judge0 service:

1. Get API key from: https://rapidapi.com/judge0-official/api/judge0-ce
2. Create `/app/backend/.env` with:
   ```bash
   JUDGE0_API_KEY=your-actual-api-key-here
   ```
3. Restart backend: `sudo supervisorctl restart backend`
4. Test execution with real API key

## Frontend Error Handling

The frontend can now handle errors properly:

```javascript
try {
  const response = await fetch('/api/code/execute', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ wrappedCode, stdinInput, mode })
  });

  if (response.status === 503) {
    // Service not configured
    showError('Judge0 service not configured. Please contact support.');
  } else if (response.status === 400) {
    // Bad request
    const error = await response.json();
    showError(error.detail);
  } else if (response.ok) {
    const result = await response.json();
    if (result.success) {
      showSuccess(result.stdout);
    } else {
      showError(result.error_message);
    }
  }
} catch (error) {
  showError('Network error: ' + error.message);
}
```

## Summary

The "Web server returned an unknown error" is now **FIXED**. The endpoint returns:
- **503** for configuration errors (missing API key)
- **400** for validation errors (bad input)
- **200** for execution results (success or failure)

All error messages are clear and actionable.
