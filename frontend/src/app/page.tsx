"use client";

/**
 * Landing page for new chats
 * Redirects to /chat/{session_id} on first message
 */

import { useState } from "react";
import { useRouter } from "next/navigation";
import { AppSidebar } from "@/components/app-sidebar";
import { SidebarProvider } from "@/components/ui/sidebar";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { ArrowUpIcon, Loader2 } from "lucide-react";
import Dither from "@/components/Dither";
import DecryptedText from "@/components/DecryptedText";

export default function Home() {
  const router = useRouter();
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userInput = input;
    setInput("");
    setIsLoading(true);

    try {
      // Generate a new session_id (UUID v4) on the frontend
      const sessionId = crypto.randomUUID();

      // Create session in localStorage
      const title = userInput.slice(0, 50) + (userInput.length > 50 ? "..." : "");
      const now = new Date().toISOString();
      const sessions = JSON.parse(localStorage.getItem("agnoSessions") || "[]");
      sessions.unshift({
        id: sessionId,
        title,
        createdAt: now,
        lastUsedAt: now,
      });
      localStorage.setItem("agnoSessions", JSON.stringify(sessions));

      // Send message with the new session_id
      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userInput,
          session_id: sessionId,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to send message");
      }

      // Redirect to the chat page with the session_id
      router.push(`/chat/${sessionId}`);
    } catch (error) {
      console.error("Error:", error);
      setIsLoading(false);
      // Could show error toast here
    }
  };

  const handleNewChat = () => {
    router.push("/");
  };

  const handleToggleHistory = () => {
    router.push("/history");
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <SidebarProvider>
      <div className="flex min-h-screen w-full">
        <AppSidebar
          onNewChat={handleNewChat}
          onToggleHistory={handleToggleHistory}
        />
        {/* Dither background - full screen, behind everything */}
        <div className="fixed inset-0 w-full h-full z-0">
          <Dither
            waveColor={[0.5, 0.5, 0.55]}
            disableAnimation={false}
            enableMouseInteraction={true}
            mouseRadius={0.2}
            colorNum={4}
            waveAmplitude={0.3}
            waveFrequency={0.2}
            waveSpeed={0.05}
          />
        </div>

        <main className="flex-1 flex flex-col relative z-10">
          {/* Main content area - Welcome screen */}
          <div className="flex-1 flex flex-col items-center justify-center p-4 md:p-6 relative z-10">
            <div className="w-full max-w-2xl mx-auto flex flex-col items-center gap-8 mainDiv">
              <DecryptedText
                text="What do we cook today, Edu?"
                animateOn="view"
                revealDirection="center"
                className="text-gray-500 dark:text-gray-400 text-2xl font-light"
              />
              <div className="w-full animate-fade-in">
                <div className="bg-white dark:bg-zinc-800 rounded-lg border border-gray-300 dark:border-zinc-700 p-2 shadow-lg flex items-end gap-2">
                  <Textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyPress}
                    placeholder="Type your message here..."
                    disabled={isLoading}
                    className="min-h-[60px] max-h-[200px] resize-none border-0 focus-visible:ring-0 focus-visible:ring-offset-0 bg-transparent flex-1"
                  />
                  <Button
                    onClick={handleSend}
                    disabled={isLoading || !input.trim()}
                    size="icon"
                    className="bg-slate-700 hover:bg-slate-600 text-white shrink-0"
                    aria-label="Send message"
                  >
                    {isLoading ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : (
                      <ArrowUpIcon className="h-4 w-4" />
                    )}
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </SidebarProvider>
  );
}
