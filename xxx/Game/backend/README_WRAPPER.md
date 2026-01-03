# Backend Wrapper Generator - Complete Guide

## 🎯 What Is This?

A **mode-agnostic backend wrapper generator** that converts user function code into full compilable C++ programs. Works for **BOTH Practice Mode and Battle Mode** without code duplication.

---

## ✅ What's Been Implemented

### **Core Files:**
- ✅ `/app/xxx/Game/backend/code_wrapper.py` - Main wrapper generator
- ✅ `/app/xxx/Game/backend/problem_templates.py` - Helper utilities for I/O
- ✅ `/app/xxx/Game/backend/server.py` - API endpoints (updated)
- ✅ `/app/xxx/Game/backend/test_wrapper.py` - Comprehensive test suite
- ✅ `/app/xxx/Game/backend/test_api.py` - API integration guide
- ✅ `/app/xxx/Game/backend/WRAPPER_ARCHITECTURE.md` - Full documentation

### **API Endpoints:**
- ✅ `POST /api/code/generate-wrapper` - Generate wrapper from user code
- ✅ `POST /api/code/test-wrapper` - Test with problem from database

### **Supported Data Types:**
- ✅ Integers (`int`)
- ✅ Strings (`string`)
- ✅ Boolean (`bool`)
- ✅ Integer Arrays (`vector<int>`)
- ✅ String Arrays (`vector<string>`)

---

## 🚀 Quick Start

### **1. Test the Wrapper Generator (Standalone)**

```bash
cd /app/xxx/Game/backend
python test_wrapper.py
```

**Output:** You'll see 3 test cases with generated C++ programs:
- Two Sum Problem (array + int → array)
- Valid Parentheses (string → bool)
- Reverse String Array (array → array)

### **2. Test the API Endpoint**

Make sure backend is running:
```bash
sudo supervisorctl status backend
# Should show: RUNNING
```

Test with curl:
```bash
curl -X POST http://localhost:8001/api/code/generate-wrapper \
  -H "Content-Type: application/json" \
  -d '{
    "userCode": "return a + b;",
    "language": "cpp",
    "problemMetadata": {
      "functionName": "add",
      "className": "Solution",
      "returnType": "int",
      "parameters": [
        {"name": "a", "type": "int"},
        {"name": "b", "type": "int"}
      ],
      "inputFormat": ["int", "int"],
      "outputFormat": "int"
    }
  }'
```

---

## 📊 How It Works

### **The Problem:**
Users write ONLY function logic (not full program):
```cpp
// USER CODE START
vector<int> result;
for (int i = 0; i < nums.size(); i++) {
    if (nums[i] == target) {
        result.push_back(i);
    }
}
return result;
// USER CODE END
```

### **The Solution:**
Backend wraps it into a full compilable program:
```cpp
#include <iostream>
#include <vector>
using namespace std;

// Helper functions (generated automatically)
vector<int> parseIntArray(const string& s) { /* ... */ }
void printIntArray(const vector<int>& arr) { /* ... */ }

// User's class (with injected code)
class Solution {
public:
    vector<int> findTarget(vector<int>& nums, int target) {
        // USER CODE INJECTED HERE
        vector<int> result;
        for (int i = 0; i < nums.size(); i++) {
            if (nums[i] == target) {
                result.push_back(i);
            }
        }
        return result;
    }
};

// Main function (handles I/O)
int main() {
    string line1;
    getline(cin, line1);
    vector<int> nums = parseIntArray(line1);
    
    string line2;
    getline(cin, line2);
    int target = stoi(line2);
    
    Solution solution;
    vector<int> result = solution.findTarget(nums, target);
    
    printIntArray(result);
    return 0;
}
```

---

## 🔧 API Usage

### **Endpoint: POST /api/code/generate-wrapper**

**Request:**
```json
{
  "userCode": "string - user's function implementation",
  "language": "cpp",
  "problemMetadata": {
    "functionName": "string - name of the function",
    "className": "Solution",
    "returnType": "string - C++ return type",
    "parameters": [
      {"name": "string", "type": "string - C++ type"}
    ],
    "inputFormat": ["array of format strings"],
    "outputFormat": "string - format string"
  }
}
```

**Response:**
```json
{
  "success": true,
  "wrappedCode": "string - full C++ program",
  "language": "cpp",
  "message": "Wrapper generated successfully"
}
```

### **Format Strings:**

| Format | C++ Type | Example Input | Example Output |
|--------|----------|---------------|----------------|
| `int` | `int` | `42` | `42` |
| `string` | `string` | `"hello"` | `hello` |
| `bool` | `bool` | `true` | `true` |
| `array_int` | `vector<int>` | `[1,2,3]` | `[1,2,3]` |
| `array_string` | `vector<string>` | `["a","b"]` | `["a","b"]` |

---

## 🎮 Integration with Practice/Battle Modes

### **Practice Mode (Frontend):**

```typescript
// app/(app)/practice/[problemId]/page.tsx

const handleSubmitCode = async () => {
  // 1. Extract user code from Monaco editor
  const userCode = extractUserCode(editorRef.current);
  
  // 2. Get problem metadata
  const problemMetadata = problem.metadata; // from database
  
  // 3. Generate wrapper
  const response = await fetch(`${API_URL}/api/code/generate-wrapper`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      userCode,
      language: 'cpp',
      problemMetadata
    })
  });
  
  const { wrappedCode } = await response.json();
  
  // 4. Send to Judge0
  const testResults = await executeOnJudge0(wrappedCode, testCases);
  
  // 5. Show results
  setOutput({
    status: testResults.allPassed ? 'success' : 'error',
    message: testResults.details
  });
};
```

### **Battle Mode (Frontend):**

```typescript
// app/(app)/battle/[matchId]/page.tsx

const handleSubmitCode = async () => {
  // 1. Extract user code
  const userCode = extractUserCode(editorRef.current);
  
  // 2. Get problem metadata
  const problemMetadata = battleProblem.metadata;
  
  // 3. Generate wrapper (SAME API!)
  const response = await fetch(`${API_URL}/api/code/generate-wrapper`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      userCode,
      language: 'cpp',
      problemMetadata
    })
  });
  
  const { wrappedCode } = await response.json();
  
  // 4. Send to Judge0 (hidden test cases)
  const battleResults = await executeOnJudge0(wrappedCode, hiddenTestCases);
  
  // 5. Update battle status
  if (battleResults.allPassed) {
    await updateBattleWinner(currentUser.id, matchId);
  }
};
```

**Key Point:** Both modes call the **SAME API** with the **SAME logic**. The difference is in what they do with the results!

---

## 📋 Problem Metadata in MongoDB

Add this to your `problems` collection:

```javascript
{
  "problem_id": "two-sum",
  "title": "Two Sum",
  "description": "Find two numbers that add up to target",
  "difficulty": "Easy",
  "category": "Arrays",
  "examples": [...],
  "testCases": [...],
  
  // ADD THIS FOR WRAPPER GENERATION
  "metadata": {
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
}
```

---

## 🧪 Testing Examples

### **Test 1: Simple Addition**

```bash
curl -X POST http://localhost:8001/api/code/generate-wrapper \
  -H "Content-Type: application/json" \
  -d '{
    "userCode": "return a + b;",
    "language": "cpp",
    "problemMetadata": {
      "functionName": "add",
      "returnType": "int",
      "parameters": [
        {"name": "a", "type": "int"},
        {"name": "b", "type": "int"}
      ],
      "inputFormat": ["int", "int"],
      "outputFormat": "int"
    }
  }'
```

### **Test 2: String Reversal**

```bash
curl -X POST http://localhost:8001/api/code/generate-wrapper \
  -H "Content-Type: application/json" \
  -d '{
    "userCode": "string result = s;\nreverse(result.begin(), result.end());\nreturn result;",
    "language": "cpp",
    "problemMetadata": {
      "functionName": "reverseString",
      "returnType": "string",
      "parameters": [{"name": "s", "type": "string"}],
      "inputFormat": ["string"],
      "outputFormat": "string"
    }
  }'
```

### **Test 3: Array Filtering**

```bash
curl -X POST http://localhost:8001/api/code/generate-wrapper \
  -H "Content-Type: application/json" \
  -d '{
    "userCode": "vector<int> result;\nfor(int num : nums) {\n  if(num > 0) result.push_back(num);\n}\nreturn result;",
    "language": "cpp",
    "problemMetadata": {
      "functionName": "filterPositive",
      "returnType": "vector<int>",
      "parameters": [{"name": "nums", "type": "vector<int>&"}],
      "inputFormat": ["array_int"],
      "outputFormat": "array_int"
    }
  }'
```

---

## 🔍 Verification

### **1. Check Backend Status:**
```bash
sudo supervisorctl status backend
# Should show: RUNNING
```

### **2. Check Logs:**
```bash
tail -f /var/log/supervisor/backend.err.log
```

### **3. Test Import:**
```bash
cd /app/xxx/Game/backend
python -c "from code_wrapper import generate_wrapper; print('✅ OK')"
```

### **4. Test Generation:**
```bash
cd /app/xxx/Game/backend
python test_wrapper.py
```

---

## 📈 Future Enhancements

### **Phase 2: More Languages**
- Python wrapper generator
- Java wrapper generator
- JavaScript wrapper generator

### **Phase 3: Complex Data Types**
- 2D Arrays
- Linked Lists
- Trees
- Graphs

### **Phase 4: Optimization**
- Cache generated wrappers
- Pre-compile common templates
- Parallel execution for multiple test cases

---

## 🎓 Key Design Principles

### **1. Separation of Concerns**
```
Wrapper Generator: userCode + metadata → fullProgram
Practice Mode: fullProgram → testResults → displayToUser
Battle Mode: fullProgram → battleResults → updateLeaderboard
```

### **2. Single Responsibility**
The wrapper generator has ONE job: Convert function to program. It doesn't care about:
- ❌ Practice vs Battle
- ❌ Test cases
- ❌ User authentication
- ❌ Database operations
- ❌ Code execution

### **3. Mode-Agnostic Design**
```python
# ✅ GOOD: One function for all modes
def generate_wrapper(code, metadata):
    return full_program

# ❌ BAD: Separate functions per mode
def generate_practice_wrapper(code, metadata):
    # duplicated logic
def generate_battle_wrapper(code, metadata):
    # duplicated logic
```

---

## ✅ Summary

### **What's Working:**
- ✅ Backend wrapper generator (C++)
- ✅ Supports: int, string, bool, arrays
- ✅ Mode-agnostic API endpoints
- ✅ Comprehensive test suite
- ✅ Full documentation

### **How to Use:**
1. **Frontend:** Extract user code from Monaco editor
2. **Frontend:** Call `/api/code/generate-wrapper` with metadata
3. **Backend:** Generate full C++ program
4. **Frontend:** Send to Judge0 for execution
5. **Frontend:** Display results (practice) or update battle (battle mode)

### **Next Steps:**
1. ✅ Update MongoDB problems with `metadata` field
2. ✅ Integrate in Practice Mode frontend
3. ✅ Integrate in Battle Mode frontend
4. ⏳ Connect to Judge0 or execution engine (separate phase)

---

## 📞 Questions?

See detailed documentation: `WRAPPER_ARCHITECTURE.md`

Run tests: `python test_wrapper.py`

Test API: `python test_api.py`

---

**The backend wrapper generator is production-ready and hackathon-safe! 🚀**
