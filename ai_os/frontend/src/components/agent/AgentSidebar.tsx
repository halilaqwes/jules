import React, { useState, useEffect } from 'react';
import { useSocket } from '../../services/socket';
import { Play, Settings, Terminal, Activity } from 'lucide-react';

function AgentLogs() {
    const [logs, setLogs] = useState<string[]>([]);
    const { socket } = useSocket();

    useEffect(() => {
        const handleLog = (data: { agent: string, type: string, content: string }) => {
            setLogs(prev => [...prev, `[${data.type.toUpperCase()}] ${data.content}`].slice(-50));
        };
        socket.on('agent_log', handleLog);
        return () => {
            socket.off('agent_log', handleLog);
        };
    }, [socket]);

    return (
        <div className="flex flex-col gap-1">
            {logs.length === 0 ? "Waiting for task..." : logs.map((log, i) => (
                <div key={i} className="border-b border-gray-800/50 pb-1 mb-1">
                    {log}
                </div>
            ))}
        </div>
    );
}

interface ModelInfo {
    name: string;
    [key: string]: unknown;
}

export const AgentSidebar = React.memo(function AgentSidebar() {
    const { isConnected, socket } = useSocket();
    const [goal, setGoal] = useState('');
    const [models, setModels] = useState<ModelInfo[]>([]);
    const [selectedModel, setSelectedModel] = useState('');

    useEffect(() => {
        fetch('http://localhost:8000/api/models')
            .then(res => res.json())
            .then(data => {
                setModels(data.models || []);
                if (data.models && data.models.length > 0) {
                    setSelectedModel(data.models[0].name);
                }
            })
            .catch(err => console.error("Error fetching models:", err));
    }, []);

    const handleSetGoal = () => {
        socket.emit('set_goal', { goal, model: selectedModel });
    };

    return (
        <div className="flex flex-col h-full w-80 bg-gray-900 border-r border-gray-800 text-gray-300">
            <div className="p-4 border-b border-gray-800 flex items-center justify-between">
                <h2 className="text-sm font-semibold flex items-center gap-2">
                    <Activity size={16} className={isConnected ? "text-green-500" : "text-red-500"} />
                    AI OS Agent {isConnected ? "(Online)" : "(Offline)"}
                </h2>
                <Settings size={16} className="text-gray-500 cursor-pointer hover:text-white" />
            </div>

            <div className="p-4 flex-1 overflow-y-auto">
                <div className="mb-4">
                    <label className="block text-xs text-gray-500 mb-1">Select Local Model</label>
                    <select
                        className="w-full bg-gray-800 border border-gray-700 text-sm rounded p-2 focus:outline-none focus:border-blue-500"
                        value={selectedModel}
                        onChange={(e) => setSelectedModel(e.target.value)}
                    >
                        {models.map(m => (
                            <option key={m.name} value={m.name}>{m.name}</option>
                        ))}
                    </select>
                </div>

                <div className="mb-4">
                    <label className="block text-xs text-gray-500 mb-1">Agent Goal / Task</label>
                    <textarea
                        className="w-full bg-gray-800 border border-gray-700 text-sm rounded p-2 h-32 resize-none focus:outline-none focus:border-blue-500"
                        placeholder="Tell the agent what to do... (e.g. Write a python script to fetch weather)"
                        value={goal}
                        onChange={(e) => setGoal(e.target.value)}
                    />
                </div>

                <button
                    onClick={handleSetGoal}
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium py-2 px-4 rounded flex items-center justify-center gap-2 transition-colors"
                >
                    <Play size={16} />
                    Start Agent Loop
                </button>

                <div className="mt-8 border-t border-gray-800 pt-4 flex-1 flex flex-col min-h-0">
                    <h3 className="text-xs font-semibold text-gray-500 mb-2 uppercase flex items-center gap-2">
                        <Terminal size={14} /> Agent Log
                    </h3>
                    <div className="flex-1 bg-black/50 p-3 rounded overflow-y-auto text-xs font-mono text-green-400 whitespace-pre-wrap">
                        <AgentLogs />
                    </div>
                </div>
            </div>
        </div>
    );
});
