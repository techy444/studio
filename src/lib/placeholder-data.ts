import type { Problem, User } from './types';

export const placeholderProblems: Problem[] = [
  {
    id: 'two-sum',
    title: 'Two Sum',
    description: 'Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`. You may assume that each input would have exactly one solution, and you may not use the same element twice. You can return the answer in any order.',
    difficulty: 'Easy',
    category: 'Arrays',
    examples: [
      {
        input: 'nums = [2,7,11,15], target = 9',
        output: '[0,1]',
        explanation: 'Because nums[0] + nums[1] == 9, we return [0, 1].',
      },
      {
        input: 'nums = [3,2,4], target = 6',
        output: '[1,2]',
      },
    ],
    testCases: [
      { input: '[2,7,11,15], 9', expectedOutput: '[0,1]' },
      { input: '[3,2,4], 6', expectedOutput: '[1,2]' },
      { input: '[3,3], 6', expectedOutput: '[0,1]' },
    ],
    defaultCode: `function twoSum(nums, target) {\n  // Write your code here\n};`
  },
  {
    id: 'valid-parentheses',
    title: 'Valid Parentheses',
    description: "Given a string `s` containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid. An input string is valid if: Open brackets must be closed by the same type of brackets. Open brackets must be closed in the correct order. Every close bracket has a corresponding open bracket of the same type.",
    difficulty: 'Easy',
    category: 'Stacks',
    examples: [
      {
        input: 's = "()"',
        output: 'true',
      },
      {
        input: 's = "()[]{}"',
        output: 'true',
      },
      {
        input: 's = "(]"',
        output: 'false',
      },
    ],
    testCases: [
        { input: '"()"', expectedOutput: 'true' },
        { input: '"()[]{}"', expectedOutput: 'true' },
        { input: '"(]"', expectedOutput: 'false' },
        { input: '"{[]}"', expectedOutput: 'true' },
    ],
    defaultCode: `function isValid(s) {\n  // Write your code here\n};`
  },
  {
    id: 'reverse-linked-list',
    title: 'Reverse Linked List',
    description: 'Given the `head` of a singly linked list, reverse the list, and return the reversed list.',
    difficulty: 'Medium',
    category: 'Linked List',
    examples: [
      {
        input: 'head = [1,2,3,4,5]',
        output: '[5,4,3,2,1]',
      },
    ],
    testCases: [
        { input: '[1,2,3,4,5]', expectedOutput: '[5,4,3,2,1]' },
        { input: '[1,2]', expectedOutput: '[2,1]' },
        { input: '[]', expectedOutput: '[]' },
    ],
    defaultCode: `/**\n * Definition for singly-linked list.\n * function ListNode(val, next) {\n *     this.val = (val===undefined ? 0 : val)\n *     this.next = (next===undefined ? null : next)\n * }\n */\nfunction reverseList(head) {\n  // Write your code here\n};`
  }
];

export const placeholderUsers: User[] = [
    { id: 'user1', username: 'codeMaster', avatar: 'https://picsum.photos/seed/user1/150/150', totalPoints: 1250, wins: 25, losses: 5, rank: 1 },
    { id: 'user2', username: 'algoQueen', avatar: 'https://picsum.photos/seed/user2/150/150', totalPoints: 1180, wins: 22, losses: 8, rank: 2 },
    { id: 'user3', username: 'BytePioneer', avatar: 'https://picsum.photos/seed/user3/150/150', totalPoints: 1050, wins: 20, losses: 10, rank: 3 },
    { id: 'user4', username: 'SyntaxSlayer', avatar: 'https://picsum.photos/seed/user4/150/150', totalPoints: 980, wins: 18, losses: 7, rank: 4 },
    { id: 'user5', username: 'LogicLich', avatar: 'https://picsum.photos/seed/user5/150/150', totalPoints: 900, wins: 15, losses: 12, rank: 5 },
    { id: 'user6', username: 'KernelKnight', avatar: 'https://picsum.photos/seed/user6/150/150', totalPoints: 850, wins: 14, losses: 9, rank: 6 },
    { id: 'user7', username: 'ReactRebel', avatar: 'https://picsum.photos/seed/user7/150/150', totalPoints: 760, wins: 12, losses: 11, rank: 7 },
    { id: 'user8', username: 'NodeNinja', avatar: 'https://picsum.photos/seed/user8/150/150', totalPoints: 700, wins: 10, losses: 10, rank: 8 },
].sort((a, b) => b.totalPoints - a.totalPoints).map((user, index) => ({ ...user, rank: index + 1 }));
