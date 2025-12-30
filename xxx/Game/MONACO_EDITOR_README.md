# LeetCode-Style Monaco Editor Implementation

## Overview
This document explains the implementation of a LeetCode-style code editor using Monaco Editor in the CodeDuel Arena application. The editor provides a professional coding experience with syntax highlighting, read-only sections, and user-friendly features.

## Design Architecture

### Core Components

#### 1. **CodeEditor Component** (`/frontend/src/components/CodeEditor.tsx`)
The main component that wraps Monaco Editor with custom functionality.

**Key Features:**
- Monaco Editor integration with C++ syntax highlighting
- Dark theme (vs-dark)
- Read-only region enforcement
- Comment-based editable zones
- Code extraction functionality
- Reset capability

#### 2. **Practice Problem Page Integration** (`/frontend/src/app/(app)/practice/[problemId]/page.tsx`)
Updated to use the Monaco Editor instead of a simple textarea.

### Code Template Structure

The editor uses a structured C++ template with clearly marked editable regions:

```cpp
#include <vector>
using namespace std;

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        // USER CODE START
        // Write your solution here
        
        // USER CODE END
    }
};
```

**Template Components:**
- **Read-Only Header**: Includes, namespace declarations
- **Read-Only Class Structure**: Class declaration and function signature
- **Editable Zone**: Between `// USER CODE START` and `// USER CODE END` markers
- **Read-Only Footer**: Closing braces and boilerplate

## Technical Implementation

### 1. Read-Only Region Enforcement

The editor uses Monaco's decorations API to mark and enforce read-only regions:

```typescript
// Apply decorations to mark read-only sections
const decorations: monaco.editor.IModelDeltaDecoration[] = [];

// Make everything before USER CODE START read-only
decorations.push({
  range: new monaco.Range(1, 1, range.start, 1),
  options: {
    isWholeLine: true,
    className: 'read-only-line',
    glyphMarginClassName: 'read-only-glyph',
    hoverMessage: { value: '🔒 This section is read-only' },
  },
});
```

### 2. Edit Prevention

Two-layer protection prevents editing in read-only zones:

**Layer 1: Cursor Position Control**
```typescript
editor.onDidChangeCursorPosition((e) => {
  const position = e.position;
  if (editableRange) {
    const line = position.lineNumber;
    if (line < editableRange.start || line >= editableRange.end) {
      // Move cursor back to editable region
      editor.setPosition({ lineNumber: editableRange.start + 1, column: 1 });
    }
  }
});
```

**Layer 2: Content Change Validation**
```typescript
editor.onDidChangeModelContent((e) => {
  for (const change of e.changes) {
    const startLine = change.range.startLineNumber;
    const endLine = change.range.endLineNumber;
    
    if (startLine < range.start || endLine >= range.end) {
      // Revert invalid changes
      model.setValue(code);
      return;
    }
  }
});
```

### 3. User Code Extraction

The `extractUserCode()` function retrieves only the code written by the user:

```typescript
const extractUserCode = (): string => {
  const lines = code.split('\n');
  const range = findEditableRange(code);
  
  if (!range) return '';
  
  // Extract lines between markers (exclusive of marker lines)
  return lines.slice(range.start, range.end - 1).join('\n').trim();
};
```

### 4. Reset Functionality

The reset feature clears both code and output:

```typescript
const handleResetCode = () => {
  // Increment reset trigger to notify CodeEditor
  setResetTrigger(prev => prev + 1);
  
  // Reset output display
  setOutput({ 
    status: 'initial', 
    message: 'Run your code to see the output here.' 
  });
};
```

## Features Implemented

### ✅ Monaco Editor Integration
- Professional code editor with IntelliSense
- Syntax highlighting for C++
- Line numbers and minimap
- Auto-indentation and bracket matching

### ✅ Read-Only Sections
- Function signature is protected
- Class structure is non-editable
- Includes and namespace declarations are locked
- Visual feedback with gray background

### ✅ Editable User Zone
- Clearly marked with comment markers
- Users can only edit between markers
- Maintains proper indentation
- Cursor automatically positioned in editable area

### ✅ Reset Code Button
- Restores original template
- Clears execution output
- Repositions cursor to editable area
- Single-click operation

### ✅ Dark Theme
- Professional dark theme (vs-dark)
- Consistent with modern coding environments
- Reduces eye strain
- Syntax-aware color highlighting

### ✅ Code Extraction
- Function to get only user-written code
- Excludes boilerplate and markers
- Ready for backend submission
- Clean trimmed output

## Usage Example

### For Developers Adding New Problems

To create a new problem with the editor:

```typescript
// 1. Create template using helper function
import { createCppTemplate } from '@/components/CodeEditor';

const template = createCppTemplate(
  'Two Sum',
  'vector<int> twoSum(vector<int>& nums, int target)'
);

// 2. Use in your page
<CodeEditor
  defaultCode={template}
  onChange={(code) => setCode(code)}
  onResetTrigger={resetTrigger}
/>

// 3. Extract user code when submitting
const userCode = extractUserCode();
// Submit userCode to backend for evaluation
```

### For Users

1. **Navigate** to any practice problem
2. **View** the problem description on the left
3. **Write** your solution in the editable zone (between comment markers)
4. **Run** to test your code
5. **Reset** if you want to start over (clears both code and output)
6. **Submit** when ready

## Configuration

### Monaco Editor Options

Current configuration in `CodeEditor.tsx`:

```typescript
options={{
  minimap: { enabled: true },          // Shows code overview
  fontSize: 14,                        // Readable font size
  lineNumbers: 'on',                   // Show line numbers
  scrollBeyondLastLine: false,         // Prevent excessive scrolling
  automaticLayout: true,               // Auto-resize with container
  tabSize: 4,                          // 4 spaces per tab
  wordWrap: 'on',                      // Wrap long lines
  glyphMargin: true,                   // Show glyph margin for decorations
  folding: true,                       // Allow code folding
  renderWhitespace: 'selection',       // Show whitespace when selected
}}
```

## Future Enhancements

### Planned Features (Not Yet Implemented)
1. **Multi-language Support**: Python, Java, JavaScript
2. **Backend Compilation**: Integration with Judge0 or similar
3. **Test Case Validation**: Real-time execution
4. **Code Templates**: Multiple templates per problem
5. **Auto-save**: Persist code in localStorage
6. **Themes**: Light theme option
7. **Font Customization**: User preference settings
8. **Keyboard Shortcuts**: Custom shortcuts for run/submit

## Testing

### Manual Testing Checklist
- ✅ Editor loads with correct template
- ✅ Read-only sections cannot be edited
- ✅ User can type in editable zone
- ✅ Reset button works correctly
- ✅ Dark theme is applied
- ✅ Syntax highlighting works
- ✅ No console errors
- ✅ Responsive layout

### Test Scenarios
1. Try to edit function signature → Should be prevented
2. Type code in editable zone → Should work normally
3. Click Reset → Should restore template and clear output
4. Navigate between lines → Cursor should stay in editable zone
5. Copy/paste → Should work within editable zone

## Technical Stack

- **Monaco Editor**: v0.55.1
- **@monaco-editor/react**: v4.7.0
- **React**: v18.3.1
- **Next.js**: v15.3.3
- **TypeScript**: v5.x

## Dependencies Added

```json
{
  "monaco-editor": "^0.55.1",
  "@monaco-editor/react": "^4.7.0"
}
```

## Known Limitations

1. **C++ Only**: Currently only C++ syntax is supported
2. **No Compilation**: Code execution is mocked (not actually compiled)
3. **Single Template**: Each problem uses the same template structure
4. **SSR Issues**: Editor must be loaded client-side with `dynamic` import

## Performance Considerations

- Editor is dynamically imported to avoid SSR issues
- Loading state shown while editor initializes
- Automatic layout handles container resizing
- Efficient decoration updates using refs

## Browser Compatibility

- ✅ Chrome/Edge (Chromium)
- ✅ Firefox
- ✅ Safari
- ⚠️ IE11 (Not supported)

## Conclusion

This implementation provides a solid foundation for a LeetCode-style coding experience. The editor successfully enforces code structure while giving users the flexibility to write their solutions. The clean separation between editable and read-only sections makes it clear where users should focus their efforts.

The architecture is designed to be extensible, making it straightforward to add support for additional programming languages and more sophisticated features in the future.
