"use client"
import { placeholderProblems } from '@/lib/placeholder-data';
import { notFound } from 'next/navigation';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Play, Send, RefreshCw, AlertCircle } from 'lucide-react';
import { useState, useEffect } from 'react';

const difficultyColors = {
  Easy: 'bg-green-500/20 text-green-400 border-green-500/30 hover:bg-green-500/30',
  Medium: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30 hover:bg-yellow-500/30',
  Hard: 'bg-red-500/20 text-red-400 border-red-500/30 hover:bg-red-500/30',
};

type Output = {
  status: 'initial' | 'running' | 'success' | 'error';
  message: string;
};

export default function ProblemPage({ params }: { params: { problemId: string } }) {
  const problem = placeholderProblems.find(p => p.id === params.problemId);
  const [code, setCode] = useState('');
  const [output, setOutput] = useState<Output>({ status: 'initial', message: 'Run your code to see the output here.' });
  
  useEffect(() => {
    if (problem) {
      setCode(problem.defaultCode);
    }
  }, [problem]);

  if (!problem) {
    notFound();
  }
  
  const handleRunCode = () => {
    setOutput({ status: 'running', message: 'Executing code...' });
    // Mock API call to Judge0
    setTimeout(() => {
        setOutput({ status: 'success', message: 'Test case 1 passed!\nTest case 2 passed!' });
    }, 1500);
  }

  const handleSubmitCode = () => {
    setOutput({ status: 'running', message: 'Submitting final code...' });
    // Mock API call to Judge0
    setTimeout(() => {
        if(Math.random() > 0.3) {
            setOutput({ status: 'success', message: 'Congratulations! All test cases passed.' });
        } else {
            setOutput({ status: 'error', message: 'Submission failed on test case 3: Wrong Answer' });
        }
    }, 2000);
  }

  return (
    <div className="container mx-auto grid md:grid-cols-2 gap-8 py-8 h-full flex-1">
      {/* Problem Description */}
      <div className="flex flex-col h-full overflow-y-auto pr-4">
        <div className="space-y-4">
          <h1 className="text-3xl font-bold font-headline tracking-tight">{problem.title}</h1>
          <div className="flex items-center gap-2">
            <Badge variant="outline" className={difficultyColors[problem.difficulty]}>
              {problem.difficulty}
            </Badge>
            <Badge variant="secondary">{problem.category}</Badge>
          </div>
          <p className="text-muted-foreground">{problem.description}</p>
        </div>

        <Separator className="my-6" />

        <div className="space-y-6">
          {problem.examples.map((example, index) => (
            <div key={index}>
              <h3 className="font-semibold mb-2">Example {index + 1}:</h3>
              <Card>
                <CardContent className="p-4 font-code text-sm">
                  <p><span className="font-semibold">Input:</span> {example.input}</p>
                  <p><span className="font-semibold">Output:</span> {example.output}</p>
                  {example.explanation && <p><span className="font-semibold">Explanation:</span> {example.explanation}</p>}
                </CardContent>
              </Card>
            </div>
          ))}
        </div>
      </div>

      {/* Code Editor and Output */}
      <div className="flex flex-col h-full">
        <div className="flex-grow flex flex-col">
            <h2 className="text-xl font-bold font-headline mb-2">Solution</h2>
            <div className="bg-card border rounded-lg flex-grow flex flex-col relative">
                <Textarea 
                    placeholder="Write your code here..."
                    className="flex-grow w-full bg-transparent border-0 rounded-t-lg font-code text-base resize-none focus-visible:ring-0"
                    value={code}
                    onChange={e => setCode(e.target.value)}
                />
                <Button variant="ghost" size="icon" className="absolute top-2 right-2" onClick={() => setCode(problem.defaultCode)}>
                  <RefreshCw className="h-4 w-4" />
                  <span className="sr-only">Reset Code</span>
                </Button>
            </div>
        </div>

        <div className="mt-4 flex-shrink-0">
          <Tabs defaultValue="output" className="w-full">
            <div className="flex items-center justify-between">
              <TabsList>
                <TabsTrigger value="output">Output</TabsTrigger>
                <TabsTrigger value="testcases">Test Cases</TabsTrigger>
              </TabsList>
              <div className="flex gap-2">
                <Button variant="outline" onClick={handleRunCode} disabled={output.status === 'running'}>
                  <Play className="mr-2 h-4 w-4" />
                  Run
                </Button>
                <Button onClick={handleSubmitCode} disabled={output.status === 'running'}>
                  <Send className="mr-2 h-4 w-4" />
                  Submit
                </Button>
              </div>
            </div>
            <TabsContent value="output" className="mt-2">
              <Card>
                <CardHeader>
                    <CardTitle className="text-lg font-headline">Execution Result</CardTitle>
                </CardHeader>
                <CardContent>
                  <pre className="p-4 bg-secondary/50 rounded-md text-sm font-code whitespace-pre-wrap min-h-[100px]">
                    {output.status === 'running' && <p className="flex items-center gap-2"><RefreshCw className="h-4 w-4 animate-spin"/>{output.message}</p>}
                    {output.status === 'initial' && <p className="text-muted-foreground">{output.message}</p>}
                    {output.status === 'success' && <p className="text-green-400">{output.message}</p>}
                    {output.status === 'error' && <p className="text-red-400 flex items-center gap-2"><AlertCircle className="h-4 w-4"/>{output.message}</p>}
                  </pre>
                </CardContent>
              </Card>
            </TabsContent>
            <TabsContent value="testcases" className="mt-2">
              <Card>
                <CardContent className="p-4">
                  <div className="space-y-2">
                    {problem.testCases.map((tc, index) => (
                      <div key={index} className="font-code text-sm">
                        <p className="font-semibold">Case {index + 1}:</p>
                        <p><span className="text-muted-foreground">Input:</span> {tc.input}</p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
}
