"use client"
import { placeholderProblems, placeholderUsers } from '@/lib/placeholder-data';
import { notFound } from 'next/navigation';
import { Card, CardContent } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Send, Timer } from 'lucide-react';
import { useState, useEffect } from 'react';
import { Progress } from '@/components/ui/progress';
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar';

const problem = placeholderProblems[1]; // Use a fixed problem for mock battle
const currentUser = placeholderUsers[0];
const opponent = placeholderUsers[1];

export default function BattleRoomPage({ params }: { params: { matchId: string } }) {
  const [code, setCode] = useState('');
  const [timeLeft, setTimeLeft] = useState(300); // 5 minutes
  const [opponentProgress, setOpponentProgress] = useState(10);

  useEffect(() => {
    if(problem) {
      setCode(problem.defaultCode)
    }

    const timer = setInterval(() => {
      setTimeLeft(prev => (prev > 0 ? prev - 1 : 0));
    }, 1000);
    
    const opponentTimer = setInterval(() => {
        setOpponentProgress(prev => Math.min(prev + Math.random() * 10, 100));
    }, 2000);

    return () => {
      clearInterval(timer);
      clearInterval(opponentTimer);
    };
  }, []);

  if (!problem) {
    notFound();
  }
  
  const formatTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="container mx-auto grid md:grid-cols-2 gap-8 py-8 h-full flex-1">
      {/* Problem Description & Opponent Info */}
      <div className="flex flex-col h-full overflow-y-auto pr-4">
        <Card className="mb-6">
            <CardContent className="p-4 flex justify-between items-center">
                <div className="flex items-center gap-3">
                    <Avatar><AvatarImage src={currentUser.avatar} data-ai-hint="avatar" /><AvatarFallback>{currentUser.username[0]}</AvatarFallback></Avatar>
                    <span className="font-bold">{currentUser.username} (You)</span>
                </div>
                <div className="text-2xl font-bold font-headline text-accent">VS</div>
                <div className="flex items-center gap-3">
                    <span className="font-bold">{opponent.username}</span>
                    <Avatar><AvatarImage src={opponent.avatar} data-ai-hint="avatar" /><AvatarFallback>{opponent.username[0]}</AvatarFallback></Avatar>
                </div>
            </CardContent>
        </Card>
        
        <div className="flex items-center justify-between mb-4">
            <h1 className="text-3xl font-bold font-headline tracking-tight">{problem.title}</h1>
            <div className="flex items-center gap-2 text-xl font-semibold bg-secondary px-3 py-1 rounded-md">
                <Timer className="h-6 w-6 text-accent"/>
                {formatTime(timeLeft)}
            </div>
        </div>

        <p className="text-muted-foreground">{problem.description}</p>
        <Separator className="my-6" />
        <h3 className="font-semibold mb-2">Example:</h3>
        <Card>
          <CardContent className="p-4 font-code text-sm">
            <p><span className="font-semibold">Input:</span> {problem.examples[0].input}</p>
            <p><span className="font-semibold">Output:</span> {problem.examples[0].output}</p>
          </CardContent>
        </Card>
      </div>

      {/* Code Editor and Opponent Progress */}
      <div className="flex flex-col h-full">
        <div className="flex-grow flex flex-col">
            <h2 className="text-xl font-bold font-headline mb-2">Your Solution</h2>
            <div className="bg-card border rounded-lg flex-grow flex flex-col">
                <Textarea 
                    placeholder="Write your code here..."
                    className="flex-grow w-full bg-transparent border-0 rounded-t-lg font-code text-base resize-none focus-visible:ring-0"
                    value={code}
                    onChange={e => setCode(e.target.value)}
                />
            </div>
        </div>

        <div className="mt-4 flex-shrink-0 space-y-4">
            <div>
                <div className="flex justify-between items-center mb-1">
                    <label className="text-sm font-medium">Opponent's Progress</label>
                    <span className="text-sm font-bold">{Math.floor(opponentProgress)}%</span>
                </div>
                <Progress value={opponentProgress} className="w-full h-3" />
            </div>
            <Button className="w-full h-12 text-lg">
              <Send className="mr-2 h-5 w-5" />
              Submit & Win
            </Button>
        </div>
      </div>
    </div>
  );
}
