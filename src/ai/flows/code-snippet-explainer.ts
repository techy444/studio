'use server';

/**
 * @fileOverview Explains a code snippet line by line as if explained by a senior engineer.
 *
 * - codeSnippetExplainer - A function that explains the code snippet.
 * - CodeSnippetExplainerInput - The input type for the codeSnippetExplainer function.
 * - CodeSnippetExplainerOutput - The return type for the codeSnippetExplainer function.
 */

import {ai} from '@/ai/genkit';
import {z} from 'genkit';

const CodeSnippetExplainerInputSchema = z.object({
  codeSnippet: z
    .string()
    .describe('The code snippet to be explained.'),
});
export type CodeSnippetExplainerInput = z.infer<typeof CodeSnippetExplainerInputSchema>;

const CodeSnippetExplainerOutputSchema = z.object({
  explanation: z
    .string()
    .describe('The line by line explanation of the code snippet.'),
});
export type CodeSnippetExplainerOutput = z.infer<typeof CodeSnippetExplainerOutputSchema>;

export async function codeSnippetExplainer(input: CodeSnippetExplainerInput): Promise<CodeSnippetExplainerOutput> {
  return codeSnippetExplainerFlow(input);
}

const prompt = ai.definePrompt({
  name: 'codeSnippetExplainerPrompt',
  input: {schema: CodeSnippetExplainerInputSchema},
  output: {schema: CodeSnippetExplainerOutputSchema},
  prompt: `You are a senior engineer explaining the following code snippet line by line. Identify and explain any relevant programming paradigms such as dependency injection.

Code Snippet:
\`\`\`
{{{codeSnippet}}}
\`\`\`

Explanation:`, 
});

const codeSnippetExplainerFlow = ai.defineFlow(
  {
    name: 'codeSnippetExplainerFlow',
    inputSchema: CodeSnippetExplainerInputSchema,
    outputSchema: CodeSnippetExplainerOutputSchema,
  },
  async input => {
    const {output} = await prompt(input);
    return output!;
  }
);
