import Editor from '@monaco-editor/react';
import React from 'react';

interface CodeEditorProps {
    fileContent: string;
    language?: string;
    onChange?: (value: string | undefined) => void;
}

// ⚡ Bolt Performance Optimization: Added React.memo to prevent unnecessary re-renders when MainLayout state changes
export const CodeEditor = React.memo(function CodeEditor({ fileContent, language = 'python', onChange }: CodeEditorProps) {
    return (
        <div className="h-full w-full bg-[#1e1e1e]">
            <Editor
                height="100%"
                theme="vs-dark"
                language={language}
                value={fileContent}
                onChange={onChange}
                options={{
                    minimap: { enabled: false },
                    fontSize: 14,
                    wordWrap: 'on',
                    padding: { top: 16 }
                }}
            />
        </div>
    );
});
