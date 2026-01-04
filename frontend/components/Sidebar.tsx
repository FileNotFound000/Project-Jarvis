import { useState, useEffect, useRef } from "react";
import { MessageSquare, Plus, Trash2, X, Pencil, Check, Settings } from "lucide-react";
import SettingsModal from "./SettingsModal";

interface Session {
    id: string;
    title: string;
    created_at: string;
}

interface SidebarProps {
    sessions: Session[];
    currentSessionId: string | null;
    onSessionSelect: (sessionId: string) => void;
    onNewChat: () => void;
    onDeleteSession: (sessionId: string) => void;
    onRenameSession: (sessionId: string, newTitle: string) => void;
    isOpen: boolean;
    setIsOpen: (isOpen: boolean) => void;
}

export default function Sidebar({
    sessions,
    currentSessionId,
    onSessionSelect,
    onNewChat,
    onDeleteSession,
    onRenameSession,
    isOpen,
    setIsOpen
}: SidebarProps) {
    const [editingSessionId, setEditingSessionId] = useState<string | null>(null);
    const [editTitle, setEditTitle] = useState("");
    const inputRef = useRef<HTMLInputElement>(null);

    useEffect(() => {
        if (editingSessionId && inputRef.current) {
            inputRef.current.focus();
        }
    }, [editingSessionId]);

    const handleDeleteClick = (e: React.MouseEvent, sessionId: string) => {
        e.stopPropagation();
        if (confirm("Are you sure you want to delete this chat?")) {
            onDeleteSession(sessionId);
        }
    };

    const startEditing = (e: React.MouseEvent, session: Session) => {
        e.stopPropagation();
        setEditingSessionId(session.id);
        setEditTitle(session.title);
    };

    const saveTitle = () => {
        if (editingSessionId && editTitle.trim()) {
            onRenameSession(editingSessionId, editTitle.trim());
            setEditingSessionId(null);
        } else {
            setEditingSessionId(null);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === "Enter") {
            saveTitle();
        } else if (e.key === "Escape") {
            setEditingSessionId(null);
        }
    };

    const [isSettingsOpen, setIsSettingsOpen] = useState(false);

    // ... (existing code)

    return (
        <>
            <SettingsModal isOpen={isSettingsOpen} onClose={() => setIsSettingsOpen(false)} />

            {/* Mobile Overlay */}
            {isOpen && (
                <div
                    className="fixed inset-0 z-30 bg-black/50 backdrop-blur-sm md:hidden"
                    onClick={() => setIsOpen(false)}
                />
            )}

            {/* Sidebar */}
            <div className={`fixed md:static inset-y-0 left-0 z-40 w-64 bg-black/40 backdrop-blur-xl border-r border-white/10 transform transition-transform duration-300 ease-in-out ${isOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
                }`}>
                <div className="flex flex-col h-full p-4">
                    <div className="flex items-center justify-between mb-6">
                        <h2 className="text-lg font-bold text-violet-100 tracking-wider">HISTORY</h2>
                        <button
                            onClick={() => setIsOpen(false)}
                            className="md:hidden text-violet-400 hover:text-white"
                        >
                            <X size={20} />
                        </button>
                    </div>

                    <button
                        onClick={() => {
                            onNewChat();
                            if (window.innerWidth < 768) setIsOpen(false);
                        }}
                        className="flex items-center gap-2 w-full p-3 mb-4 rounded-xl bg-violet-600/20 hover:bg-violet-600/30 border border-violet-500/30 text-violet-100 transition-all group"
                    >
                        <Plus size={18} className="group-hover:rotate-90 transition-transform" />
                        <span className="font-medium text-sm">New Chat</span>
                    </button>

                    <div className="flex-1 overflow-y-auto space-y-2 scrollbar-thin scrollbar-thumb-white/10">
                        {sessions.map((session) => (
                            <div
                                key={session.id}
                                onClick={() => {
                                    if (editingSessionId !== session.id) {
                                        onSessionSelect(session.id);
                                        if (window.innerWidth < 768) setIsOpen(false);
                                    }
                                }}
                                className={`group flex items-center justify-between p-3 rounded-lg cursor-pointer transition-all ${currentSessionId === session.id
                                    ? "bg-white/10 text-white border border-white/10"
                                    : "text-violet-300/70 hover:bg-white/5 hover:text-violet-100"
                                    }`}
                            >
                                <div className="flex items-center gap-3 overflow-hidden flex-1 min-w-0">
                                    <MessageSquare size={16} className={`flex-shrink-0 ${currentSessionId === session.id ? "text-violet-400" : "opacity-50"}`} />

                                    {editingSessionId === session.id ? (
                                        <input
                                            ref={inputRef}
                                            type="text"
                                            value={editTitle}
                                            onChange={(e) => setEditTitle(e.target.value)}
                                            onBlur={saveTitle}
                                            onKeyDown={handleKeyDown}
                                            onClick={(e) => e.stopPropagation()}
                                            className="bg-black/50 text-white text-sm px-1 py-0.5 rounded border border-violet-500/50 outline-none w-full"
                                        />
                                    ) : (
                                        <span className="text-sm truncate">{session.title}</span>
                                    )}
                                </div>

                                {editingSessionId !== session.id && (
                                    <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                                        <button
                                            onClick={(e) => startEditing(e, session)}
                                            className="p-1 hover:text-violet-300 transition-colors"
                                            title="Rename"
                                        >
                                            <Pencil size={14} />
                                        </button>
                                        <button
                                            onClick={(e) => handleDeleteClick(e, session.id)}
                                            className="p-1 hover:text-red-400 transition-colors"
                                            title="Delete"
                                        >
                                            <Trash2 size={14} />
                                        </button>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>

                    {/* Settings Button */}
                    <div className="mt-4 pt-4 border-t border-white/10">
                        <button
                            onClick={() => setIsSettingsOpen(true)}
                            className="flex items-center gap-3 w-full p-3 rounded-lg text-violet-300/70 hover:bg-white/5 hover:text-violet-100 transition-all"
                        >
                            <Settings size={18} />
                            <span className="font-medium text-sm">Settings</span>
                        </button>
                    </div>
                </div>
            </div>
        </>
    );
}
