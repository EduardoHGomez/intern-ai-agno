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
import BubbleMenu from "@/components/BubbleMenu";
import Image from "next/image";

const toolItems = [
  {
    label: "Drive",
    href: "#",
    ariaLabel: "Google Drive",
    rotation: -8,
    hoverStyles: { bgColor: "#4285f4", textColor: "#ffffff" }
  },
  {
    label: "Gmail",
    href: "#",
    ariaLabel: "Gmail",
    rotation: 8,
    hoverStyles: { bgColor: "#ea4335", textColor: "#ffffff" }
  },
  {
    label: "Google",
    href: "#",
    ariaLabel: "Google",
    rotation: -8,
    hoverStyles: { bgColor: "#fbbc04", textColor: "#ffffff" }
  },
  {
    label: "Slack",
    href: "#",
    ariaLabel: "Slack",
    rotation: 8,
    hoverStyles: { bgColor: "#611f69", textColor: "#ffffff" }
  },
  {
    label: "Zoom",
    href: "#",
    ariaLabel: "Zoom",
    rotation: -8,
    hoverStyles: { bgColor: "#2d8cff", textColor: "#ffffff" }
  },
  {
    label: "Analytics",
    href: "#",
    ariaLabel: "Analytics",
    rotation: 8,
    hoverStyles: { bgColor: "#ff6f00", textColor: "#ffffff" }
  }
];

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
            <div className="w-full max-w-2xl mx-auto flex flex-col items-center gap-2 mainDiv">
              <DecryptedText
                text="Intern AI"
                animateOn="view"
                revealDirection="center"
                className="text-gray-800 dark:text-gray-700 text-3xl font-bold"
              />
              <div>
                <span
                className="text-gray-500 dark:text-gray-400 text-2l font-light"
                >One assistant to connect your corporate tasks</span>
              </div>
              <div className="w-full animate-fade-in">
                <div className="bg-white dark:bg-zinc-800 rounded-lg border border-gray-300 dark:border-zinc-700 p-2 flex items-end gap-2">
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

            {/* Tools Section */}
            <div className="w-full max-w-4xl mx-auto mt-16 px-4">
              <div className="text-center mb-8">
                <h2 className="text-2xl md:text-3xl font-semibold text-gray-800 dark:text-gray-200 mb-2">
                  Your Intern without bothering you
                </h2>
                <p className="text-gray-600 dark:text-gray-400 text-lg">
                  Connect these tools
                </p>
              </div>

              {/* Tool Icons Grid */}
              <div className="grid grid-cols-3 md:grid-cols-6 gap-6 md:gap-8 justify-items-center mb-8">
                {[
                  { src: "/drive.svg", alt: "Google Drive", color: "#4285f4" },
                  { src: "/gmail.svg", alt: "Gmail", color: "#ea4335" },
                  { src: "/google.svg", alt: "Google", color: "#fbbc04" },
                  { src: "/slack.svg", alt: "Slack", color: "#611f69" },
                  { src: "/zoom.svg", alt: "Zoom", color: "#2d8cff" },
                  { src: "/analytics.svg", alt: "Analytics", color: "#ff6f00" }
                ].map((tool, idx) => (
                  <div
                    key={idx}
                    className="group relative flex items-center justify-center w-16 h-16 md:w-20 md:h-20 rounded-2xl bg-white dark:bg-zinc-800 shadow-md hover:shadow-xl transition-all duration-300 hover:scale-110 cursor-pointer border border-gray-200 dark:border-zinc-700"
                    style={{
                      transitionDelay: `${idx * 50}ms`
                    }}
                  >
                    <Image
                      src={tool.src}
                      alt={tool.alt}
                      width={40}
                      height={40}
                      className="w-8 h-8 md:w-10 md:h-10 object-contain transition-transform group-hover:scale-110"
                    />
                  </div>
                ))}
              </div>
            </div>
          </div>
        </main>
      </div>
    </SidebarProvider>
  );
}
