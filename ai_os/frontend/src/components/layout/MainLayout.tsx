import { AgentSidebar } from '../agent/AgentSidebar';
import { CodeEditor } from '../editor/CodeEditor';
import { useState } from 'react';

export function MainLayout() {
    const [code, setCode] = useState<string>('# Welcome to AI OS\n# Select a file or ask the agent to write code.');

    return (
        <div className="flex h-screen w-screen bg-black overflow-hidden font-sans">
            <AgentSidebar />
            <div className="flex-1 flex flex-col min-w-0">
                <div className="h-10 bg-[#1e1e1e] border-b border-gray-800 flex items-center px-4 text-xs text-gray-400">
                    <span>workspace / main.py</span>
                </div>
                <div className="flex-1 relative">
                    <CodeEditor fileContent={code} onChange={(v) => setCode(v || '')} />
                </div>
            </div>
        </div>
    );
}
