"""
Test Cases for Coding Platform Problems
Includes sampleTestCases (for RUN button) and hiddenTestCases (for SUBMIT button)

Structure:
- sampleTestCases: 1-2 simple, visible test cases for debugging
- hiddenTestCases: 3-5 comprehensive test cases covering edge cases
"""

from database import problems_collection

# Test cases for all problems (excluding trees and graphs)
test_cases_data = [
    {
        "problem_id": "two-sum",
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
        ]
    },
    {
        "problem_id": "reverse-string",
        "sampleTestCases": [
            {
                "input": "['h','e','l','l','o']",
                "expectedOutput": "['o','l','l','e','h']"
            }
        ],
        "hiddenTestCases": [
            {
                "input": "['H','a','n','n','a','h']",
                "expectedOutput": "['h','a','n','n','a','H']"
            },
            {
                "input": "['a']",
                "expectedOutput": "['a']"
            },
            {
                "input": "['a','b']",
                "expectedOutput": "['b','a']"
            },
            {
                "input": "['A',' ','m','a','n',',',' ','a',' ','p','l','a','n']",
                "expectedOutput": "['n','a','l','p',' ','a',',',' ','n','a','m',' ','A']"
            }
        ]
    },
    {
        "problem_id": "valid-parentheses",
        "sampleTestCases": [
            {
                "input": "'()'",
                "expectedOutput": "true"
            },
            {
                "input": "'()[]{}'",
                "expectedOutput": "true"
            }
        ],
        "hiddenTestCases": [
            {
                "input": "'(]'",
                "expectedOutput": "false"
            },
            {
                "input": "'([)]'",
                "expectedOutput": "false"
            },
            {
                "input": "'{[]}'",
                "expectedOutput": "true"
            },
            {
                "input": "''",
                "expectedOutput": "true"
            },
            {
                "input": "'((((((('",
                "expectedOutput": "false"
            }
        ]
    },
    {
        "problem_id": "merge-sorted-arrays",
        "sampleTestCases": [
            {
                "input": "[1,2,3,0,0,0], 3, [2,5,6], 3",
                "expectedOutput": "[1,2,2,3,5,6]"
            }
        ],
        "hiddenTestCases": [
            {
                "input": "[1], 1, [], 0",
                "expectedOutput": "[1]"
            },
            {
                "input": "[0], 0, [1], 1",
                "expectedOutput": "[1]"
            },
            {
                "input": "[4,5,6,0,0,0], 3, [1,2,3], 3",
                "expectedOutput": "[1,2,3,4,5,6]"
            },
            {
                "input": "[1,3,5,7,9,0,0,0], 5, [2,4,6], 3",
                "expectedOutput": "[1,2,3,4,5,6,7,9]"
            }
        ]
    },
    {
        "problem_id": "maximum-subarray",
        "sampleTestCases": [
            {
                "input": "[-2,1,-3,4,-1,2,1,-5,4]",
                "expectedOutput": "6"
            },
            {
                "input": "[1]",
                "expectedOutput": "1"
            }
        ],
        "hiddenTestCases": [
            {
                "input": "[5,4,-1,7,8]",
                "expectedOutput": "23"
            },
            {
                "input": "[-1]",
                "expectedOutput": "-1"
            },
            {
                "input": "[-2,-1]",
                "expectedOutput": "-1"
            },
            {
                "input": "[1,2,3,4,5]",
                "expectedOutput": "15"
            },
            {
                "input": "[-5,-4,-3,-2,-1]",
                "expectedOutput": "-1"
            }
        ]
    },
    {
        "problem_id": "longest-substring",
        "sampleTestCases": [
            {
                "input": "'abcabcbb'",
                "expectedOutput": "3"
            },
            {
                "input": "'bbbbb'",
                "expectedOutput": "1"
            }
        ],
        "hiddenTestCases": [
            {
                "input": "'pwwkew'",
                "expectedOutput": "3"
            },
            {
                "input": "''",
                "expectedOutput": "0"
            },
            {
                "input": "' '",
                "expectedOutput": "1"
            },
            {
                "input": "'abcdefg'",
                "expectedOutput": "7"
            },
            {
                "input": "'dvdf'",
                "expectedOutput": "3"
            }
        ]
    },
    {
        "problem_id": "container-with-most-water",
        "sampleTestCases": [
            {
                "input": "[1,8,6,2,5,4,8,3,7]",
                "expectedOutput": "49"
            }
        ],
        "hiddenTestCases": [
            {
                "input": "[1,1]",
                "expectedOutput": "1"
            },
            {
                "input": "[4,3,2,1,4]",
                "expectedOutput": "16"
            },
            {
                "input": "[1,2,1]",
                "expectedOutput": "2"
            },
            {
                "input": "[2,3,4,5,18,17,6]",
                "expectedOutput": "17"
            },
            {
                "input": "[1,2,3,4,5,6,7,8,9,10]",
                "expectedOutput": "25"
            }
        ]
    },
    {
        "problem_id": "reverse-linked-list",
        "sampleTestCases": [
            {
                "input": "[1,2,3,4,5]",
                "expectedOutput": "[5,4,3,2,1]"
            }
        ],
        "hiddenTestCases": [
            {
                "input": "[1,2]",
                "expectedOutput": "[2,1]"
            },
            {
                "input": "[]",
                "expectedOutput": "[]"
            },
            {
                "input": "[1]",
                "expectedOutput": "[1]"
            },
            {
                "input": "[1,2,3,4,5,6,7,8,9,10]",
                "expectedOutput": "[10,9,8,7,6,5,4,3,2,1]"
            }
        ]
    },
    {
        "problem_id": "linked-list-cycle",
        "sampleTestCases": [
            {
                "input": "[3,2,0,-4], 1",
                "expectedOutput": "true"
            }
        ],
        "hiddenTestCases": [
            {
                "input": "[1,2], 0",
                "expectedOutput": "true"
            },
            {
                "input": "[1], -1",
                "expectedOutput": "false"
            },
            {
                "input": "[1,2,3,4,5], 2",
                "expectedOutput": "true"
            },
            {
                "input": "[1,2,3,4,5], -1",
                "expectedOutput": "false"
            }
        ]
    },
    {
        "problem_id": "climbing-stairs",
        "sampleTestCases": [
            {
                "input": "2",
                "expectedOutput": "2"
            },
            {
                "input": "3",
                "expectedOutput": "3"
            }
        ],
        "hiddenTestCases": [
            {
                "input": "1",
                "expectedOutput": "1"
            },
            {
                "input": "5",
                "expectedOutput": "8"
            },
            {
                "input": "10",
                "expectedOutput": "89"
            },
            {
                "input": "20",
                "expectedOutput": "10946"
            }
        ]
    },
    {
        "problem_id": "house-robber",
        "sampleTestCases": [
            {
                "input": "[1,2,3,1]",
                "expectedOutput": "4"
            }
        ],
        "hiddenTestCases": [
            {
                "input": "[2,7,9,3,1]",
                "expectedOutput": "12"
            },
            {
                "input": "[1]",
                "expectedOutput": "1"
            },
            {
                "input": "[2,1,1,2]",
                "expectedOutput": "4"
            },
            {
                "input": "[5,3,4,11,2]",
                "expectedOutput": "16"
            },
            {
                "input": "[1,3,1,3,100]",
                "expectedOutput": "103"
            }
        ]
    },
    {
        "problem_id": "coin-change",
        "sampleTestCases": [
            {
                "input": "[1,2,5], 11",
                "expectedOutput": "3"
            }
        ],
        "hiddenTestCases": [
            {
                "input": "[2], 3",
                "expectedOutput": "-1"
            },
            {
                "input": "[1], 0",
                "expectedOutput": "0"
            },
            {
                "input": "[1,3,4,5], 7",
                "expectedOutput": "2"
            },
            {
                "input": "[2,5,10,1], 27",
                "expectedOutput": "4"
            },
            {
                "input": "[1], 1",
                "expectedOutput": "1"
            }
        ]
    },
    {
        "problem_id": "palindrome-number",
        "sampleTestCases": [
            {
                "input": "121",
                "expectedOutput": "true"
            },
            {
                "input": "-121",
                "expectedOutput": "false"
            }
        ],
        "hiddenTestCases": [
            {
                "input": "10",
                "expectedOutput": "false"
            },
            {
                "input": "0",
                "expectedOutput": "true"
            },
            {
                "input": "1",
                "expectedOutput": "true"
            },
            {
                "input": "12321",
                "expectedOutput": "true"
            },
            {
                "input": "1000021",
                "expectedOutput": "false"
            }
        ]
    },
    {
        "problem_id": "fizz-buzz",
        "sampleTestCases": [
            {
                "input": "3",
                "expectedOutput": "['1','2','Fizz']"
            },
            {
                "input": "5",
                "expectedOutput": "['1','2','Fizz','4','Buzz']"
            }
        ],
        "hiddenTestCases": [
            {
                "input": "1",
                "expectedOutput": "['1']"
            },
            {
                "input": "15",
                "expectedOutput": "['1','2','Fizz','4','Buzz','Fizz','7','8','Fizz','Buzz','11','Fizz','13','14','FizzBuzz']"
            },
            {
                "input": "10",
                "expectedOutput": "['1','2','Fizz','4','Buzz','Fizz','7','8','Fizz','Buzz']"
            },
            {
                "input": "20",
                "expectedOutput": "['1','2','Fizz','4','Buzz','Fizz','7','8','Fizz','Buzz','11','Fizz','13','14','FizzBuzz','16','17','Fizz','19','Buzz']"
            }
        ]
    },
    {
        "problem_id": "search-rotated-array",
        "sampleTestCases": [
            {
                "input": "[4,5,6,7,0,1,2], 0",
                "expectedOutput": "4"
            }
        ],
        "hiddenTestCases": [
            {
                "input": "[4,5,6,7,0,1,2], 3",
                "expectedOutput": "-1"
            },
            {
                "input": "[1], 0",
                "expectedOutput": "-1"
            },
            {
                "input": "[1], 1",
                "expectedOutput": "0"
            },
            {
                "input": "[3,1], 1",
                "expectedOutput": "1"
            },
            {
                "input": "[5,1,3], 5",
                "expectedOutput": "0"
            }
        ]
    },
    {
        "problem_id": "trapping-rain-water",
        "sampleTestCases": [
            {
                "input": "[0,1,0,2,1,0,1,3,2,1,2,1]",
                "expectedOutput": "6"
            }
        ],
        "hiddenTestCases": [
            {
                "input": "[4,2,0,3,2,5]",
                "expectedOutput": "9"
            },
            {
                "input": "[]",
                "expectedOutput": "0"
            },
            {
                "input": "[3]",
                "expectedOutput": "0"
            },
            {
                "input": "[3,0,2,0,4]",
                "expectedOutput": "7"
            },
            {
                "input": "[1,2,3,4,5]",
                "expectedOutput": "0"
            }
        ]
    }
]

def update_test_cases():
    """
    Update all problems with sampleTestCases and hiddenTestCases
    """
    updated_count = 0
    
    for test_data in test_cases_data:
        result = problems_collection.update_one(
            {"problem_id": test_data["problem_id"]},
            {
                "$set": {
                    "sampleTestCases": test_data["sampleTestCases"],
                    "hiddenTestCases": test_data["hiddenTestCases"]
                }
            }
        )
        
        if result.modified_count > 0:
            updated_count += 1
            print(f"✓ Updated test cases for: {test_data['problem_id']}")
        else:
            print(f"⚠ No update for: {test_data['problem_id']} (problem not found or already updated)")
    
    print(f"\n✅ Successfully updated {updated_count} problems with test cases")
    return updated_count

if __name__ == "__main__":
    update_test_cases()
