import { AgentSidebar } from '../agent/AgentSidebar';
import { CodeEditor } from '../editor/CodeEditor';
import { ChatPanel } from '../chat/ChatPanel';
import { useState, useEffect } from 'react';

// ⚡ Bolt: Extracted Workspace component to isolate high-frequency state
// What: Moved the 'code' state and CodeEditor out of MainLayout
// Why: Prevent MainLayout (and sibling Chat/Agent panels) from re-rendering on every keystroke
// Impact: Reduces re-renders significantly and makes the editor feel more responsive
function Workspace() {
    const [code, setCode] = useState<string>('# Welcome to AI OS\n# Select a file or ask the agent to write code.');

    return (
        <div className="flex-1 flex flex-col min-w-0 border-r border-gray-800">
            <div className="h-10 bg-[#1e1e1e] border-b border-gray-800 flex items-center px-4 text-xs text-gray-400">
                <span>workspace / main.py</span>
            </div>
            <div className="flex-1 relative">
                <CodeEditor fileContent={code} onChange={(v) => setCode(v || '')} />
            </div>
        </div>
    );
}

export function MainLayout() {
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

    return (
        <div className="flex h-screen w-screen bg-black overflow-hidden font-sans">
            <AgentSidebar />
            <Workspace />
            <ChatPanel selectedModel={selectedModel} />
        </div>
    );
}
