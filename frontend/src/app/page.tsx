"use client";

import { useState, useEffect } from "react";
import { AppSidebar } from "@/components/app-sidebar";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { ArrowUpIcon, Loader2 } from "lucide-react";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      const data = await response.json();
      const assistantMessage: Message = {
        role: "assistant",
        content: data.response,
      };
      setMessages((prev) => [...prev, assistantMessage]);
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

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <SidebarProvider>
      <div className="flex min-h-screen w-full">
        <AppSidebar />
        <main className="flex-1 flex flex-col bg-zinc-50 dark:bg-zinc-900">
          {/* Header with sidebar trigger */}
          <header className="sticky top-0 z-10 flex h-14 items-center gap-4 border-b bg-white dark:bg-zinc-800 px-4">
            <SidebarTrigger />
          </header>

          {/* Main chat area */}
          <div className="flex-1 flex flex-col p-4 md:p-6">
            {messages.length === 0 ? (
              /* Centered welcome and input */
              <div className="flex-1 flex flex-col items-center justify-center w-full max-w-2xl mx-auto gap-8">
                <p className="text-gray-500 dark:text-gray-400 text-2xl font-light animate-fade-in">
                  What do we cook today, Edu?
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
                            : "bg-white dark:bg-zinc-800 text-black dark:text-white border border-gray-200 dark:border-zinc-700"
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
