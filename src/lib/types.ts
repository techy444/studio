export type Problem = {
  id: string;
  title: string;
  description: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  category: string;
  examples: { input: string; output: string; explanation?: string }[];
  testCases: { input: string; expectedOutput: string }[];
  defaultCode: string;
};

export type User = {
  id: string;
  username: string;
  avatar: string;
  totalPoints: number;
  wins: number;
  losses: number;
  rank: number;
};
