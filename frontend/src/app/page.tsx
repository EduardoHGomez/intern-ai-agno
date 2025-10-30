"use client";

import { useState } from "react";

type Message = {
  role: "user" | "system";
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
      const systemMessage: Message = { role: "system", content: data.response };
      setMessages((prev) => [...prev, systemMessage]);
    } catch (error) {
      console.error("Error:", error);
      const errorMessage: Message = {
        role: "system",
        content: "Error: Could not connect to backend",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 dark:bg-zinc-900 p-4">
      <div className="w-full max-w-2xl bg-white dark:bg-zinc-800 rounded-lg shadow-lg p-6 flex flex-col h-[600px]">
        <h1 className="text-2xl font-bold mb-4 text-black dark:text-white">
          Chat Interface
        </h1>

        {/* Messages Display */}
        <div className="flex-1 overflow-y-auto mb-4 space-y-3">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`p-3 rounded-lg ${
                msg.role === "user"
                  ? "bg-blue-100 dark:bg-blue-900 ml-auto max-w-[80%]"
                  : "bg-gray-100 dark:bg-gray-700 mr-auto max-w-[80%]"
              }`}
            >
              <p className="text-sm font-semibold mb-1 text-black dark:text-white">
                {msg.role === "user" ? "You" : "Assistant"}
              </p>
              <p className="text-black dark:text-white">{msg.content}</p>
            </div>
          ))}
          {messages.length === 0 && (
            <p className="text-center text-gray-500 dark:text-gray-400 mt-10">
              Send a message to start chatting
            </p>
          )}
        </div>

        {/* Input Area */}
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            disabled={isLoading}
            className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-zinc-700 dark:text-white disabled:opacity-50"
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? "..." : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
}
