import { useState, useEffect, useRef, memo } from 'react';
import { useSocket } from '../../services/socket';
import { Send, Bot, User, Loader } from 'lucide-react';

interface ChatMessage {
    role: 'user' | 'agent';
    content: string;
}

// ⚡ Bolt: Wrapped in React.memo() to prevent unnecessary re-renders
// when the parent MainLayout's state (e.g. editor keystrokes) changes.
export const ChatPanel = memo(function ChatPanel({ selectedModel }: { selectedModel: string }) {
    const { isConnected, socket } = useSocket();
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [input, setInput] = useState('');
    const [isThinking, setIsThinking] = useState(false);
    const endOfMessagesRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const handleReply = (data: { message: string }) => {
            setMessages(prev => [...prev, { role: 'agent', content: data.message }]);
            setIsThinking(false);
        };
        const handleStatus = (data: { status: string }) => {
            if (data.status === 'thinking') setIsThinking(true);
        };

        socket.on('chat_reply', handleReply);
        socket.on('chat_status', handleStatus);

        return () => {
            socket.off('chat_reply', handleReply);
            socket.off('chat_status', handleStatus);
        };
    }, [socket]);

    useEffect(() => {
        endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, isThinking]);

    const handleSend = () => {
        if (!input.trim() || !isConnected) return;

        const text = input.trim();
        setMessages(prev => [...prev, { role: 'user', content: text }]);
        setInput('');
        socket.emit('chat_message', { message: text, model: selectedModel });
    };

    return (
        <div className="flex flex-col h-full w-96 bg-[#18181b] border-l border-gray-800 text-gray-300">
            <div className="p-3 border-b border-gray-800 flex items-center justify-between bg-[#1e1e2e]">
                <h2 className="text-sm font-semibold flex items-center gap-2 text-white">
                    <Bot size={16} className="text-blue-400" /> AI Assistant
                </h2>
                <span className="text-xs text-gray-500">{selectedModel || 'No Model'}</span>
            </div>

            <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-4">
                {messages.length === 0 && (
                    <div className="text-center text-gray-500 text-sm mt-10">
                        Ask me anything, or instruct me to build something!
                    </div>
                )}
                {messages.map((msg, idx) => (
                    <div key={idx} className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 ${msg.role === 'user' ? 'bg-blue-600' : 'bg-gray-700'}`}>
                            {msg.role === 'user' ? <User size={14} className="text-white" /> : <Bot size={14} className="text-blue-400" />}
                        </div>
                        <div className={`text-sm p-3 rounded-lg max-w-[80%] whitespace-pre-wrap ${msg.role === 'user' ? 'bg-blue-600 text-white rounded-tr-none' : 'bg-gray-800 text-gray-200 rounded-tl-none'}`}>
                            {msg.content}
                        </div>
                    </div>
                ))}
                {isThinking && (
                    <div className="flex gap-3">
                        <div className="w-8 h-8 rounded-full flex items-center justify-center shrink-0 bg-gray-700">
                            <Loader size={14} className="text-blue-400 animate-spin" />
                        </div>
                        <div className="text-sm p-3 rounded-lg bg-gray-800 text-gray-400 rounded-tl-none flex items-center gap-2">
                            Thinking...
                        </div>
                    </div>
                )}
                <div ref={endOfMessagesRef} />
            </div>

            <div className="p-4 border-t border-gray-800 bg-[#1e1e2e]">
                <div className="relative">
                    <textarea
                        className="w-full bg-gray-900 border border-gray-700 text-sm rounded-lg p-3 pr-10 resize-none focus:outline-none focus:border-blue-500 text-white placeholder-gray-500"
                        placeholder="Message the AI..."
                        rows={3}
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                                e.preventDefault();
                                handleSend();
                            }
                        }}
                    />
                    <button
                        onClick={handleSend}
                        disabled={!isConnected || !input.trim() || isThinking}
                        className="absolute right-2 bottom-2 p-2 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 disabled:cursor-not-allowed rounded-md text-white transition-colors"
                    >
                        <Send size={14} />
                    </button>
                </div>
                <div className="text-center mt-2 text-[10px] text-gray-500">
                    Use Shift + Enter for new line
                </div>
            </div>
        </div>
    );
});
