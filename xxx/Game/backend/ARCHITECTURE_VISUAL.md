# Backend Wrapper Generator - Visual Architecture

## 🎨 System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FRONTEND LAYER                              │
│                                                                     │
│  ┌────────────────────────┐       ┌─────────────────────────┐     │
│  │   Practice Mode        │       │    Battle Mode           │     │
│  │   (/practice/:id)      │       │    (/battle/:id)         │     │
│  │                        │       │                          │     │
│  │ • Monaco Editor        │       │ • Monaco Editor          │     │
│  │ • Test Cases Display   │       │ • Timer + Opponent       │     │
│  │ • Run/Submit Buttons   │       │ • Submit Button          │     │
│  └────────┬───────────────┘       └──────────┬───────────────┘     │
│           │                                  │                      │
│           │   Extract User Code              │                      │
│           │   (between USER CODE markers)    │                      │
│           │                                  │                      │
└───────────┼──────────────────────────────────┼──────────────────────┘
            │                                  │
            │                                  │
            │  POST userCode + metadata        │
            │                                  │
            ▼                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         BACKEND API LAYER                           │
│                                                                     │
│         POST /api/code/generate-wrapper                             │
│         ┌────────────────────────────────────────┐                 │
│         │  Input:                                │                 │
│         │  {                                     │                 │
│         │    userCode: "return nums[0];",        │                 │
│         │    language: "cpp",                    │                 │
│         │    problemMetadata: { ... }            │                 │
│         │  }                                     │                 │
│         └────────────────┬───────────────────────┘                 │
│                          │                                          │
│                          │ Validate & Process                       │
│                          ▼                                          │
│         ┌──────────────────────────────────────┐                   │
│         │    Wrapper Generator Core            │                   │
│         │    (code_wrapper.py)                 │                   │
│         │                                      │                   │
│         │  • Extract metadata                  │                   │
│         │  • Generate headers                  │                   │
│         │  • Build Solution class              │                   │
│         │  • Create main() function            │                   │
│         │  • Add I/O helpers                   │                   │
│         └────────────────┬───────────────────────┘                 │
│                          │                                          │
│                          │ Uses                                     │
│                          ▼                                          │
│         ┌──────────────────────────────────────┐                   │
│         │    Helper Utilities                  │                   │
│         │    (problem_templates.py)            │                   │
│         │                                      │                   │
│         │  • parseInt()                        │                   │
│         │  • parseIntArray()                   │                   │
│         │  • parseStringArray()                │                   │
│         │  • printInt()                        │                   │
│         │  • printIntArray()                   │                   │
│         │  • printStringArray()                │                   │
│         └──────────────────────────────────────┘                   │
│                                                                     │
│         ┌────────────────────────────────────────┐                 │
│         │  Output:                               │                 │
│         │  {                                     │                 │
│         │    success: true,                      │                 │
│         │    wrappedCode: "full C++ program",    │                 │
│         │    language: "cpp"                     │                 │
│         │  }                                     │                 │
│         └────────────────┬───────────────────────┘                 │
└──────────────────────────┼──────────────────────────────────────────┘
                           │
                           │ Full Compilable Program
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         FRONTEND LAYER                              │
│                                                                     │
│  ┌────────────────────────┐       ┌─────────────────────────┐     │
│  │   Practice Mode        │       │    Battle Mode           │     │
│  │                        │       │                          │     │
│  │ → Send to Judge0       │       │ → Send to Judge0         │     │
│  │ → Run test cases       │       │ → Run hidden tests       │     │
│  │ → Show results         │       │ → Update battle status   │     │
│  │ → Allow retry          │       │ → Declare winner         │     │
│  └────────────────────────┘       └─────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Example: Two Sum Problem

### **Step 1: User Writes Code (Frontend)**

```
┌─────────────────────────────────────┐
│  Monaco Editor (Practice/Battle)    │
│                                     │
│  class Solution {                   │
│  public:                            │
│      vector<int> twoSum(...) {      │
│          // USER CODE START         │
│          vector<int> result;        │
│          for(int i=0; i<nums.size();│
│              // logic here          │
│          return result;             │
│          // USER CODE END           │
│      }                              │
│  }                                  │
└─────────────────┬───────────────────┘
                  │
                  │ Extract only user code
                  ▼
        "vector<int> result;\n..."
```

### **Step 2: Send to Backend**

```
POST /api/code/generate-wrapper

{
  "userCode": "vector<int> result;\nfor(int i=0; i<nums.size(); i++)...",
  "language": "cpp",
  "problemMetadata": {
    "functionName": "twoSum",
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

### **Step 3: Backend Processing**

```
┌────────────────────────────────────────┐
│  Wrapper Generator                     │
│                                        │
│  1. Add headers:                       │
│     #include <iostream>                │
│     #include <vector>                  │
│                                        │
│  2. Add helper functions:              │
│     vector<int> parseIntArray(...)     │
│     int parseInt(...)                  │
│     void printIntArray(...)            │
│                                        │
│  3. Create Solution class:             │
│     class Solution {                   │
│     public:                            │
│         vector<int> twoSum(...) {      │
│             /* USER CODE HERE */       │
│         }                              │
│     };                                 │
│                                        │
│  4. Create main():                     │
│     int main() {                       │
│         // Read inputs                 │
│         // Call user function          │
│         // Print output                │
│     }                                  │
└────────────────────────────────────────┘
```

### **Step 4: Return Full Program**

```cpp
#include <iostream>
#include <vector>
#include <sstream>
using namespace std;

vector<int> parseIntArray(const string& s) {
    // Generated parser code
}

int parseInt(const string& s) {
    return stoi(s);
}

void printIntArray(const vector<int>& arr) {
    // Generated printer code
}

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        // USER CODE INJECTED HERE
        vector<int> result;
        for(int i=0; i<nums.size(); i++) {
            // user's logic
        }
        return result;
    }
};

int main() {
    // Read nums
    string line1;
    getline(cin, line1);
    vector<int> nums = parseIntArray(line1);
    
    // Read target
    string line2;
    getline(cin, line2);
    int target = parseInt(line2);
    
    // Execute
    Solution solution;
    vector<int> result = solution.twoSum(nums, target);
    
    // Print result
    printIntArray(result);
    
    return 0;
}
```

### **Step 5: Execute (Judge0)**

```
┌────────────────────────────────────┐
│  Judge0 Execution Engine           │
│                                    │
│  Input (stdin):                    │
│  [2,7,11,15]                       │
│  9                                 │
│                                    │
│  Compile: g++ -o solution code.cpp │
│  Run: ./solution                   │
│                                    │
│  Output (stdout):                  │
│  [0,1]                             │
│                                    │
│  Result: Success ✅                │
└────────────────────────────────────┘
```

---

## 🎯 Mode Comparison

### **Practice Mode Path:**

```
User Code → Wrapper Generator → Full Program → Judge0 (public tests)
                                                     ↓
                                            Pass/Fail Details
                                                     ↓
                                            Show to User
                                                     ↓
                                            Allow Retry ✅
```

### **Battle Mode Path:**

```
User Code → Wrapper Generator → Full Program → Judge0 (hidden tests)
                                                     ↓
                                              All Pass/Fail
                                                     ↓
                                            Update Leaderboard
                                                     ↓
                                             Declare Winner 🏆
```

### **Key Point:**

```
┌─────────────────────────────────────────┐
│   SAME WRAPPER GENERATOR                │
│   Different handling of results         │
│                                         │
│   Practice: Detailed feedback + retry   │
│   Battle: Winner/loser + leaderboard    │
└─────────────────────────────────────────┘
```

---

## 🧩 Component Interaction

```
┌──────────────────────────────────────────────────────────────┐
│                      PROBLEM METADATA                        │
│                                                              │
│  Stored in MongoDB problems collection                      │
│                                                              │
│  {                                                           │
│    problem_id: "two-sum",                                    │
│    title: "Two Sum",                                         │
│    metadata: {                                               │
│      functionName: "twoSum",                                 │
│      parameters: [...],                                      │
│      inputFormat: ["array_int", "int"],                      │
│      outputFormat: "array_int"                               │
│    }                                                         │
│  }                                                           │
└────────────┬─────────────────────────────────────────────────┘
             │
             │ Fetched by Frontend
             │
             ▼
┌──────────────────────────────────────────────────────────────┐
│                      FRONTEND                                │
│                                                              │
│  const problem = await fetchProblem(problemId)               │
│  const metadata = problem.metadata                           │
│                                                              │
│  // User writes code in Monaco                               │
│  const userCode = extractUserCode()                          │
│                                                              │
│  // Call wrapper generator                                   │
│  const result = await generateWrapper(userCode, metadata)    │
└────────────┬─────────────────────────────────────────────────┘
             │
             │ API Call
             │
             ▼
┌──────────────────────────────────────────────────────────────┐
│                      BACKEND API                             │
│                                                              │
│  POST /api/code/generate-wrapper                             │
│  Receives: userCode + metadata                               │
│  Returns: Full C++ program                                   │
└────────────┬─────────────────────────────────────────────────┘
             │
             │ Delegates to
             │
             ▼
┌──────────────────────────────────────────────────────────────┐
│                    WRAPPER GENERATOR                         │
│                                                              │
│  Pure function: (userCode, metadata) → fullProgram           │
│  No database access                                          │
│  No mode awareness                                           │
│  No authentication                                           │
│  Just code transformation                                    │
└──────────────────────────────────────────────────────────────┘
```

---

## 🎨 Code Transformation Visual

### **Input (User Code):**
```
┌─────────────────────────┐
│  return a + b;          │
└─────────────────────────┘
```

### **Metadata:**
```
┌────────────────────────────┐
│ functionName: "add"        │
│ returnType: "int"          │
│ parameters:                │
│   - {name: "a", type: "int"}│
│   - {name: "b", type: "int"}│
│ inputFormat: ["int", "int"]│
│ outputFormat: "int"        │
└────────────────────────────┘
```

### **Output (Full Program):**
```
┌─────────────────────────────────────┐
│ #include <iostream>                 │
│ using namespace std;                │
│                                     │
│ int parseInt(const string& s) {     │
│     return stoi(s);                 │
│ }                                   │
│                                     │
│ void printInt(int value) {          │
│     cout << value << endl;          │
│ }                                   │
│                                     │
│ class Solution {                    │
│ public:                             │
│     int add(int a, int b) {         │
│         return a + b; ← USER CODE   │
│     }                               │
│ };                                  │
│                                     │
│ int main() {                        │
│     string line1;                   │
│     getline(cin, line1);            │
│     int a = parseInt(line1);        │
│                                     │
│     string line2;                   │
│     getline(cin, line2);            │
│     int b = parseInt(line2);        │
│                                     │
│     Solution solution;              │
│     int result = solution.add(a, b);│
│     printInt(result);               │
│     return 0;                       │
│ }                                   │
└─────────────────────────────────────┘
```

---

## 🚀 Scalability Design

### **Current: C++ Only**
```
generate_wrapper(userCode, metadata, language="cpp")
    ↓
generate_cpp_wrapper(userCode, metadata)
```

### **Future: Multi-Language**
```
generate_wrapper(userCode, metadata, language)
    ↓
    ├─ if language == "cpp"  → generate_cpp_wrapper()
    ├─ if language == "python" → generate_python_wrapper()
    ├─ if language == "java" → generate_java_wrapper()
    └─ if language == "javascript" → generate_js_wrapper()
```

### **Adding New Types:**
```
Current Support:
├─ int
├─ string
├─ bool
├─ array_int
└─ array_string

Future:
├─ array_2d_int
├─ linked_list
├─ tree_node
└─ graph
```

---

## ✅ Design Principles Summary

```
┌────────────────────────────────────────────┐
│  1. SEPARATION OF CONCERNS                 │
│     Wrapper = Code Transform Only          │
│     Practice/Battle = Result Handling      │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│  2. MODE-AGNOSTIC                          │
│     One function works for ALL modes       │
│     No duplicated logic                    │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│  3. PURE FUNCTION                          │
│     Input: userCode + metadata             │
│     Output: fullProgram                    │
│     No side effects                        │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│  4. METADATA-DRIVEN                        │
│     Problems define their own requirements │
│     Generator adapts automatically         │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│  5. SCALABLE                               │
│     Easy to add languages                  │
│     Easy to add data types                 │
│     Easy to add modes                      │
└────────────────────────────────────────────┘
```

---

**This architecture is production-ready and hackathon-safe! 🎯**
