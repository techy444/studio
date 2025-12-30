"use client";

import React, { useRef, useEffect, useState } from 'react';
import Editor, { OnMount } from '@monaco-editor/react';
import * as monaco from 'monaco-editor';

interface CodeEditorProps {
  defaultCode: string;
  onChange?: (code: string) => void;
  onResetTrigger?: number; // Trigger reset when this changes
}

export const CodeEditor: React.FC<CodeEditorProps> = ({ 
  defaultCode, 
  onChange,
  onResetTrigger 
}) => {
  const editorRef = useRef<monaco.editor.IStandaloneCodeEditor | null>(null);
  const [code, setCode] = useState(defaultCode);
  const [editableRange, setEditableRange] = useState<{ start: number; end: number } | null>(null);
  const decorationsRef = useRef<string[]>([]);

  // Reset code when trigger changes
  useEffect(() => {
    if (onResetTrigger !== undefined && onResetTrigger > 0) {
      handleReset();
    }
  }, [onResetTrigger]);

  // Find editable region from code
  const findEditableRange = (codeContent: string) => {
    const lines = codeContent.split('\n');
    let startLine = -1;
    let endLine = -1;

    lines.forEach((line, index) => {
      if (line.trim().includes('// USER CODE START')) {
        startLine = index + 1; // Line after the marker
      }
      if (line.trim().includes('// USER CODE END')) {
        endLine = index + 1; // Line with the marker
      }
    });

    if (startLine !== -1 && endLine !== -1 && startLine < endLine) {
      return { start: startLine, end: endLine };
    }
    return null;
  };

  // Apply read-only decorations
  const applyReadOnlyDecorations = (editor: monaco.editor.IStandaloneCodeEditor) => {
    const model = editor.getModel();
    if (!model) return;

    const range = findEditableRange(model.getValue());
    setEditableRange(range);

    if (!range) return;

    const totalLines = model.getLineCount();
    const decorations: monaco.editor.IModelDeltaDecoration[] = [];

    // Make everything before USER CODE START read-only
    if (range.start > 1) {
      decorations.push({
        range: new monaco.Range(1, 1, range.start, 1),
        options: {
          isWholeLine: true,
          className: 'read-only-line',
          glyphMarginClassName: 'read-only-glyph',
          hoverMessage: { value: '🔒 This section is read-only' },
        },
      });
    }

    // Make everything after USER CODE END read-only
    if (range.end <= totalLines) {
      decorations.push({
        range: new monaco.Range(range.end, 1, totalLines, model.getLineMaxColumn(totalLines)),
        options: {
          isWholeLine: true,
          className: 'read-only-line',
          glyphMarginClassName: 'read-only-glyph',
          hoverMessage: { value: '🔒 This section is read-only' },
        },
      });
    }

    decorationsRef.current = editor.deltaDecorations(decorationsRef.current, decorations);
  };

  // Handle editor mount
  const handleEditorDidMount: OnMount = (editor, monaco) => {
    editorRef.current = editor;

    // Apply custom styling for read-only sections
    const style = document.createElement('style');
    style.innerHTML = `
      .read-only-line {
        background-color: rgba(100, 100, 100, 0.1);
        opacity: 0.7;
      }
      .read-only-glyph {
        background-color: rgba(255, 0, 0, 0.2);
      }
    `;
    document.head.appendChild(style);

    // Apply decorations
    applyReadOnlyDecorations(editor);

    // Prevent editing in read-only zones
    editor.onDidChangeCursorPosition((e) => {
      const position = e.position;
      if (editableRange) {
        const line = position.lineNumber;
        // If cursor is outside editable range, move it to the start of editable range
        if (line < editableRange.start || line >= editableRange.end) {
          editor.setPosition({ lineNumber: editableRange.start + 1, column: 1 });
        }
      }
    });

    // Intercept content changes to prevent editing read-only areas
    editor.onDidChangeModelContent((e) => {
      const model = editor.getModel();
      if (!model) return;

      const currentCode = model.getValue();
      const range = findEditableRange(currentCode);

      if (!range) return;

      // Check if any change happened outside the editable range
      for (const change of e.changes) {
        const startLine = change.range.startLineNumber;
        const endLine = change.range.endLineNumber;

        if (startLine < range.start || endLine >= range.end) {
          // Revert the change
          model.setValue(code);
          return;
        }
      }

      // Valid change in editable region
      setCode(currentCode);
      onChange?.(currentCode);
    });

    // Set initial cursor position in editable area
    if (editableRange) {
      editor.setPosition({ lineNumber: editableRange.start + 1, column: 1 });
    }
  };

  // Extract only user-written code
  const extractUserCode = (): string => {
    const lines = code.split('\n');
    const range = findEditableRange(code);

    if (!range) return '';

    // Extract lines between markers (exclusive of marker lines)
    return lines.slice(range.start, range.end - 1).join('\n').trim();
  };

  // Handle reset
  const handleReset = () => {
    setCode(defaultCode);
    if (editorRef.current) {
      editorRef.current.setValue(defaultCode);
      applyReadOnlyDecorations(editorRef.current);
      const range = findEditableRange(defaultCode);
      if (range) {
        editorRef.current.setPosition({ lineNumber: range.start + 1, column: 1 });
      }
    }
    onChange?.(defaultCode);
  };

  // Expose extract method via ref (can be called from parent)
  useEffect(() => {
    if (editorRef.current) {
      // Store extract function on editor instance for parent access
      (editorRef.current as any).extractUserCode = extractUserCode;
    }
  }, [code]);

  return (
    <div className="h-full w-full border rounded-lg overflow-hidden">
      <Editor
        height="100%"
        defaultLanguage="cpp"
        value={code}
        theme="vs-dark"
        options={{
          minimap: { enabled: true },
          fontSize: 14,
          lineNumbers: 'on',
          roundedSelection: false,
          scrollBeyondLastLine: false,
          automaticLayout: true,
          tabSize: 4,
          wordWrap: 'on',
          glyphMargin: true,
          folding: true,
          lineDecorationsWidth: 10,
          lineNumbersMinChars: 3,
          renderWhitespace: 'selection',
          scrollbar: {
            vertical: 'visible',
            horizontal: 'visible',
            useShadows: false,
          },
        }}
        onMount={handleEditorDidMount}
      />
    </div>
  );
};

// Export helper to create default template
export const createCppTemplate = (problemTitle: string = 'Two Sum', functionSignature: string = 'vector<int> twoSum(vector<int>& nums, int target)'): string => {
  return `#include <vector>
using namespace std;

class Solution {
public:
    ${functionSignature} {
        // USER CODE START
        // Write your solution here
        
        // USER CODE END
    }
};`;
};

export default CodeEditor;
