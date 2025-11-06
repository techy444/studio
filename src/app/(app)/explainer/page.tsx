"use client"

import { useState } from 'react';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { BotMessageSquare, RefreshCw, Send, Sparkles } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { getApiUrl } from '@/lib/auth';

export default function ExplainerPage() {
  const [code, setCode] = useState(`function MyComponent() {\n  const [value, setValue] = useState(null);\n\n  useEffect(() => {\n    // some side effect\n  }, []);\n\n  return <div>{value}</div>\n}`);
  const [explanation, setExplanation] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!code || code.trim().length < 10) {
      setError('Please enter a valid code snippet (at least 10 characters).');
      return;
    }

    setIsLoading(true);
    setError('');
    setExplanation('');

    try {
      const API_URL = getApiUrl();
      const response = await fetch(`${API_URL}/api/explainer/explain`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code_snippet: code }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to explain code');
      }

      setExplanation(data.explanation);
    } catch (err: any) {
      setError(err.message || 'An error occurred while explaining the code');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mx-auto py-8">
      <div className="space-y-4 mb-8 text-center">
        <div className="inline-block rounded-lg bg-accent/10 p-4">
            <BotMessageSquare className="h-10 w-10 text-accent" />
        </div>
        <h1 className="text-4xl font-bold font-headline tracking-tight">AI Code Explainer</h1>
        <p className="text-muted-foreground max-w-2xl mx-auto">
          Get line-by-line explanations for any code snippet, as if a senior engineer is walking you through it.
        </p>
      </div>
      
      <div className="max-w-4xl mx-auto">
        <form onSubmit={handleSubmit}>
            <Card>
                <CardHeader>
                    <CardTitle className="font-headline">Enter Code Snippet</CardTitle>
                </CardHeader>
                <CardContent>
                    <Textarea 
                        name="codeSnippet"
                        placeholder="Paste your code here..."
                        className="w-full bg-secondary/50 font-code text-base resize-y min-h-[200px]"
                        value={code}
                        onChange={e => setCode(e.target.value)}
                        required
                        minLength={10}
                        disabled={isLoading}
                    />
                </CardContent>
            </Card>
            <div className="flex justify-end mt-4">
                <Button type="submit" size="lg" disabled={isLoading}>
                    {isLoading ? (
                        <>
                            <RefreshCw className="mr-2 h-5 w-5 animate-spin" />
                            Analyzing...
                        </>
                    ) : (
                        <>
                            <Send className="mr-2 h-5 w-5" />
                            Explain Code
                        </>
                    )}
                </Button>
            </div>
        </form>

        {explanation && (
            <div className="mt-8">
                <h2 className="text-2xl font-bold font-headline mb-4 flex items-center gap-2">
                    <Sparkles className="h-6 w-6 text-accent" />
                    Explanation
                </h2>
                <Card>
                    <CardContent className="p-6">
                        <pre className="whitespace-pre-wrap font-body text-foreground/90 text-sm leading-relaxed">
                            {explanation}
                        </pre>
                    </CardContent>
                </Card>
            </div>
        )}
        {error && (
             <Alert variant="destructive" className="mt-8">
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>{error}</AlertDescription>
            </Alert>
        )}
      </div>
    </div>
  );
}
