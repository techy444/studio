# Test Cases Documentation

## Overview
This document explains the test case structure for the coding platform's DSA problems.

## Test Case Structure

Each problem now has two types of test cases:

### 1. Sample Test Cases (sampleTestCases)
- **Purpose**: Used for the RUN button (debugging)
- **Visibility**: Visible to users
- **Count**: 1-2 per problem
- **Characteristics**: Simple, easy-to-understand cases that demonstrate basic functionality

### 2. Hidden Test Cases (hiddenTestCases)
- **Purpose**: Used for the SUBMIT button (final grading)
- **Visibility**: NOT visible to users
- **Count**: 3-5 per problem
- **Characteristics**: Comprehensive edge cases covering:
  - Boundary conditions (empty arrays, single elements)
  - Edge values (min/max, negatives, zeros)
  - Special cases specific to each problem
  - Larger inputs for performance testing

## MongoDB Schema

Each problem document now includes:

```json
{
  "problem_id": "two-sum",
  "title": "Two Sum",
  "description": "...",
  "difficulty": "Easy",
  "category": "Arrays",
  "examples": [...],
  "defaultCode": "...",
  "sampleTestCases": [
    {
      "input": "[2,7,11,15], 9",
      "expectedOutput": "[0,1]"
    }
  ],
  "hiddenTestCases": [
    {
      "input": "[3,3], 6",
      "expectedOutput": "[0,1]"
    },
    {
      "input": "[1,5,3,7,8,9], 12",
      "expectedOutput": "[2,4]"
    }
  ]
}
```

## Test Case Coverage

### Problems Included (16 problems)
1. **Two Sum** - Array with target sum
2. **Reverse String** - In-place string reversal
3. **Valid Parentheses** - Stack-based validation
4. **Merge Sorted Array** - Two-pointer merge
5. **Maximum Subarray** - Kadane's algorithm
6. **Longest Substring** - Sliding window
7. **Container With Most Water** - Two-pointer approach
8. **Reverse Linked List** - Iterative reversal (array representation)
9. **Linked List Cycle** - Cycle detection (array representation)
10. **Climbing Stairs** - Dynamic programming (Fibonacci)
11. **House Robber** - Dynamic programming
12. **Coin Change** - Dynamic programming (unbounded knapsack)
13. **Palindrome Number** - Mathematical palindrome check
14. **Fizz Buzz** - Classic modulo problem
15. **Search in Rotated Array** - Binary search variant
16. **Trapping Rain Water** - Two-pointer / stack approach

### Problems Excluded (4 problems)
- Binary Tree Inorder Traversal (tree structure)
- Number of Islands (graph/grid structure)
- Course Schedule (graph structure)
- Word Ladder (graph structure)

## Input/Output Format Support

The test cases support the following data types:

### Integers
```json
{
  "input": "121",
  "expectedOutput": "true"
}
```

### Strings
```json
{
  "input": "'hello'",
  "expectedOutput": "'olleh'"
}
```

### 1D Arrays (integers)
```json
{
  "input": "[1,2,3,4,5]",
  "expectedOutput": "[5,4,3,2,1]"
}
```

### 1D Arrays (strings)
```json
{
  "input": "['h','e','l','l','o']",
  "expectedOutput": "['o','l','l','e','h']"
}
```

### Multiple Parameters
```json
{
  "input": "[1,2,5], 11",
  "expectedOutput": "3"
}
```

## Usage

### Step 1: Update Database
Run the test cases script to populate the database:

```bash
cd /app/xxx/Game/backend
python problem_test_cases.py
```

This will update all 16 problems with sampleTestCases and hiddenTestCases.

### Step 2: Integration with Verdict Logic

#### For RUN Button (Sample Test Cases)
```python
# Fetch sample test cases
problem = problems_collection.find_one({"problem_id": problem_id})
sample_tests = problem.get("sampleTestCases", [])

# Execute user code against sample tests
for test in sample_tests:
    result = execute_code(user_code, test["input"])
    if result == test["expectedOutput"]:
        print("✓ Test passed")
    else:
        print(f"✗ Test failed. Expected: {test['expectedOutput']}, Got: {result}")
```

#### For SUBMIT Button (Hidden Test Cases)
```python
# Fetch hidden test cases (DO NOT send to frontend)
problem = problems_collection.find_one({"problem_id": problem_id})
hidden_tests = problem.get("hiddenTestCases", [])

# Execute user code against all hidden tests
passed = 0
total = len(hidden_tests)

for test in hidden_tests:
    result = execute_code(user_code, test["input"])
    if result == test["expectedOutput"]:
        passed += 1

# Return verdict
success_rate = (passed / total) * 100
if passed == total:
    verdict = "ACCEPTED"
else:
    verdict = f"WRONG ANSWER ({passed}/{total} test cases passed)"
```

### Step 3: API Response Structure

#### RUN Button Response
```json
{
  "status": "success",
  "testResults": [
    {
      "input": "[2,7,11,15], 9",
      "expectedOutput": "[0,1]",
      "actualOutput": "[0,1]",
      "passed": true
    }
  ],
  "allPassed": true
}
```

#### SUBMIT Button Response
```json
{
  "status": "success",
  "verdict": "ACCEPTED",
  "testsPassed": 5,
  "totalTests": 5,
  "successRate": 100
}
```

Or for failures:
```json
{
  "status": "failed",
  "verdict": "WRONG ANSWER",
  "testsPassed": 3,
  "totalTests": 5,
  "successRate": 60,
  "message": "3 out of 5 test cases passed"
}
```

## Battle Mode Considerations

For Battle Mode (real-time competitions):

1. **Same Test Cases**: Use the same hiddenTestCases for consistency
2. **Deterministic**: All test cases are deterministic (no randomness)
3. **Fair Competition**: All participants get the same test cases
4. **Real-time Grading**: Execute hiddenTestCases immediately on submission

Example Battle Mode Flow:
```python
# When user submits in battle mode
battle_result = {
    "user_id": user_id,
    "problem_id": problem_id,
    "submission_time": timestamp,
    "tests_passed": passed,
    "total_tests": total,
    "execution_time": execution_time_ms,
    "verdict": verdict
}
```

## Edge Case Coverage Examples

### Two Sum
- Same numbers: `[3,3], 6`
- Negative numbers: `[-1,-2,-3,-4,-5], -8`
- With zeros: `[0,4,3,0], 0`

### Valid Parentheses
- Empty string: `''` → true
- Only opening: `'((((((('` → false
- Mixed valid: `'{[]}'` → true

### Maximum Subarray
- All negative: `[-5,-4,-3,-2,-1]` → `-1`
- All positive: `[1,2,3,4,5]` → `15`
- Single element: `[-1]` → `-1`

### Climbing Stairs
- Base cases: `1` → `1`, `2` → `2`
- Larger values: `20` → `10946` (Fibonacci growth)

## Next Steps

1. ✅ Test cases are created and ready to use
2. ⏭️ Integrate with your code execution engine (Judge0)
3. ⏭️ Implement verdict logic in your backend API
4. ⏭️ Update frontend to display RUN results
5. ⏭️ Update frontend to show SUBMIT verdict (without exposing hidden tests)

## Important Notes

- **Do NOT send hiddenTestCases to the frontend** - they should remain server-side only
- **sampleTestCases are meant to be visible** - users should see these for debugging
- **All test cases are original** - not scraped from any platform
- **Test cases are minimal but sufficient** - focused on demo and MVP functionality
- **No verdict execution logic included** - you need to implement the code execution and comparison logic
