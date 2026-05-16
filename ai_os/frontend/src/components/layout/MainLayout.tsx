import { AgentSidebar } from '../agent/AgentSidebar';
import { CodeEditor } from '../editor/CodeEditor';
import { ChatPanel } from '../chat/ChatPanel';
import { FileExplorer } from './FileExplorer';
import { useState, useEffect, useCallback, useMemo } from 'react';

export function MainLayout() {
    const [code, setCode] = useState<string>('# Welcome to AI OS\n# Select a file or ask the agent to write code.');
    const [activeFile, setActiveFile] = useState<string>('workspace / main.py');
    const [selectedModel, setSelectedModel] = useState<string>('qwen2.5:latest');

    // We can fetch models here so both sidebar and chat know about it,
    // but for now, we'll let AgentSidebar update this state if we lift it up.
    // For simplicity, we'll fetch it here to pass to chat.
    useEffect(() => {
        fetch('http://localhost:8000/api/models')
            .then(res => res.json())
            .then(data => {
                if (data.models && data.models.length > 0) {
                    setSelectedModel(data.models[0].name);
                }
            })
            .catch(err => console.error(err));
    }, []);

    // ⚡ Bolt Performance Optimization:
    // Memoize the callback to prevent FileExplorer from re-rendering
    // every time the code state changes.
    const handleFileSelect = useCallback((path: string, content: string) => {
        setActiveFile(path);
        setCode(content);
    }, []);

    // ⚡ Bolt Performance Optimization:
    // Memoize heavy sibling components. Since the 'code' state is lifted
    // to MainLayout to power the CodeEditor, typing in the editor triggers
    // a re-render of this entire component on every keystroke. By memoizing
    // these heavy sidebars, we prevent severe layout thrashing and unnecessary
    // reconciliation, resulting in a much snappier typing experience.
    const memoizedSidebar = useMemo(() => <AgentSidebar />, []);
    const memoizedExplorer = useMemo(() => <FileExplorer onFileSelect={handleFileSelect} />, [handleFileSelect]);
    const memoizedChat = useMemo(() => <ChatPanel selectedModel={selectedModel} />, [selectedModel]);

    return (
        <div className="flex h-screen w-screen bg-black overflow-hidden font-sans">
            {memoizedSidebar}
            {memoizedExplorer}
            <div className="flex-1 flex flex-col min-w-0 border-r border-gray-800">
                <div className="h-10 bg-[#1e1e1e] border-b border-gray-800 flex items-center px-4 text-xs text-gray-400">
                    <span>{activeFile}</span>
                </div>
                <div className="flex-1 relative">
                    <CodeEditor fileContent={code} onChange={(v) => setCode(v || '')} />
                </div>
            </div>
            {memoizedChat}
        </div>
    );
}
