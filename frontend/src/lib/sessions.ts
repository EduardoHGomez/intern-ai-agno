/**
 * Session management for chat history.
 * Sessions are stored in localStorage and identified by UUIDs.
 */

export type ChatSession = {
  id: string;
  title: string;
  createdAt: string;
  lastUsedAt: string;
};

const STORAGE_KEY = "agnoSessions";

/**
 * Load all sessions from localStorage
 */
export function loadSessions(): ChatSession[] {
  if (typeof window === "undefined") return [];
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? JSON.parse(stored) : [];
  } catch (error) {
    console.error("Error loading sessions:", error);
    return [];
  }
}

/**
 * Save sessions to localStorage
 */
export function saveSessions(sessions: ChatSession[]): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(sessions));
  } catch (error) {
    console.error("Error saving sessions:", error);
  }
}

/**
 * Create a new session and add it to storage
 */
export function createSession(title = "New chat"): ChatSession {
  const id = crypto.randomUUID();
  const now = new Date().toISOString();
  const session: ChatSession = {
    id,
    title,
    createdAt: now,
    lastUsedAt: now,
  };

  const sessions = loadSessions();
  sessions.unshift(session);
  saveSessions(sessions);

  return session;
}

/**
 * Update the lastUsedAt timestamp for a session
 */
export function touchSession(id: string): void {
  const sessions = loadSessions();
  const index = sessions.findIndex((s) => s.id === id);
  if (index >= 0) {
    sessions[index].lastUsedAt = new Date().toISOString();
    saveSessions(sessions);
  }
}

/**
 * Update the title of a session
 */
export function updateSessionTitle(id: string, title: string): void {
  const sessions = loadSessions();
  const index = sessions.findIndex((s) => s.id === id);
  if (index >= 0) {
    sessions[index].title = title;
    saveSessions(sessions);
  }
}

/**
 * Remove a session from storage
 */
export function removeSession(id: string): void {
  const sessions = loadSessions();
  saveSessions(sessions.filter((s) => s.id !== id));
}

/**
 * Get a specific session by ID
 */
export function getSession(id: string): ChatSession | undefined {
  return loadSessions().find((s) => s.id === id);
}
