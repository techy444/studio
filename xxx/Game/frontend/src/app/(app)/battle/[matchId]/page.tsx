"use client"
import { placeholderProblems, placeholderUsers } from '@/lib/placeholder-data';
import { notFound, useRouter } from 'next/navigation';
import { Card, CardContent } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { Button } from '@/components/ui/button';
import { Send, Timer, Loader2, RefreshCw } from 'lucide-react';
import { useState, useEffect } from 'react';
import { Progress } from '@/components/ui/progress';
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar';
import { useToast } from '@/hooks/use-toast';
import { authenticatedFetch } from '@/lib/auth';
import dynamic from 'next/dynamic';
import { createCppTemplate } from '@/components/CodeEditor';

// Dynamically import CodeEditor to avoid SSR issues with Monaco
const CodeEditor = dynamic(() => import('@/components/CodeEditor'), {
  ssr: false,
  loading: () => (
    <div className="h-full w-full flex items-center justify-center bg-card border rounded-lg">
      <Loader2 className="h-6 w-6 animate-spin text-accent" />
    </div>
  ),
});

const problem = placeholderProblems[1]; // Use a fixed problem for mock battle
const currentUser = placeholderUsers[0];
const opponent = placeholderUsers[1];

export default function BattleRoomPage({ params }: { params: { matchId: string } }) {
  const [code, setCode] = useState('');
  const [defaultCode, setDefaultCode] = useState('');
  const [resetTrigger, setResetTrigger] = useState(0);
  const [timeLeft, setTimeLeft] = useState(1800); // 30 minutes (1800 seconds)
  const [opponentProgress, setOpponentProgress] = useState(10);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [battleEnded, setBattleEnded] = useState(false);
  const router = useRouter();
  const { toast } = useToast();

  useEffect(() => {
    if(problem) {
      // Create C++ template for the battle problem
      // Extract function signature from defaultCode if possible
      const template = createCppTemplate(problem.title, 'bool isValid(string s)');
      setDefaultCode(template);
      setCode(template);
    }

    const timer = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          // Time's up! Handle timeout
          handleTimeout();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    
    const opponentTimer = setInterval(() => {
        setOpponentProgress(prev => Math.min(prev + Math.random() * 10, 100));
    }, 2000);

    return () => {
      clearInterval(timer);
      clearInterval(opponentTimer);
    };
  }, []);

  const handleTimeout = async () => {
    if (battleEnded) return;
    setBattleEnded(true);

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';
      await authenticatedFetch(`${API_URL}/api/battle/timeout`, {
        method: 'POST',
        body: JSON.stringify({
          battle_id: params.matchId,
          winner_id: null
        })
      });

      toast({
        title: "Time's Up!",
        description: "The battle has ended due to timeout.",
        variant: "destructive"
      });

      setTimeout(() => {
        router.push('/battle');
      }, 2000);
    } catch (error) {
      console.error('Error handling timeout:', error);
    }
  };

  const handleSubmitCode = async () => {
    if (isSubmitting || battleEnded) return;
    
    setIsSubmitting(true);
    
    try {
      // Extract only user-written code for submission
      const lines = code.split('\n');
      let startIdx = -1;
      let endIdx = -1;
      
      lines.forEach((line, index) => {
        if (line.trim().includes('// USER CODE START')) {
          startIdx = index + 1;
        }
        if (line.trim().includes('// USER CODE END')) {
          endIdx = index;
        }
      });
      
      const userCode = startIdx !== -1 && endIdx !== -1 
        ? lines.slice(startIdx, endIdx).join('\n').trim()
        : code;

      // TODO: Send userCode to backend for evaluation
      console.log('Submitting user code:', userCode);
      
      // Mock submission
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      toast({
        title: "Code Submitted!",
        description: "Your solution has been submitted for evaluation.",
      });
      
      setBattleEnded(true);
      
      setTimeout(() => {
        router.push('/battle');
      }, 2000);
    } catch (error) {
      console.error('Error submitting code:', error);
      toast({
        title: "Submission Failed",
        description: "Failed to submit your code. Please try again.",
        variant: "destructive"
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleResetCode = () => {
    setResetTrigger(prev => prev + 1);
    toast({
      title: "Code Reset",
      description: "Your code has been reset to the default template.",
    });
  };

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
        <div className="flex-grow flex flex-col min-h-[500px]">
            <div className="flex items-center justify-between mb-2">
              <h2 className="text-xl font-bold font-headline">Your Solution</h2>
              <Button 
                variant="outline" 
                size="sm" 
                onClick={handleResetCode}
                disabled={isSubmitting || battleEnded}
                data-testid="reset-code-button"
              >
                <RefreshCw className="mr-2 h-4 w-4" />
                Reset Code
              </Button>
            </div>
            <div className="flex-grow">
              <CodeEditor
                defaultCode={defaultCode}
                onChange={setCode}
                onResetTrigger={resetTrigger}
                language="cpp"
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
            <Button 
              className="w-full h-12 text-lg" 
              onClick={handleSubmitCode}
              disabled={isSubmitting || battleEnded}
              data-testid="submit-battle-code"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Submitting...
                </>
              ) : (
                <>
                  <Send className="mr-2 h-5 w-5" />
                  Submit & Win
                </>
              )}
            </Button>
        </div>
      </div>
    </div>
  );
}