"""
Reusable Template and Schema for Test Cases

This file provides templates and schemas for adding new problems
with test cases to the coding platform.
"""

# ============================================
# MONGODB SCHEMA
# ============================================

PROBLEM_SCHEMA = {
    "problem_id": "string (unique, kebab-case)",
    "title": "string",
    "description": "string (full problem description)",
    "difficulty": "string (Easy|Medium|Hard)",
    "category": "string (Arrays|Strings|Dynamic Programming|Math|Linked List)",
    "examples": [
        {
            "input": "string (human-readable input example)",
            "output": "string (human-readable output example)",
            "explanation": "string (optional)"
        }
    ],
    "sampleTestCases": [
        {
            "input": "string (input parameters)",
            "expectedOutput": "string (expected output)"
        }
    ],
    "hiddenTestCases": [
        {
            "input": "string (input parameters)",
            "expectedOutput": "string (expected output)"
        }
    ],
    "defaultCode": "string (starter code template)"
}

# ============================================
# TEMPLATE FOR NEW PROBLEM
# ============================================

NEW_PROBLEM_TEMPLATE = {
    "problem_id": "problem-name",
    "title": "Problem Title",
    "description": "Detailed problem description with constraints and requirements.",
    "difficulty": "Easy",  # or Medium, Hard
    "category": "Arrays",  # or Strings, Dynamic Programming, Math, etc.
    "examples": [
        {
            "input": "nums = [1,2,3]",
            "output": "6",
            "explanation": "1 + 2 + 3 = 6"
        }
    ],
    "sampleTestCases": [
        # 1-2 simple test cases for RUN button
        {
            "input": "[1,2,3]",
            "expectedOutput": "6"
        },
        {
            "input": "[5,5]",
            "expectedOutput": "10"
        }
    ],
    "hiddenTestCases": [
        # 3-5 comprehensive test cases for SUBMIT button
        {
            "input": "[]",
            "expectedOutput": "0"
        },
        {
            "input": "[1]",
            "expectedOutput": "1"
        },
        {
            "input": "[-1,-2,-3]",
            "expectedOutput": "-6"
        },
        {
            "input": "[0,0,0,0]",
            "expectedOutput": "0"
        },
        {
            "input": "[1,2,3,4,5,6,7,8,9,10]",
            "expectedOutput": "55"
        }
    ],
    "defaultCode": "function sumArray(nums) {\n  // Write your code here\n};"
}

# ============================================
# TEST CASE GENERATION GUIDELINES
# ============================================

TEST_CASE_GUIDELINES = {
    "sampleTestCases": {
        "count": "1-2 per problem",
        "purpose": "Debugging and understanding the problem",
        "visibility": "Visible to users",
        "characteristics": [
            "Simple and easy to understand",
            "Demonstrates basic functionality",
            "Uses small input sizes",
            "Happy path scenarios"
        ],
        "examples": [
            "Basic input with expected output",
            "Simple edge case (if relevant)"
        ]
    },
    "hiddenTestCases": {
        "count": "3-5 per problem",
        "purpose": "Comprehensive grading and validation",
        "visibility": "Hidden from users (server-side only)",
        "characteristics": [
            "Cover edge cases thoroughly",
            "Test boundary conditions",
            "Include larger inputs",
            "Test special values (0, negatives, max/min)",
            "Verify algorithm correctness"
        ],
        "examples": [
            "Empty input",
            "Single element",
            "All same elements",
            "Negative numbers",
            "Large input size",
            "Special mathematical cases (0, 1, -1)"
        ]
    }
}

# ============================================
# EDGE CASE CHECKLIST BY DATA TYPE
# ============================================

EDGE_CASES_BY_TYPE = {
    "Arrays (integers)": [
        "Empty array: []",
        "Single element: [1]",
        "Two elements: [1, 2]",
        "All same: [5, 5, 5, 5]",
        "All negative: [-1, -2, -3]",
        "With zeros: [0, 1, 0, 2]",
        "Large array: [1,2,3,...,100]",
        "Sorted ascending: [1,2,3,4,5]",
        "Sorted descending: [5,4,3,2,1]"
    ],
    "Strings": [
        "Empty string: ''",
        "Single character: 'a'",
        "Two characters: 'ab'",
        "All same: 'aaaa'",
        "With spaces: 'hello world'",
        "Long string: 'abcd...xyz' (26+ chars)",
        "Special characters: '!@#$%'"
    ],
    "Integers": [
        "Zero: 0",
        "One: 1",
        "Negative: -1, -100",
        "Large positive: 1000, 10000",
        "Large negative: -1000, -10000"
    ],
    "Boolean outputs": [
        "True case",
        "False case",
        "Edge true case",
        "Edge false case"
    ]
}

# ============================================
# EXAMPLE: COMPREHENSIVE TEST CASE CREATION
# ============================================

def create_test_cases_example():
    """
    Example function showing how to create comprehensive test cases
    for a 'Find Maximum' problem
    """
    
    problem = {
        "problem_id": "find-maximum",
        "title": "Find Maximum",
        "description": "Given an array of integers, return the maximum value.",
        "difficulty": "Easy",
        "category": "Arrays",
        
        # Sample test cases - visible to users
        "sampleTestCases": [
            {
                "input": "[1,2,3,4,5]",
                "expectedOutput": "5"
            },
            {
                "input": "[-1,-2,-3]",
                "expectedOutput": "-1"
            }
        ],
        
        # Hidden test cases - for grading only
        "hiddenTestCases": [
            # Edge case: Single element
            {
                "input": "[42]",
                "expectedOutput": "42"
            },
            # Edge case: Two elements
            {
                "input": "[1,2]",
                "expectedOutput": "2"
            },
            # Edge case: All same
            {
                "input": "[5,5,5,5]",
                "expectedOutput": "5"
            },
            # Edge case: Zero included
            {
                "input": "[0,-1,5,3]",
                "expectedOutput": "5"
            },
            # Edge case: Large array
            {
                "input": "[10,20,30,40,50,60,70,80,90,100]",
                "expectedOutput": "100"
            }
        ],
        
        "defaultCode": "function findMax(nums) {\n  // Write your code here\n};"
    }
    
    return problem

# ============================================
# VALIDATION RULES
# ============================================

VALIDATION_RULES = {
    "input_format": {
        "rule": "Must be a string representation of the input",
        "examples": {
            "single_int": "5",
            "array": "[1,2,3]",
            "string": "'hello'",
            "multiple_params": "[1,2,3], 5",
            "array_of_strings": "['a','b','c']"
        }
    },
    "output_format": {
        "rule": "Must be a string representation of the expected output",
        "examples": {
            "int": "42",
            "boolean": "true",
            "array": "[1,2,3]",
            "string": "'result'"
        }
    },
    "test_case_count": {
        "sampleTestCases": "1-2 cases",
        "hiddenTestCases": "3-5 cases"
    },
    "deterministic": {
        "rule": "All test cases must be deterministic",
        "note": "No random values, no timestamps, same input always produces same output"
    }
}

# ============================================
# USAGE EXAMPLE
# ============================================

def usage_example():
    """
    Example showing how to add a new problem with test cases
    """
    from database import problems_collection
    
    new_problem = {
        "problem_id": "sum-array",
        "title": "Sum Array",
        "description": "Given an array of integers, return the sum of all elements.",
        "difficulty": "Easy",
        "category": "Arrays",
        "examples": [
            {
                "input": "nums = [1,2,3]",
                "output": "6"
            }
        ],
        "sampleTestCases": [
            {"input": "[1,2,3]", "expectedOutput": "6"},
            {"input": "[5,5]", "expectedOutput": "10"}
        ],
        "hiddenTestCases": [
            {"input": "[]", "expectedOutput": "0"},
            {"input": "[0]", "expectedOutput": "0"},
            {"input": "[-1,-2,-3]", "expectedOutput": "-6"},
            {"input": "[1,2,3,4,5]", "expectedOutput": "15"}
        ],
        "defaultCode": "function sumArray(nums) {\n  // Write your code here\n};"
    }
    
    # Insert into database
    result = problems_collection.insert_one(new_problem)
    print(f"Inserted problem with ID: {result.inserted_id}")

# ============================================
# EXPORT
# ============================================

__all__ = [
    'PROBLEM_SCHEMA',
    'NEW_PROBLEM_TEMPLATE',
    'TEST_CASE_GUIDELINES',
    'EDGE_CASES_BY_TYPE',
    'VALIDATION_RULES',
    'create_test_cases_example',
    'usage_example'
]
