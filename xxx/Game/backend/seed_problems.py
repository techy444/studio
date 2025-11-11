"""
Seed the database with LeetCode-style problems
"""
from database import problems_collection
from datetime import datetime

# Clear existing problems
problems_collection.delete_many({})

problems = [
    {
        "problem_id": "two-sum",
        "title": "Two Sum",
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution, and you may not use the same element twice.",
        "difficulty": "Easy",
        "category": "Arrays",
        "examples": [
            {
                "input": "nums = [2,7,11,15], target = 9",
                "output": "[0,1]",
                "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."
            },
            {
                "input": "nums = [3,2,4], target = 6",
                "output": "[1,2]"
            }
        ],
        "testCases": [
            {"input": "[2,7,11,15], 9", "expectedOutput": "[0,1]"},
            {"input": "[3,2,4], 6", "expectedOutput": "[1,2]"},
            {"input": "[3,3], 6", "expectedOutput": "[0,1]"}
        ],
        "defaultCode": "function twoSum(nums, target) {\n  // Write your code here\n};"
    },
    {
        "problem_id": "reverse-string",
        "title": "Reverse String",
        "description": "Write a function that reverses a string. The input string is given as an array of characters s. You must do this by modifying the input array in-place with O(1) extra memory.",
        "difficulty": "Easy",
        "category": "Strings",
        "examples": [
            {
                "input": "s = ['h','e','l','l','o']",
                "output": "['o','l','l','e','h']"
            },
            {
                "input": "s = ['H','a','n','n','a','h']",
                "output": "['h','a','n','n','a','H']"
            }
        ],
        "testCases": [
            {"input": "['h','e','l','l','o']", "expectedOutput": "['o','l','l','e','h']"},
            {"input": "['H','a','n','n','a','h']", "expectedOutput": "['h','a','n','n','a','H']"}
        ],
        "defaultCode": "function reverseString(s) {\n  // Write your code here\n};"
    },
    {
        "problem_id": "valid-parentheses",
        "title": "Valid Parentheses",
        "description": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid. An input string is valid if: Open brackets must be closed by the same type of brackets. Open brackets must be closed in the correct order.",
        "difficulty": "Easy",
        "category": "Strings",
        "examples": [
            {
                "input": "s = '()'",
                "output": "true"
            },
            {
                "input": "s = '()[]{}'",
                "output": "true"
            },
            {
                "input": "s = '(]'",
                "output": "false"
            }
        ],
        "testCases": [
            {"input": "'()'", "expectedOutput": "true"},
            {"input": "'()[]{}'", "expectedOutput": "true"},
            {"input": "'(]'", "expectedOutput": "false"}
        ],
        "defaultCode": "function isValid(s) {\n  // Write your code here\n};"
    },
    {
        "problem_id": "merge-sorted-arrays",
        "title": "Merge Sorted Array",
        "description": "You are given two integer arrays nums1 and nums2, sorted in non-decreasing order, and two integers m and n, representing the number of elements in nums1 and nums2 respectively. Merge nums1 and nums2 into a single array sorted in non-decreasing order.",
        "difficulty": "Easy",
        "category": "Arrays",
        "examples": [
            {
                "input": "nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3",
                "output": "[1,2,2,3,5,6]"
            }
        ],
        "testCases": [
            {"input": "[1,2,3,0,0,0], 3, [2,5,6], 3", "expectedOutput": "[1,2,2,3,5,6]"}
        ],
        "defaultCode": "function merge(nums1, m, nums2, n) {\n  // Write your code here\n};"
    },
    {
        "problem_id": "maximum-subarray",
        "title": "Maximum Subarray",
        "description": "Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum. A subarray is a contiguous part of an array.",
        "difficulty": "Medium",
        "category": "Arrays",
        "examples": [
            {
                "input": "nums = [-2,1,-3,4,-1,2,1,-5,4]",
                "output": "6",
                "explanation": "[4,-1,2,1] has the largest sum = 6."
            }
        ],
        "testCases": [
            {"input": "[-2,1,-3,4,-1,2,1,-5,4]", "expectedOutput": "6"},
            {"input": "[1]", "expectedOutput": "1"},
            {"input": "[5,4,-1,7,8]", "expectedOutput": "23"}
        ],
        "defaultCode": "function maxSubArray(nums) {\n  // Write your code here\n};"
    },
    {
        "problem_id": "longest-substring",
        "title": "Longest Substring Without Repeating Characters",
        "description": "Given a string s, find the length of the longest substring without repeating characters.",
        "difficulty": "Medium",
        "category": "Strings",
        "examples": [
            {
                "input": "s = 'abcabcbb'",
                "output": "3",
                "explanation": "The answer is 'abc', with the length of 3."
            },
            {
                "input": "s = 'bbbbb'",
                "output": "1",
                "explanation": "The answer is 'b', with the length of 1."
            }
        ],
        "testCases": [
            {"input": "'abcabcbb'", "expectedOutput": "3"},
            {"input": "'bbbbb'", "expectedOutput": "1"},
            {"input": "'pwwkew'", "expectedOutput": "3"}
        ],
        "defaultCode": "function lengthOfLongestSubstring(s) {\n  // Write your code here\n};"
    },
    {
        "problem_id": "container-with-most-water",
        "title": "Container With Most Water",
        "description": "You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]). Find two lines that together with the x-axis form a container, such that the container contains the most water.",
        "difficulty": "Medium",
        "category": "Arrays",
        "examples": [
            {
                "input": "height = [1,8,6,2,5,4,8,3,7]",
                "output": "49",
                "explanation": "The vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. The max area = 49."
            }
        ],
        "testCases": [
            {"input": "[1,8,6,2,5,4,8,3,7]", "expectedOutput": "49"},
            {"input": "[1,1]", "expectedOutput": "1"}
        ],
        "defaultCode": "function maxArea(height) {\n  // Write your code here\n};"
    },
    {
        "problem_id": "reverse-linked-list",
        "title": "Reverse Linked List",
        "description": "Given the head of a singly linked list, reverse the list, and return the reversed list.",
        "difficulty": "Easy",
        "category": "Linked List",
        "examples": [
            {
                "input": "head = [1,2,3,4,5]",
                "output": "[5,4,3,2,1]"
            }
        ],
        "testCases": [
            {"input": "[1,2,3,4,5]", "expectedOutput": "[5,4,3,2,1]"},
            {"input": "[1,2]", "expectedOutput": "[2,1]"}
        ],
        "defaultCode": "function reverseList(head) {\n  // Write your code here\n};"
    },
    {
        "problem_id": "linked-list-cycle",
        "title": "Linked List Cycle",
        "description": "Given head, the head of a linked list, determine if the linked list has a cycle in it. There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the next pointer.",
        "difficulty": "Easy",
        "category": "Linked List",
        "examples": [
            {
                "input": "head = [3,2,0,-4], pos = 1",
                "output": "true",
                "explanation": "There is a cycle in the linked list, where the tail connects to the 1st node (0-indexed)."
            }
        ],
        "testCases": [
            {"input": "[3,2,0,-4], pos = 1", "expectedOutput": "true"},
            {"input": "[1,2], pos = 0", "expectedOutput": "true"},
            {"input": "[1], pos = -1", "expectedOutput": "false"}
        ],
        "defaultCode": "function hasCycle(head) {\n  // Write your code here\n};"
    },
    {
        "problem_id": "binary-tree-inorder",
        "title": "Binary Tree Inorder Traversal",
        "description": "Given the root of a binary tree, return the inorder traversal of its nodes' values.",
        "difficulty": "Easy",
        "category": "Math",
        "examples": [
            {
                "input": "root = [1,null,2,3]",
                "output": "[1,3,2]"
            }
        ],
        "testCases": [
            {"input": "[1,null,2,3]", "expectedOutput": "[1,3,2]"},
            {"input": "[]", "expectedOutput": "[]"},
            {"input": "[1]", "expectedOutput": "[1]"}
        ],
        "defaultCode": "function inorderTraversal(root) {\n  // Write your code here\n};"
    },
    {
        "problem_id": "climbing-stairs",
        "title": "Climbing Stairs",
        "description": "You are climbing a staircase. It takes n steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?",
        "difficulty": "Easy",
        "category": "Dynamic Programming",
        "examples": [
            {
                "input": "n = 2",
                "output": "2",
                "explanation": "There are two ways to climb to the top: 1. 1 step + 1 step, 2. 2 steps"
            },
            {
                "input": "n = 3",
                "output": "3",
                "explanation": "There are three ways: 1. 1+1+1, 2. 1+2, 3. 2+1"
            }
        ],
        "testCases": [
            {"input": "2", "expectedOutput": "2"},
            {"input": "3", "expectedOutput": "3"},
            {"input": "5", "expectedOutput": "8"}
        ],
        "defaultCode": "function climbStairs(n) {\n  // Write your code here\n};"
    },
    {
        "problem_id": "house-robber",
        "title": "House Robber",
        "description": "You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night. Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.",
        "difficulty": "Medium",
        "category": "Dynamic Programming",
        "examples": [
            {
                "input": "nums = [1,2,3,1]",
                "output": "4",
                "explanation": "Rob house 1 (money = 1) and then rob house 3 (money = 3). Total = 1 + 3 = 4."
            }
        ],
        "testCases": [
            {"input": "[1,2,3,1]", "expectedOutput": "4"},
            {"input": "[2,7,9,3,1]", "expectedOutput": "12"}
        ],
        "defaultCode": "function rob(nums) {\n  // Write your code here\n};"
    },
    {
        "problem_id": "coin-change",
        "title": "Coin Change",
        "description": "You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money. Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.",
        "difficulty": "Medium",
        "category": "Dynamic Programming",
        "examples": [
            {
                "input": "coins = [1,2,5], amount = 11",
                "output": "3",
                "explanation": "11 = 5 + 5 + 1"
            }
        ],
        "testCases": [
            {"input": "[1,2,5], 11", "expectedOutput": "3"},
            {"input": "[2], 3", "expectedOutput": "-1"},
            {"input": "[1], 0", "expectedOutput": "0"}
        ],
        "defaultCode": "function coinChange(coins, amount) {\n  // Write your code here\n};"
    },
    {
        "problem_id": "palindrome-number",
        "title": "Palindrome Number",
        "description": "Given an integer x, return true if x is a palindrome, and false otherwise. An integer is a palindrome when it reads the same forward and backward.",
        "difficulty": "Easy",
        "category": "Math",
        "examples": [
            {
                "input": "x = 121",
                "output": "true",
                "explanation": "121 reads as 121 from left to right and from right to left."
            },
            {
                "input": "x = -121",
                "output": "false",
                "explanation": "From left to right, it reads -121. From right to left, it becomes 121-."
            }
        ],
        "testCases": [
            {"input": "121", "expectedOutput": "true"},
            {"input": "-121", "expectedOutput": "false"},
            {"input": "10", "expectedOutput": "false"}
        ],
        "defaultCode": "function isPalindrome(x) {\n  // Write your code here\n};"
    },
    {
        "problem_id": "fizz-buzz",
        "title": "Fizz Buzz",
        "description": "Given an integer n, return a string array answer (1-indexed) where: answer[i] == 'FizzBuzz' if i is divisible by 3 and 5. answer[i] == 'Fizz' if i is divisible by 3. answer[i] == 'Buzz' if i is divisible by 5. answer[i] == i (as a string) if none of the above conditions are true.",
        "difficulty": "Easy",
        "category": "Math",
        "examples": [
            {
                "input": "n = 3",
                "output": "['1','2','Fizz']"
            },
            {
                "input": "n = 5",
                "output": "['1','2','Fizz','4','Buzz']"
            }
        ],
        "testCases": [
            {"input": "3", "expectedOutput": "['1','2','Fizz']"},
            {"input": "5", "expectedOutput": "['1','2','Fizz','4','Buzz']"},
            {"input": "15", "expectedOutput": "['1','2','Fizz','4','Buzz','Fizz','7','8','Fizz','Buzz','11','Fizz','13','14','FizzBuzz']"}
        ],
        "defaultCode": "function fizzBuzz(n) {\n  // Write your code here\n};"
    },
    {
        "problem_id": "number-of-islands",
        "title": "Number of Islands",
        "description": "Given an m x n 2D binary grid which represents a map of '1's (land) and '0's (water), return the number of islands. An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.",
        "difficulty": "Medium",
        "category": "Graphs",
        "examples": [
            {
                "input": "grid = [['1','1','1','1','0'],['1','1','0','1','0'],['1','1','0','0','0'],['0','0','0','0','0']]",
                "output": "1"
            }
        ],
        "testCases": [
            {"input": "[['1','1','1','1','0'],['1','1','0','1','0'],['1','1','0','0','0'],['0','0','0','0','0']]", "expectedOutput": "1"}
        ],
        "defaultCode": "function numIslands(grid) {\n  // Write your code here\n};"
    },
    {
        "problem_id": "course-schedule",
        "title": "Course Schedule",
        "description": "There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai. Return true if you can finish all courses. Otherwise, return false.",
        "difficulty": "Medium",
        "category": "Graphs",
        "examples": [
            {
                "input": "numCourses = 2, prerequisites = [[1,0]]",
                "output": "true",
                "explanation": "There are a total of 2 courses to take. To take course 1 you should have finished course 0. So it is possible."
            }
        ],
        "testCases": [
            {"input": "2, [[1,0]]", "expectedOutput": "true"},
            {"input": "2, [[1,0],[0,1]]", "expectedOutput": "false"}
        ],
        "defaultCode": "function canFinish(numCourses, prerequisites) {\n  // Write your code here\n};"
    },
    {
        "problem_id": "search-rotated-array",
        "title": "Search in Rotated Sorted Array",
        "description": "There is an integer array nums sorted in ascending order (with distinct values). Prior to being passed to your function, nums is possibly rotated at an unknown pivot index. Given the array nums after the possible rotation and an integer target, return the index of target if it is in nums, or -1 if it is not in nums.",
        "difficulty": "Medium",
        "category": "Arrays",
        "examples": [
            {
                "input": "nums = [4,5,6,7,0,1,2], target = 0",
                "output": "4"
            }
        ],
        "testCases": [
            {"input": "[4,5,6,7,0,1,2], 0", "expectedOutput": "4"},
            {"input": "[4,5,6,7,0,1,2], 3", "expectedOutput": "-1"},
            {"input": "[1], 0", "expectedOutput": "-1"}
        ],
        "defaultCode": "function search(nums, target) {\n  // Write your code here\n};"
    },
    {
        "problem_id": "word-ladder",
        "title": "Word Ladder",
        "description": "A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence of words beginWord -> s1 -> s2 -> ... -> sk such that: Every adjacent pair of words differs by a single letter. Return the number of words in the shortest transformation sequence from beginWord to endWord, or 0 if no such sequence exists.",
        "difficulty": "Hard",
        "category": "Graphs",
        "examples": [
            {
                "input": "beginWord = 'hit', endWord = 'cog', wordList = ['hot','dot','dog','lot','log','cog']",
                "output": "5",
                "explanation": "One shortest transformation sequence is 'hit' -> 'hot' -> 'dot' -> 'dog' -> 'cog', which is 5 words long."
            }
        ],
        "testCases": [
            {"input": "'hit', 'cog', ['hot','dot','dog','lot','log','cog']", "expectedOutput": "5"},
            {"input": "'hit', 'cog', ['hot','dot','dog','lot','log']", "expectedOutput": "0"}
        ],
        "defaultCode": "function ladderLength(beginWord, endWord, wordList) {\n  // Write your code here\n};"
    },
    {
        "problem_id": "trapping-rain-water",
        "title": "Trapping Rain Water",
        "description": "Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
        "difficulty": "Hard",
        "category": "Arrays",
        "examples": [
            {
                "input": "height = [0,1,0,2,1,0,1,3,2,1,2,1]",
                "output": "6",
                "explanation": "The elevation map is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water are being trapped."
            }
        ],
        "testCases": [
            {"input": "[0,1,0,2,1,0,1,3,2,1,2,1]", "expectedOutput": "6"},
            {"input": "[4,2,0,3,2,5]", "expectedOutput": "9"}
        ],
        "defaultCode": "function trap(height) {\n  // Write your code here\n};"
    }
]

# Insert problems
result = problems_collection.insert_many(problems)
print(f"✓ Successfully inserted {len(result.inserted_ids)} problems into the database")

# Print summary by category and difficulty
from collections import Counter
categories = Counter(p["category"] for p in problems)
difficulties = Counter(p["difficulty"] for p in problems)

print("\n📊 Problems Summary:")
print(f"Total: {len(problems)} problems")
print(f"\nBy Difficulty:")
for diff, count in difficulties.items():
    print(f"  {diff}: {count}")
print(f"\nBy Category:")
for cat, count in categories.items():
    print(f"  {cat}: {count}")
