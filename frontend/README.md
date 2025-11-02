# Agent Frontend

A modern chat interface for interacting with AI agents that manage emails and calendar events. Built with Next.js 15, React 19, and TypeScript.

## What It Does

This frontend provides a clean, intuitive interface for chatting with an AI-powered personal assistant. The assistant can:
- Read and summarize your emails
- Search through email history
- Manage calendar events
- Show your upcoming schedule
- Coordinate between email and calendar tasks

All responses are rendered beautifully with markdown support, making information easy to read and understand.

## Tech Stack

- **Next.js 15** - React framework with App Router
- **React 19** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS v4** - Styling
- **shadcn/ui** - UI components
- **react-markdown** - Markdown rendering

## Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## Configuration

### Backend API URL

The frontend connects to the backend API running at `http://localhost:8000`.

If you need to change the API URL, update it in:
- `src/app/chat/[session_id]/page.tsx` (lines 48, 77)

### Environment Variables

Currently, no environment variables are required for the frontend. The backend URL is hardcoded for development simplicity.

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── chat/[session_id]/    # Chat page with session management
│   │   ├── history/               # Chat history page
│   │   ├── globals.css            # Global styles
│   │   └── page.tsx               # Home page
│   ├── components/
│   │   ├── ui/                    # shadcn/ui components
│   │   └── app-sidebar.tsx        # Sidebar navigation
│   └── lib/
│       ├── sessions.ts            # Session management logic
│       └── utils.ts               # Utility functions
├── public/                         # Static assets
└── package.json
```

## Features

### Chat Interface
- **Real-time messaging** - Send messages and get instant responses
- **Session management** - Each conversation has a unique session ID
- **Message history** - All messages are persisted and loaded automatically
- **Markdown support** - Assistant responses render as formatted markdown

### Navigation
- **Sidebar** - Access chat history and create new conversations
- **Responsive design** - Works on desktop and mobile
- **Dark mode ready** - Supports dark theme

### Session Management
Sessions are stored in **localStorage** with the following structure:
```typescript
{
  id: string;           // UUID v4
  title: string;        // Auto-generated from first message
  createdAt: number;    // Timestamp
  updatedAt: number;    // Last activity timestamp
}
```

## API Routes Used

The frontend communicates with these backend endpoints:

### GET `/api/sessions/{session_id}/messages`
Retrieves all messages for a specific session.

**Response:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Show me my recent emails"
    },
    {
      "role": "assistant",
      "content": "Here are your recent emails..."
    }
  ]
}
```

### POST `/api/chat`
Sends a message and receives a response.

**Request:**
```json
{
  "message": "What events do I have this week?",
  "session_id": "123e4567-e89b-12d3-a456-426614174000",
  "stream": false
}
```

**Response:**
```json
{
  "session_id": "123e4567-e89b-12d3-a456-426614174000",
  "response": "Here are your upcoming events..."
}
```

## How to Use

1. **Start a new chat:**
   - Click the home icon or visit `http://localhost:3000`
   - Type your message in the text area
   - Press Enter or click the send button

2. **View chat history:**
   - Click the history icon in the sidebar
   - Select a previous conversation to continue

3. **Ask the assistant:**
   - "Show me my recent emails"
   - "What events do I have this week?"
   - "Find emails from Dana"
   - "Show me events with Chris"

## Development

### Build for Production
```bash
npm run build
```

### Run Production Build
```bash
npm start
```

### Lint Code
```bash
npm run lint
```

## Notes

- **Session IDs in URLs:** For development simplicity, session IDs are exposed in URLs. In production, implement proper authentication.
- **No Authentication:** The current version doesn't include user authentication. Add this before deploying to production.
- **Local Storage:** Session metadata is stored client-side. Consider moving to a database for multi-device support.

## Future Improvements

- Add user authentication
- Implement streaming responses for real-time message generation
- Add file upload support for emails/attachments
- Multi-device session sync with backend database
- Export chat history feature
