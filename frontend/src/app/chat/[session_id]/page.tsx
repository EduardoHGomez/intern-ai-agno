"use client";

/**
 * Chat session page with session_id in URL
 *
 * NOTE: Exposing session_id in the URL is not ideal for production security
 * (anyone with the URL can access that chat session). For a production app,
 * you should implement proper authentication and authorization. This approach
 * is used here for simplicity and ease of development.
 */

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { AppSidebar } from "@/components/app-sidebar";
import { SidebarProvider } from "@/components/ui/sidebar";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { ArrowUpIcon, Loader2 } from "lucide-react";
import { touchSession, getSession, updateSessionTitle } from "@/lib/sessions";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function ChatPage() {
  const params = useParams();
  const router = useRouter();
  const sessionId = params.session_id as string;

  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingHistory, setIsLoadingHistory] = useState(true);

  // Load session messages from backend on mount
  useEffect(() => {
    const loadMessages = async () => {
      try {
        // Verify session exists in localStorage
        const session = getSession(sessionId);
        if (session) {
          touchSession(sessionId);
        }

        // Fetch conversation history from backend
        const response = await fetch(
          `http://localhost:8000/api/sessions/${sessionId}/messages`
        );

        if (response.ok) {
          const data = await response.json();
          setMessages(data.messages || []);
        }
      } catch (error) {
        console.error("Error loading session messages:", error);
      } finally {
        setIsLoadingHistory(false);
      }
    };

    loadMessages();
  }, [sessionId]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { role: "user", content: input };
    const userInput = input;
    const isFirstMessage = messages.length === 0;

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userInput,
          session_id: sessionId, // Use session_id from URL
        }),
      });

      const data = await response.json();
      const assistantMessage: Message = {
        role: "assistant",
        content: data.response,
      };
      setMessages((prev) => [...prev, assistantMessage]);

      // Update session metadata
      touchSession(sessionId);

      // Auto-generate title from first message
      if (isFirstMessage) {
        const title = userInput.slice(0, 50) + (userInput.length > 50 ? "..." : "");
        updateSessionTitle(sessionId, title);
      }
    } catch (error) {
      console.error("Error:", error);
      const errorMessage: Message = {
        role: "assistant",
        content: "Error: Could not connect to backend",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
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
        <main className="flex-1 flex flex-col bg-zinc-50 dark:bg-zinc-900">
          {/* Main content area */}
          <div className="flex-1 flex flex-col p-4 md:p-6">
            {isLoadingHistory ? (
              /* Loading state */
              <div className="flex-1 flex items-center justify-center">
                <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
              </div>
            ) : messages.length === 0 ? (
              /* Centered welcome and input (for truly new sessions) */
              <div className="flex-1 flex flex-col items-center justify-center w-full max-w-2xl mx-auto gap-8">
                <p className="text-gray-500 dark:text-gray-400 text-2xl font-light animate-fade-in">
                   cook today, Edu?
                </p>
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
            ) : (
              /* Chat with messages */
              <div className="flex-1 w-full max-w-4xl mx-auto flex flex-col">
                {/* Messages Display */}
                <div className="flex-1 overflow-y-auto mb-4 space-y-4">
                  {messages.map((msg, idx) => (
                    <div
                      key={idx}
                      className={`flex ${
                        msg.role === "user" ? "justify-end" : "justify-start"
                      }`}
                    >
                      <div
                        className={`max-w-[80%] rounded-lg p-4 ${
                          msg.role === "user"
                            ? "bg-slate-700 text-white"
                            : "text-gray-800 dark:text-gray-200"
                        }`}
                      >
                        <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Input Area - Bottom */}
                <div className="sticky bottom-0 bg-zinc-50 dark:bg-zinc-900 pt-4">
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
            )}
          </div>
        </main>
      </div>
    </SidebarProvider>
  );
}
