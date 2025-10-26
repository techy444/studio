"use client";

import { useState } from 'react';
import Link from 'next/link';
import { placeholderProblems } from '@/lib/placeholder-data';
import type { Problem } from '@/lib/types';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Button } from '@/components/ui/button';
import { Search, ArrowRight } from 'lucide-react';

const difficultyColors = {
  Easy: 'bg-green-500/20 text-green-400 border-green-500/30 hover:bg-green-500/30',
  Medium: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30 hover:bg-yellow-500/30',
  Hard: 'bg-red-500/20 text-red-400 border-red-500/30 hover:bg-red-500/30',
};

const categories = [...new Set(placeholderProblems.map(p => p.category))];

export default function PracticePage() {
  const [search, setSearch] = useState('');
  const [difficulty, setDifficulty] = useState('all');
  const [category, setCategory] = useState('all');

  const filteredProblems = placeholderProblems.filter(problem => {
    return (
      (problem.title.toLowerCase().includes(search.toLowerCase()) ||
       problem.description.toLowerCase().includes(search.toLowerCase())) &&
      (difficulty === 'all' || problem.difficulty === difficulty) &&
      (category === 'all' || problem.category === category)
    );
  });

  return (
    <div className="container mx-auto py-8">
      <div className="space-y-4 mb-8">
        <h1 className="text-4xl font-bold font-headline tracking-tight">Problem Set</h1>
        <p className="text-muted-foreground">
          Sharpen your coding skills with our collection of problems. Filter by difficulty, category, or search by keyword.
        </p>
      </div>

      <div className="flex flex-col md:flex-row gap-4 mb-8">
        <div className="relative flex-grow">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
          <Input 
            placeholder="Search problems..." 
            className="pl-10"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <Select value={difficulty} onValueChange={setDifficulty}>
          <SelectTrigger className="w-full md:w-[180px]">
            <SelectValue placeholder="Difficulty" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Difficulties</SelectItem>
            <SelectItem value="Easy">Easy</SelectItem>
            <SelectItem value="Medium">Medium</SelectItem>
            <SelectItem value="Hard">Hard</SelectItem>
          </SelectContent>
        </Select>
        <Select value={category} onValueChange={setCategory}>
          <SelectTrigger className="w-full md:w-[180px]">
            <SelectValue placeholder="Category" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Categories</SelectItem>
            {categories.map(cat => (
              <SelectItem key={cat} value={cat}>{cat}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredProblems.map((problem) => (
          <Card key={problem.id} className="flex flex-col hover:border-accent transition-colors">
            <CardHeader>
              <CardTitle className="font-headline text-xl">{problem.title}</CardTitle>
              <CardDescription className="line-clamp-2">{problem.description}</CardDescription>
            </CardHeader>
            <CardContent className="flex-grow">
              <div className="flex items-center gap-2">
                <Badge variant="outline" className={difficultyColors[problem.difficulty]}>
                  {problem.difficulty}
                </Badge>
                <Badge variant="secondary">{problem.category}</Badge>
              </div>
            </CardContent>
            <CardFooter>
              <Link href={`/practice/${problem.id}`} className="w-full">
                <Button className="w-full">
                  Solve Problem <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </Link>
            </CardFooter>
          </Card>
        ))}
      </div>
      {filteredProblems.length === 0 && (
        <div className="text-center py-16 text-muted-foreground">
          <p>No problems found matching your criteria.</p>
        </div>
      )}
    </div>
  );
}
