# Backend Wrapper Generator - Architecture & Design

## 📋 Overview

This document explains the **mode-agnostic backend wrapper generator** for the online coding judge platform. The wrapper generator converts user function code into full compilable C++ programs that work for **BOTH Practice Mode and Battle Mode**.

---

## 🏗️ Architecture

### **Core Principle: Mode-Agnostic Design**

```
┌─────────────────────────────────────────────────┐
│         PRACTICE MODE (Frontend)                │
│   - User writes function logic                  │
│   - Test against sample cases                   │
│   - Show detailed feedback                      │
└────────────────┬────────────────────────────────┘
                 │
                 │ POST /api/code/generate-wrapper
                 │ { userCode, problemMetadata }
                 ▼
┌─────────────────────────────────────────────────┐
│         BATTLE MODE (Frontend)                  │
│   - User writes function logic                  │
│   - Compete against opponent                    │
│   - Time-limited submission                     │
└────────────────┬────────────────────────────────┘
                 │
                 │ POST /api/code/generate-wrapper
                 │ { userCode, problemMetadata }
                 ▼
┌─────────────────────────────────────────────────┐
│      SHARED API ENDPOINT (Backend)              │
│   /api/code/generate-wrapper                    │
│   - No mode awareness                           │
│   - Pure transformation                         │
└────────────────┬────────────────────────────────┘
                 │
                 │ calls
                 ▼
┌─────────────────────────────────────────────────┐
│   WRAPPER GENERATOR (code_wrapper.py)           │
│   generate_wrapper(userCode, metadata)          │
│   - Language-agnostic interface                 │
│   - Returns full compilable program             │
└────────────────┬────────────────────────────────┘
                 │
                 │ uses
                 ▼
┌─────────────────────────────────────────────────┐
│   HELPER UTILITIES (problem_templates.py)       │
│   - Input parsers (int, string, arrays)         │
│   - Output formatters                           │
│   - C++ code generation utilities               │
└─────────────────────────────────────────────────┘
```

### **Key Design Decision: Why Mode-Agnostic?**

❌ **Bad Design (Mode-Aware):**
```python
def generate_practice_wrapper(user_code, metadata):
    # Practice-specific logic
    pass

def generate_battle_wrapper(user_code, metadata):
    # Battle-specific logic (DUPLICATE CODE!)
    pass
```

✅ **Good Design (Mode-Agnostic):**
```python
def generate_wrapper(user_code, metadata):
    # Single source of truth
    # Works for ALL modes
    pass

# Practice mode calls:
practice_code = generate_wrapper(user_code, metadata)
# → Sends to Judge0 for test cases
# → Shows detailed results

# Battle mode calls:
battle_code = generate_wrapper(user_code, metadata)
# → Sends to Judge0 for evaluation
# → Updates leaderboard based on result
```

**Benefits:**
- ✅ No code duplication
- ✅ Single point of maintenance
- ✅ Easy to add new modes (Contest, Tutorial, etc.)
- ✅ Consistent behavior across all modes

---

## 📂 File Structure

```
/app/xxx/Game/backend/
├── code_wrapper.py           # Main wrapper generator
├── problem_templates.py      # Helper utilities
├── test_wrapper.py           # Test/demo script
└── server.py                 # FastAPI endpoints (updated)
```

---

## 🔧 Components

### 1. **code_wrapper.py** - Main Wrapper Generator

**Purpose:** Convert user function code into full compilable C++ program

**Main Function:**
```python
def generate_wrapper(
    user_code: str,
    problem_metadata: Dict[str, Any],
    language: str = "cpp"
) -> Dict[str, Any]:
    """
    Returns:
    {
        "success": True/False,
        "wrappedCode": "full C++ program",
        "error": "error message if failed"
    }
    """
```

**Process:**
1. Extract metadata (function name, parameters, return type)
2. Generate C++ headers
3. Create helper functions (parsers/formatters)
4. Build Solution class with user code
5. Generate main() function with I/O handling
6. Return complete compilable program

---

### 2. **problem_templates.py** - Helper Utilities

**Purpose:** Provide C++ code generation utilities

**Key Components:**

#### Input Parsers:
- `parseInt()` - Parse integer from stdin
- `parseString()` - Parse string (removes quotes)
- `parseIntArray()` - Parse `[1,2,3]` → `vector<int>`
- `parseStringArray()` - Parse `["hello","world"]` → `vector<string>`

#### Output Formatters:
- `printInt()` - Print integer
- `printString()` - Print string
- `printBool()` - Print `true`/`false`
- `printIntArray()` - Print `[1,2,3]`
- `printStringArray()` - Print `["hello","world"]`

---

### 3. **API Endpoints** (server.py)

#### **POST /api/code/generate-wrapper**

Generate full C++ program from user code.

**Request:**
```json
{
  "userCode": "vector<int> result;\nreturn result;",
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
}
```

**Response:**
```json
{
  "success": true,
  "wrappedCode": "/* Full C++ program */",
  "language": "cpp",
  "message": "Wrapper generated successfully"
}
```

#### **POST /api/code/test-wrapper**

Test endpoint that fetches metadata from MongoDB.

**Request:**
```json
{
  "userCode": "vector<int> result;\nreturn result;",
  "problemId": "two-sum"
}
```

**Response:**
```json
{
  "success": true,
  "wrappedCode": "/* Full C++ program */",
  "problemId": "two-sum",
  "problemTitle": "Two Sum",
  "metadata": { /* problem metadata */ }
}
```

---

## 📊 Problem Metadata Format

**Stored in MongoDB `problems` collection:**

```javascript
{
  "problem_id": "two-sum",
  "title": "Two Sum",
  "description": "Find two numbers that add up to target",
  "difficulty": "Easy",
  "category": "Arrays",
  
  // Wrapper generation metadata
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

### **Supported Input/Output Formats:**

| Format | Description | Example Input | C++ Type |
|--------|-------------|---------------|----------|
| `int` | Integer | `42` | `int` |
| `string` | String | `"hello"` or `hello` | `string` |
| `bool` | Boolean | `true` / `false` | `bool` |
| `array_int` | Integer array | `[1,2,3]` | `vector<int>` |
| `array_string` | String array | `["a","b"]` | `vector<string>` |

---

## 🎯 Example: Two Sum Problem

### **User Code (in Monaco Editor):**
```cpp
// USER CODE START
vector<int> result;
for (int i = 0; i < nums.size(); i++) {
    for (int j = i + 1; j < nums.size(); j++) {
        if (nums[i] + nums[j] == target) {
            result.push_back(i);
            result.push_back(j);
            return result;
        }
    }
}
return result;
// USER CODE END
```

### **Generated Full Program:**
```cpp
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

// Parse integer array from string like "[1,2,3]"
vector<int> parseIntArray(const string& s) {
    vector<int> result;
    string clean = s;
    if (!clean.empty() && clean.front() == '[') clean = clean.substr(1);
    if (!clean.empty() && clean.back() == ']') clean.pop_back();
    if (clean.empty()) return result;
    
    stringstream ss(clean);
    string item;
    while (getline(ss, item, ',')) {
        item.erase(0, item.find_first_not_of(" \t\n\r"));
        item.erase(item.find_last_not_of(" \t\n\r") + 1);
        if (!item.empty()) {
            result.push_back(stoi(item));
        }
    }
    return result;
}

// Parse integer from string
int parseInt(const string& s) {
    return stoi(s);
}

// Print integer array in format [1,2,3]
void printIntArray(const vector<int>& arr) {
    cout << "[";
    for (size_t i = 0; i < arr.size(); i++) {
        cout << arr[i];
        if (i < arr.size() - 1) cout << ",";
    }
    cout << "]" << endl;
}

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        vector<int> result;
        for (int i = 0; i < nums.size(); i++) {
            for (int j = i + 1; j < nums.size(); j++) {
                if (nums[i] + nums[j] == target) {
                    result.push_back(i);
                    result.push_back(j);
                    return result;
                }
            }
        }
        return result;
    }
};

int main() {
    // Read input 1: nums
    string line1;
    getline(cin, line1);
    vector<int> nums = parseIntArray(line1);

    // Read input 2: target
    string line2;
    getline(cin, line2);
    int target = parseInt(line2);

    Solution solution;
    vector<int> result = solution.twoSum(nums, target);
    
    // Print output
    printIntArray(result);
    
    return 0;
}
```

### **Execution:**
```bash
# Input (stdin):
[2,7,11,15]
9

# Output (stdout):
[0,1]
```

---

## 🔄 How Practice and Battle Use It

### **Practice Mode Flow:**

```python
# Frontend extracts user code
user_code = extract_code_from_editor()

# Frontend calls API
response = fetch('/api/code/generate-wrapper', {
    userCode: user_code,
    problemMetadata: problem.metadata
})

# Backend generates wrapper
wrapped_code = generate_wrapper(user_code, metadata)

# Frontend sends to Judge0
judge_result = judge0.execute(wrapped_code, test_cases)

# Show results to user
display_test_results(judge_result)
```

### **Battle Mode Flow:**

```python
# Frontend extracts user code
user_code = extract_code_from_editor()

# Frontend calls SAME API
response = fetch('/api/code/generate-wrapper', {
    userCode: user_code,
    problemMetadata: problem.metadata
})

# Backend generates wrapper (SAME FUNCTION)
wrapped_code = generate_wrapper(user_code, metadata)

# Frontend sends to Judge0
judge_result = judge0.execute(wrapped_code, hidden_test_cases)

# Update battle results
if (judge_result.all_passed) {
    declare_winner(current_user)
}
```

**Key Difference:**
- **Practice:** Shows detailed feedback, allows retry
- **Battle:** Only shows pass/fail, tracks time, updates rankings

**Wrapper Generator:** Completely unaware of these differences! ✅

---

## 🚀 Scalability

### **Adding New Languages (Future):**

```python
# code_wrapper.py

def generate_wrapper(user_code, metadata, language):
    if language == "cpp":
        return generate_cpp_wrapper(user_code, metadata)
    elif language == "python":
        return generate_python_wrapper(user_code, metadata)
    elif language == "java":
        return generate_java_wrapper(user_code, metadata)
```

### **Adding New Data Types:**

```python
# problem_templates.py

@staticmethod
def generate_parse_2d_array_function():
    """Parse 2D array like [[1,2],[3,4]]"""
    return """
vector<vector<int>> parse2DArray(const string& s) {
    // Implementation
}
"""
```

---

## ✅ Testing

Run the test script:

```bash
cd /app/xxx/Game/backend
python test_wrapper.py
```

**Output:**
- ✅ Test 1: Two Sum Problem
- ✅ Test 2: Valid Parentheses
- ✅ Test 3: Reverse String Array
- ✅ Mode-Agnostic Demonstration

---

## 📝 Summary

### **What We Built:**
1. ✅ Mode-agnostic wrapper generator (`code_wrapper.py`)
2. ✅ Helper utilities for I/O (`problem_templates.py`)
3. ✅ API endpoints for both modes (`server.py`)
4. ✅ Test script demonstrating usage (`test_wrapper.py`)

### **Why This Design:**
- 🎯 **Single Source of Truth:** One function for all modes
- 🔧 **Maintainable:** Easy to update and extend
- 📈 **Scalable:** Add languages/types without rewriting
- 🛡️ **Consistent:** Same behavior everywhere

### **Next Steps:**
1. Store problem metadata in MongoDB
2. Frontend integration (call API endpoints)
3. Judge0 integration (execute generated code)
4. Add more languages (Python, Java, etc.)

---

## 🎓 Key Takeaway

**The wrapper generator is a PURE FUNCTION:**
```
f(user_code, metadata) = full_program
```

It doesn't care about:
- ❌ Practice vs Battle
- ❌ User rankings
- ❌ Time limits
- ❌ Database operations

It ONLY cares about:
- ✅ Converting user function → full program
- ✅ Handling I/O correctly
- ✅ Generating compilable code

This separation of concerns makes the system **hackathon-safe** and **production-ready**! 🚀
