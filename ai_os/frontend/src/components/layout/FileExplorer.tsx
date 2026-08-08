import React, { useState, useEffect } from 'react';
import { Folder, FileCode, File, ChevronRight, ChevronDown } from 'lucide-react';

interface FileNode {
    name: string;
    path: string;
    is_dir: boolean;
    children?: FileNode[];
}

export const FileExplorer = React.memo(function FileExplorer({ onFileSelect }: { onFileSelect: (path: string, content: string) => void }) {
    const [tree, setTree] = useState<FileNode[]>([]);
    const [expanded, setExpanded] = useState<Record<string, boolean>>({});

    const fetchTree = async () => {
        try {
            const res = await fetch('http://localhost:8000/api/files');
            const data = await res.json();
            setTree(data.tree || []);
        } catch (e) {
            console.error(e);
        }
    };

    useEffect(() => {

        fetchTree();
        const interval = setInterval(fetchTree, 5000); // refresh every 5s
        return () => clearInterval(interval);
    }, []);

    const toggleDir = (path: string) => {
        setExpanded(prev => ({ ...prev, [path]: !prev[path] }));
    };

    const handleFileClick = async (path: string) => {
        try {
            const res = await fetch(`http://localhost:8000/api/files/read?path=${encodeURIComponent(path)}`);
            const data = await res.json();
            if (data.content) {
                onFileSelect(path, data.content);
            }
        } catch (e) {
            console.error(e);
        }
    };

    const renderTree = (nodes: FileNode[], level = 0) => {
        return nodes.map(node => (
            <div key={node.path} style={{ paddingLeft: `${level * 12}px` }}>
                <div
                    className="flex items-center gap-1.5 py-1 px-2 hover:bg-gray-800 cursor-pointer text-gray-400 hover:text-white transition-colors text-sm"
                    onClick={() => node.is_dir ? toggleDir(node.path) : handleFileClick(node.path)}
                >
                    {node.is_dir ? (
                        <>
                            {expanded[node.path] ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                            <Folder size={14} className="text-blue-400" />
                        </>
                    ) : (
                        <>
                            <span className="w-3.5" /> {/* spacing spacer */}
                            {node.name.endsWith('.py') || node.name.endsWith('.ts') ?
                                <FileCode size={14} className="text-green-400" /> :
                                <File size={14} />
                            }
                        </>
                    )}
                    <span className="truncate">{node.name}</span>
                </div>
                {node.is_dir && expanded[node.path] && node.children && (
                    <div>{renderTree(node.children, level + 1)}</div>
                )}
            </div>
        ));
    };

    return (
        <div className="w-64 h-full bg-[#18181b] border-r border-gray-800 flex flex-col">
            <div className="p-3 border-b border-gray-800 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                Explorer
            </div>
            <div className="flex-1 overflow-y-auto p-2">
                {tree.length === 0 ? (
                    <div className="text-xs text-gray-600 text-center mt-4">Workspace is empty</div>
                ) : (
                    renderTree(tree)
                )}
            </div>
        </div>
    );
});
