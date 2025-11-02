"use client";

import { useEffect, useState } from "react";
import { loadSessions, removeSession, type ChatSession } from "@/lib/sessions";
import { Button } from "@/components/ui/button";
import { Trash2 } from "lucide-react";

type ChatHistoryProps = {
  onSelectSession: (sessionId: string) => void;
};

export function ChatHistory({ onSelectSession }: ChatHistoryProps) {
  const [sessions, setSessions] = useState<ChatSession[]>([]);

  useEffect(() => {
    // Load sessions on mount
    setSessions(loadSessions());
  }, []);

  const handleDelete = (sessionId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    removeSession(sessionId);
    setSessions(loadSessions());
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return "Just now";
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className="flex-1 overflow-y-auto p-4">
      <h2 className="text-lg font-semibold mb-4">Chat History</h2>
      {sessions.length === 0 ? (
        <p className="text-sm text-muted-foreground">No chat history yet</p>
      ) : (
        <div className="space-y-2">
          {sessions.map((session) => (
            <div
              key={session.id}
              className="group flex items-center gap-2 p-3 rounded-lg border bg-card hover:bg-accent cursor-pointer transition-colors"
              onClick={() => onSelectSession(session.id)}
            >
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">{session.title}</p>
                <p className="text-xs text-muted-foreground">
                  {formatDate(session.lastUsedAt)}
                </p>
              </div>
              <Button
                variant="ghost"
                size="icon"
                className="opacity-0 group-hover:opacity-100 transition-opacity"
                onClick={(e) => handleDelete(session.id, e)}
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
