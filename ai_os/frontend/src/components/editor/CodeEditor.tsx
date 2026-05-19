import Editor from '@monaco-editor/react';
import { memo } from 'react';

interface CodeEditorProps {
    fileContent: string;
    language?: string;
    onChange?: (value: string | undefined) => void;
}

// ⚡ Bolt: Wrapped CodeEditor in React.memo to prevent unnecessary re-renders
// It now only re-renders when its content actually changes, saving resources.
export const CodeEditor = memo(function CodeEditor({ fileContent, language = 'python', onChange }: CodeEditorProps) {
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
