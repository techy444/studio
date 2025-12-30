"use client";

import { useState } from 'react';
import dynamic from 'next/dynamic';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Code2, RefreshCw, Download, Loader2 } from 'lucide-react';
import { createCppTemplate } from '@/components/CodeEditor';

const CodeEditor = dynamic(() => import('@/components/CodeEditor'), {
  ssr: false,
  loading: () => (
    <div className="h-[500px] w-full flex items-center justify-center bg-card border rounded-lg">
      <Loader2 className="h-6 w-6 animate-spin text-accent" />
    </div>
  ),
});

export default function EditorDemo() {
  const [code, setCode] = useState('');
  const [resetTrigger, setResetTrigger] = useState(0);
  const [extractedCode, setExtractedCode] = useState('');

  const defaultTemplate = createCppTemplate(
    'Two Sum',
    'vector<int> twoSum(vector<int>& nums, int target)'
  );

  const handleReset = () => {
    setResetTrigger(prev => prev + 1);
    setExtractedCode('');
  };

  const handleExtractCode = () => {
    // Extract only the user-written code between markers
    const lines = code.split('\n');
    let startLine = -1;
    let endLine = -1;

    lines.forEach((line, index) => {
      if (line.trim().includes('// USER CODE START')) {
        startLine = index + 1;
      }
      if (line.trim().includes('// USER CODE END')) {
        endLine = index;
      }
    });

    if (startLine !== -1 && endLine !== -1 && startLine < endLine) {
      const userCode = lines.slice(startLine, endLine).join('\n').trim();
      setExtractedCode(userCode);
    } else {
      setExtractedCode('// No user code found');
    }
  };

  return (
    <div className="container mx-auto py-8 space-y-6">
      <div className="space-y-2">
        <h1 className="text-4xl font-bold font-headline flex items-center gap-3">
          <Code2 className="h-10 w-10 text-accent" />
          Monaco Editor Demo
        </h1>
        <p className="text-muted-foreground text-lg">
          LeetCode-style code editor with read-only sections and user-editable zones
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="font-headline">Features Demonstrated</CardTitle>
          <CardDescription>
            This editor showcases all the implemented features for a LeetCode-style coding experience
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div className="space-y-2">
              <h3 className="font-semibold text-accent">✅ Implemented Features</h3>
              <ul className="space-y-1 text-muted-foreground">
                <li>• Monaco Editor with C++ syntax highlighting</li>
                <li>• Read-only function signature and class structure</li>
                <li>• Editable zone marked with comment markers</li>
                <li>• Dark theme (vs-dark)</li>
                <li>• Reset code functionality</li>
                <li>• Extract user-written code only</li>
              </ul>
            </div>
            <div className="space-y-2">
              <h3 className="font-semibold text-yellow-500">ℹ️ Usage Instructions</h3>
              <ul className="space-y-1 text-muted-foreground">
                <li>• Try editing outside the editable zone (prevented)</li>
                <li>• Write your code between USER CODE markers</li>
                <li>• Click "Reset Code" to restore the template</li>
                <li>• Click "Extract User Code" to see your solution</li>
                <li>• Function signature is protected from editing</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Editor Section */}
        <Card>
          <CardHeader>
            <CardTitle className="font-headline">Code Editor</CardTitle>
            <CardDescription>
              Write your solution between the USER CODE START and USER CODE END markers
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="h-[500px]">
                <CodeEditor
                  defaultCode={defaultTemplate}
                  onChange={setCode}
                  onResetTrigger={resetTrigger}
                />
              </div>
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  onClick={handleReset}
                  className="flex-1"
                  data-testid="demo-reset-button"
                >
                  <RefreshCw className="mr-2 h-4 w-4" />
                  Reset Code
                </Button>
                <Button
                  onClick={handleExtractCode}
                  className="flex-1"
                  data-testid="demo-extract-button"
                >
                  <Download className="mr-2 h-4 w-4" />
                  Extract User Code
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Extracted Code Section */}
        <Card>
          <CardHeader>
            <CardTitle className="font-headline">Extracted User Code</CardTitle>
            <CardDescription>
              This shows only the code you wrote, excluding boilerplate
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="bg-secondary/50 rounded-lg p-4 h-[500px] overflow-auto">
                <pre className="text-sm font-code whitespace-pre-wrap">
                  {extractedCode || '// Click "Extract User Code" to see your solution here\n// Only the code between USER CODE markers will appear'}
                </pre>
              </div>
              <div className="text-sm text-muted-foreground">
                <p>📝 This extracted code can be sent to the backend for compilation and testing.</p>
                <p className="mt-2">🔒 Boilerplate code (includes, class definition, function signature) is automatically excluded.</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="border-accent/50">
        <CardHeader>
          <CardTitle className="font-headline">Technical Details</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <h4 className="font-semibold mb-2">Read-Only Enforcement</h4>
            <p className="text-sm text-muted-foreground">
              The editor uses Monaco's decorations API to mark read-only sections. Any attempt to edit
              outside the USER CODE markers is prevented through cursor position tracking and content
              change validation.
            </p>
          </div>
          <div>
            <h4 className="font-semibold mb-2">Code Template Structure</h4>
            <p className="text-sm text-muted-foreground">
              The template follows a standard LeetCode pattern: includes at the top, class definition,
              function signature (all read-only), then the editable zone where users write their logic.
            </p>
          </div>
          <div>
            <h4 className="font-semibold mb-2">Future Enhancements</h4>
            <p className="text-sm text-muted-foreground">
              Backend compilation with Judge0, multi-language support (Python, Java, JavaScript),
              test case validation, and auto-save functionality are planned for future releases.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
