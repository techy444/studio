# Example Test Cases - Complete Examples

This file shows 2 complete examples with detailed explanation of test case design.

---

## Example 1: Two Sum Problem

### Problem Statement
Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.

### Function Signature
```javascript
function twoSum(nums, target) {
  // Write your code here
}
```

### Sample Test Cases (Visible to Users - For RUN Button)

#### Test Case 1: Basic Happy Path
```json
{
  "input": "[2,7,11,15], 9",
  "expectedOutput": "[0,1]"
}
```
**Why this test case?**
- Simple, easy to understand
- Shows basic functionality
- Answer is at the beginning of array
- Matches the problem example

#### Test Case 2: Answer in Middle
```json
{
  "input": "[3,2,4], 6",
  "expectedOutput": "[1,2]"
}
```
**Why this test case?**
- Shows answer isn't always at the start
- Small array size for easy verification
- Tests different positions

### Hidden Test Cases (Server-side Only - For SUBMIT Button)

#### Hidden Test Case 1: Duplicate Numbers
```json
{
  "input": "[3,3], 6",
  "expectedOutput": "[0,1]"
}
```
**Edge case covered**: Same number twice, both needed for solution

#### Hidden Test Case 2: Larger Array
```json
{
  "input": "[1,5,3,7,8,9], 12",
  "expectedOutput": "[2,4]"
}
```
**Edge case covered**: Answer in middle of larger array (3 + 8 = 12)

#### Hidden Test Case 3: Negative Numbers
```json
{
  "input": "[-1,-2,-3,-4,-5], -8",
  "expectedOutput": "[2,4]"
}
```
**Edge case covered**: Negative integers (-3 + -5 = -8)

#### Hidden Test Case 4: With Zeros
```json
{
  "input": "[0,4,3,0], 0",
  "expectedOutput": "[0,3]"
}
```
**Edge case covered**: Zero as input and target (0 + 0 = 0)

#### Hidden Test Case 5: Minimum Size
```json
{
  "input": "[1,2], 3",
  "expectedOutput": "[0,1]"
}
```
**Edge case covered**: Smallest valid array (exactly 2 elements)

### Coverage Analysis

| Category | Covered | Test Case |
|----------|---------|-----------|
| Basic functionality | ✅ | Sample 1, 2 |
| Duplicate numbers | ✅ | Hidden 1 |
| Negative numbers | ✅ | Hidden 3 |
| Zero values | ✅ | Hidden 4 |
| Minimum array size | ✅ | Hidden 5 |
| Larger arrays | ✅ | Hidden 2 |

---

## Example 2: Climbing Stairs Problem

### Problem Statement
You are climbing a staircase. It takes `n` steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

### Function Signature
```javascript
function climbStairs(n) {
  // Write your code here
}
```

### Mathematical Background
This is a Fibonacci sequence problem:
- f(1) = 1 (one way: 1 step)
- f(2) = 2 (two ways: 1+1 or 2)
- f(n) = f(n-1) + f(n-2)

Sequence: 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144...

### Sample Test Cases (Visible to Users - For RUN Button)

#### Test Case 1: Base Case (n=2)
```json
{
  "input": "2",
  "expectedOutput": "2"
}
```
**Why this test case?**
- Shows base case scenario
- Easy to manually verify (1+1 or 2)
- Matches problem example

#### Test Case 2: Small Case (n=3)
```json
{
  "input": "3",
  "expectedOutput": "3"
}
```
**Why this test case?**
- Small enough to manually verify (1+1+1, 1+2, 2+1)
- Shows recursive nature
- From problem examples

### Hidden Test Cases (Server-side Only - For SUBMIT Button)

#### Hidden Test Case 1: Minimum Input
```json
{
  "input": "1",
  "expectedOutput": "1"
}
```
**Edge case covered**: Smallest valid input (only one way: take 1 step)

#### Hidden Test Case 2: Medium Input
```json
{
  "input": "5",
  "expectedOutput": "8"
}
```
**Edge case covered**: Tests algorithm beyond examples (5th Fibonacci number)

#### Hidden Test Case 3: Larger Input
```json
{
  "input": "10",
  "expectedOutput": "89"
}
```
**Edge case covered**: Tests efficiency (10th Fibonacci number = 89)

#### Hidden Test Case 4: Even Larger Input
```json
{
  "input": "20",
  "expectedOutput": "10946"
}
```
**Edge case covered**: Tests for overflow/performance (20th Fibonacci = 10,946)

### Coverage Analysis

| Category | Covered | Test Case |
|----------|---------|-----------|
| Base cases (1, 2) | ✅ | Sample 1, Hidden 1 |
| Small numbers (3-5) | ✅ | Sample 2, Hidden 2 |
| Medium numbers (6-15) | ✅ | Hidden 3 |
| Large numbers (16+) | ✅ | Hidden 4 |
| Algorithm correctness | ✅ | All tests |
| Performance | ✅ | Hidden 3, 4 |

### Fibonacci Verification Table

| n | Ways | Calculation |
|---|------|-------------|
| 1 | 1 | Base case |
| 2 | 2 | Base case |
| 3 | 3 | f(2) + f(1) = 2 + 1 |
| 5 | 8 | f(4) + f(3) = 5 + 3 |
| 10 | 89 | ... |
| 20 | 10946 | ... |

---

## Test Case Design Principles (Demonstrated)

### 1. Sample Test Cases Should:
✅ Be from problem examples when possible
✅ Be simple enough to manually verify
✅ Demonstrate basic functionality
✅ Cover different scenarios within simplicity
✅ Help users understand the problem

### 2. Hidden Test Cases Should:
✅ Test edge cases thoroughly
✅ Verify boundary conditions
✅ Test algorithm correctness
✅ Include larger/complex inputs
✅ Cover special values (0, 1, -1, negatives)
✅ Not be guessable from sample tests alone

### 3. Input Progression Strategy:

**Sample Tests**: Easy → Medium Easy
**Hidden Tests**: Minimum → Medium → Large → Edge Cases

Example for Two Sum:
```
Sample:   [2,7,11,15] → [3,2,4]
Hidden:   [3,3] → [1,5,3,7,8,9] → [-1,-2,-3,-4,-5] → [0,4,3,0] → [1,2]
          (dup)   (larger)        (negative)         (zeros)    (minimum)
```

### 4. Output Verification:

All test cases are designed so outputs can be verified:
- **Deterministic**: Same input always gives same output
- **Verifiable**: Outputs can be computed independently
- **Correct**: All expected outputs are mathematically/logically correct

---

## How These Examples Integrate with Your System

### Frontend (RUN Button) - User sees:
```javascript
// API Response for RUN
{
  "status": "success",
  "testResults": [
    {
      "input": "[2,7,11,15], 9",
      "expectedOutput": "[0,1]",
      "actualOutput": "[0,1]",
      "passed": true,
      "message": "✓ Test passed"
    },
    {
      "input": "[3,2,4], 6",
      "expectedOutput": "[1,2]",
      "actualOutput": "[1,2]",
      "passed": true,
      "message": "✓ Test passed"
    }
  ],
  "allPassed": true
}
```

### Backend (SUBMIT Button) - User sees verdict only:
```javascript
// API Response for SUBMIT
{
  "status": "success",
  "verdict": "ACCEPTED",
  "testsPassed": 5,
  "totalTests": 5,
  "successRate": 100,
  "message": "All test cases passed! 🎉"
}
```

**Important**: Users do NOT see the actual hidden test cases, only the count and verdict.

---

## Complete MongoDB Document Example

```json
{
  "_id": ObjectId("..."),
  "problem_id": "two-sum",
  "title": "Two Sum",
  "description": "Given an array of integers nums and an integer target...",
  "difficulty": "Easy",
  "category": "Arrays",
  "examples": [
    {
      "input": "nums = [2,7,11,15], target = 9",
      "output": "[0,1]",
      "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."
    }
  ],
  "sampleTestCases": [
    {
      "input": "[2,7,11,15], 9",
      "expectedOutput": "[0,1]"
    },
    {
      "input": "[3,2,4], 6",
      "expectedOutput": "[1,2]"
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
    },
    {
      "input": "[-1,-2,-3,-4,-5], -8",
      "expectedOutput": "[2,4]"
    },
    {
      "input": "[0,4,3,0], 0",
      "expectedOutput": "[0,3]"
    },
    {
      "input": "[1,2], 3",
      "expectedOutput": "[0,1]"
    }
  ],
  "defaultCode": "function twoSum(nums, target) {\n  // Write your code here\n};"
}
```

---

## Summary

These examples demonstrate:
✅ Clear separation between sample (visible) and hidden test cases
✅ Comprehensive edge case coverage
✅ Progressive difficulty in test cases
✅ Deterministic and verifiable outputs
✅ MongoDB-ready structure
✅ Integration-ready format

All 16 problems follow this same pattern and quality standard!
