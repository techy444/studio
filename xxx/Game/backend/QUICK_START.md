# Quick Start Guide - Test Cases

## 🚀 Quick Start (3 Steps)

### Step 1: Update Database
```bash
cd /app/xxx/Game/backend
python problem_test_cases.py
```

### Step 2: Verify Update
```python
from database import problems_collection

# Check any problem
problem = problems_collection.find_one({"problem_id": "two-sum"})
print(f"Sample tests: {len(problem['sampleTestCases'])}")
print(f"Hidden tests: {len(problem['hiddenTestCases'])}")
```

### Step 3: Integrate with API
See `TEST_CASES_DOCUMENTATION.md` for integration code examples.

---

## 📁 Files Overview

| File | Purpose | When to Use |
|------|---------|-------------|
| `problem_test_cases.py` | **Main file** - Contains all test cases + update script | Run this to populate database |
| `TEST_CASES_DOCUMENTATION.md` | **Complete docs** - Structure, usage, integration | Read for full understanding |
| `TEST_CASES_SUMMARY.md` | **Overview** - Stats, coverage, next steps | Quick reference of what's included |
| `test_case_template.py` | **Template** - Schema and guidelines | Use when adding new problems |
| `EXAMPLE_TEST_CASES.md` | **Examples** - 2 complete examples with explanations | See detailed test case design |

---

## 📊 What You Got

✅ **16 problems** with test cases (20 total - 4 excluded as requested)
✅ **91 test cases** total (24 sample + 67 hidden)
✅ **Comprehensive edge case coverage**
✅ **MongoDB-ready format**
✅ **Battle Mode compatible** (deterministic)

---

## 🎯 Test Case Types

### Sample Test Cases (RUN Button)
- 1-2 per problem
- ✅ Visible to users
- Used for debugging
- Simple and clear

### Hidden Test Cases (SUBMIT Button)
- 3-5 per problem
- ❌ NOT visible to users
- Used for grading
- Comprehensive edge cases

---

## 💡 Key Points

1. **Sample tests are visible** - Users can see input and expected output
2. **Hidden tests are secret** - Only verdict (pass/fail count) is shown
3. **All original** - Not scraped from any platform
4. **Deterministic** - No randomness, consistent results
5. **Ready to use** - Just run the update script

---

## 🔍 Problems Covered

### ✅ Included (16)
- Two Sum, Reverse String, Valid Parentheses
- Merge Sorted Array, Maximum Subarray
- Longest Substring, Container With Most Water
- Reverse Linked List, Linked List Cycle
- Climbing Stairs, House Robber, Coin Change
- Palindrome Number, Fizz Buzz
- Search in Rotated Array, Trapping Rain Water

### ❌ Excluded (4)
- Binary Tree Inorder (tree)
- Number of Islands (graph)
- Course Schedule (graph)
- Word Ladder (graph)

---

## 🔗 Integration Example

### RUN Button API
```python
@app.post("/api/run")
def run_code(problem_id, user_code):
    problem = get_problem(problem_id)
    
    # Use sampleTestCases (visible)
    for test in problem["sampleTestCases"]:
        result = execute(user_code, test["input"])
        # Return result with input/output visible
```

### SUBMIT Button API
```python
@app.post("/api/submit")
def submit_code(problem_id, user_code):
    problem = get_problem(problem_id)
    passed = 0
    
    # Use hiddenTestCases (NOT visible)
    for test in problem["hiddenTestCases"]:
        result = execute(user_code, test["input"])
        if result == test["expectedOutput"]:
            passed += 1
    
    # Return verdict only (not test details)
    return {
        "verdict": "ACCEPTED" if passed == total else "WRONG ANSWER",
        "testsPassed": passed,
        "totalTests": total
    }
```

---

## 📖 Read Next

1. **Getting Started**: Run `python problem_test_cases.py`
2. **Full Documentation**: Read `TEST_CASES_DOCUMENTATION.md`
3. **See Examples**: Check `EXAMPLE_TEST_CASES.md`
4. **Add New Problems**: Use `test_case_template.py`

---

## ❓ Common Questions

**Q: Can users see hidden test cases?**
A: No! Only send `sampleTestCases` to frontend. Keep `hiddenTestCases` server-side only.

**Q: How do I add a new problem?**
A: Use the template in `test_case_template.py` and follow the guidelines.

**Q: Are test cases sufficient for demo?**
A: Yes! They're minimal but comprehensive, perfect for MVP/demo.

**Q: Can I modify test cases?**
A: Yes! Edit `problem_test_cases.py` and re-run the update script.

**Q: What about tree/graph problems?**
A: Excluded as requested. Add them later when you support those structures.

---

## 🎉 You're Ready!

Everything is set up. Just run the update script and integrate with your API!

```bash
cd /app/xxx/Game/backend
python problem_test_cases.py
```
