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

    // Memoize the callback to avoid re-rendering FileExplorer
    const handleFileSelect = useCallback((path: string, content: string) => {
        setActiveFile(path);
        setCode(content);
    }, []);

    // Memoize the onChange callback to avoid re-rendering CodeEditor unnecessarily
    const handleCodeChange = useCallback((v: string | undefined) => {
        setCode(v || '');
    }, []);

    // Wrap heavy sibling components in useMemo to prevent them from re-rendering
    // on every keystroke when typing in CodeEditor, since `code` state updates MainLayout.
    const agentSidebar = useMemo(() => <AgentSidebar />, []);
    const fileExplorer = useMemo(() => <FileExplorer onFileSelect={handleFileSelect} />, [handleFileSelect]);
    const chatPanel = useMemo(() => <ChatPanel selectedModel={selectedModel} />, [selectedModel]);

    return (
        <div className="flex h-screen w-screen bg-black overflow-hidden font-sans">
            {agentSidebar}
            {fileExplorer}
            <div className="flex-1 flex flex-col min-w-0 border-r border-gray-800">
                <div className="h-10 bg-[#1e1e1e] border-b border-gray-800 flex items-center px-4 text-xs text-gray-400">
                    <span>{activeFile}</span>
                </div>
                <div className="flex-1 relative">
                    <CodeEditor fileContent={code} onChange={handleCodeChange} />
                </div>
            </div>
            {chatPanel}
        </div>
    );
}
