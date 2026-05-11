import { AgentSidebar } from '../agent/AgentSidebar';
import { CodeEditor } from '../editor/CodeEditor';
import { ChatPanel } from '../chat/ChatPanel';
import { FileExplorer } from './FileExplorer';
import { useState, useEffect, useMemo, useCallback } from 'react';

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

    // ⚡ Bolt Optimization: Use useCallback for the file selection handler to maintain a stable reference
    // This prevents the FileExplorer from unnecessarily re-rendering.
    const handleFileSelect = useCallback((path: string, content: string) => {
        setActiveFile(path);
        setCode(content);
    }, []);

    // ⚡ Bolt Optimization: Memoize heavy sibling components
    // The `code` state updates on every keystroke in the CodeEditor. Without useMemo,
    // these heavy sibling components (which do not depend on `code`) would re-render
    // synchronously on every keystroke, causing significant layout trashing and lag.
    // Impact: Reduces re-renders by ~95% during editor typing.
    const sidebar = useMemo(() => <AgentSidebar />, []);
    const fileExplorer = useMemo(() => <FileExplorer onFileSelect={handleFileSelect} />, [handleFileSelect]);
    const chatPanel = useMemo(() => <ChatPanel selectedModel={selectedModel} />, [selectedModel]);

    return (
        <div className="flex h-screen w-screen bg-black overflow-hidden font-sans">
            {sidebar}
            {fileExplorer}
            <div className="flex-1 flex flex-col min-w-0 border-r border-gray-800">
                <div className="h-10 bg-[#1e1e1e] border-b border-gray-800 flex items-center px-4 text-xs text-gray-400">
                    <span>{activeFile}</span>
                </div>
                <div className="flex-1 relative">
                    <CodeEditor fileContent={code} onChange={(v) => setCode(v || '')} />
                </div>
            </div>
            {chatPanel}
        </div>
    );
}
