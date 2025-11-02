"use client";

import { useRouter } from "next/navigation";
import { AppSidebar } from "@/components/app-sidebar";
import { SidebarProvider } from "@/components/ui/sidebar";
import { ChatHistory } from "@/components/chat-history";
import { touchSession } from "@/lib/sessions";

export default function HistoryPage() {
  const router = useRouter();

  const handleNewChat = () => {
    router.push("/");
  };

  const handleToggleHistory = () => {
    router.push("/history");
  };

  const handleSelectSession = (sessionId: string) => {
    // Resume the selected session
    touchSession(sessionId);
    // Navigate to the chat page with the session_id
    router.push(`/chat/${sessionId}`);
  };

  return (
    <SidebarProvider>
      <div className="flex min-h-screen w-full">
        <AppSidebar
          onNewChat={handleNewChat}
          onToggleHistory={handleToggleHistory}
        />
        <main className="flex-1 flex flex-col bg-zinc-50 dark:bg-zinc-900">
          {/* History content */}
          <ChatHistory onSelectSession={handleSelectSession} />
        </main>
      </div>
    </SidebarProvider>
  );
}
