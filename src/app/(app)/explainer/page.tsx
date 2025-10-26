"use client"

import { useState } from 'react';
import { useFormState, useFormStatus } from 'react-dom';
import { codeSnippetExplainer } from '@/ai/flows/code-snippet-explainer';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { BotMessageSquare, RefreshCw, Send, Sparkles } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';

const initialState = {
  explanation: '',
  error: '',
};

async function explainerFormAction(prevState: any, formData: FormData) {
  const codeSnippet = formData.get('codeSnippet') as string;
  if (!codeSnippet || codeSnippet.trim().length < 10) {
      return { explanation: '', error: 'Please enter a valid code snippet (at least 10 characters).' };
  }
  try {
    const result = await codeSnippetExplainer({ codeSnippet });
    return { explanation: result.explanation, error: '' };
  } catch (e: any) {
    return { explanation: '', error: e.message || 'An unknown error occurred.' };
  }
}

function SubmitButton() {
    const { pending } = useFormStatus();
    return (
        <Button type="submit" size="lg" disabled={pending}>
            {pending ? (
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
    )
}

export default function ExplainerPage() {
  const [state, formAction] = useFormState(explainerFormAction, initialState);
  const [code, setCode] = useState(`function MyComponent() {\n  const [value, setValue] = useState(null);\n\n  useEffect(() => {\n    // some side effect\n  }, []);\n\n  return <div>{value}</div>\n}`);

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
        <form action={formAction}>
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
                    />
                </CardContent>
            </Card>
            <div className="flex justify-end mt-4">
                <SubmitButton />
            </div>
        </form>

        {state.explanation && (
            <div className="mt-8">
                <h2 className="text-2xl font-bold font-headline mb-4 flex items-center gap-2">
                    <Sparkles className="h-6 w-6 text-accent" />
                    Explanation
                </h2>
                <Card>
                    <CardContent className="p-6">
                        <pre className="whitespace-pre-wrap font-body text-foreground/90 text-sm leading-relaxed">
                            {state.explanation}
                        </pre>
                    </CardContent>
                </Card>
            </div>
        )}
        {state.error && (
             <Alert variant="destructive" className="mt-8">
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>{state.error}</AlertDescription>
            </Alert>
        )}
      </div>
    </div>
  );
}
