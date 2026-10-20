
import { useState } from "react";
import type { FormEvent } from "react";
import "./App.css";

type Message = {
  role: "user" | "assistant";
  content: string;
};

const suggestions = [
  {
    icon: "☀",
    title: "Check the weather",
    prompt: "What is the current weather in Jaipur?",
  },
  {
    icon: "↗",
    title: "Stock market",
    prompt: "What is the latest closing price of TCS?",
  },
  {
    icon: "⌘",
    title: "Compare weather",
    prompt: "Compare the weather in Jaipur and Mumbai.",
  },
];

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function sendMessage(
    text: string,
    event?: FormEvent<HTMLFormElement>,
  ) {
    event?.preventDefault();

    const message = text.trim();
    if (!message || loading) return;

    setMessages((previous) => [
      ...previous,
      { role: "user", content: message },
    ]);
    setInput("");
    setError("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to get a response.");
      }

      setMessages((previous) => [
        ...previous,
        { role: "assistant", content: data.reply },
      ]);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not connect to the backend.",
      );
    } finally {
      setLoading(false);
    }
  }

  function newChat() {
    if (loading) return;
    setMessages([]);
    setInput("");
    setError("");
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">✳</div>
          <div>
            <strong>Orbit AI</strong>
            <span>Intelligent assistant</span>
          </div>
        </div>

        <button className="new-chat" onClick={newChat}>
          <span>＋</span> New conversation
        </button>

        <div className="sidebar-label">YOUR ASSISTANT</div>

        <div className="sidebar-item active">
          <span>◉</span> Weather & Stocks
        </div>

        <div className="sidebar-info">
          <div className="status-dot" />
          <div>
            <strong>Gemini Agent</strong>
            <span>Python tools enabled</span>
          </div>
        </div>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <div>
            <span className="mobile-brand">✳ Orbit AI</span>
            <span className="breadcrumb">Workspace / Chat</span>
          </div>
          <div className="model-pill">
            <span className="status-dot" />
            Gemini · Tool calling
          </div>
        </header>

        <section className="chat-area">
          {messages.length === 0 ? (
            <div className="welcome">
              <div className="welcome-symbol">✳</div>
              <div className="eyebrow">YOUR AI ASSISTANT</div>
              <h1>What can I help you <span>explore?</span></h1>
              <p className="welcome-description">
                Ask about the weather or stock prices.
                I'll choose the right Python tool for your request.
              </p>

              <div className="suggestions">
                {suggestions.map((item) => (
                  <button
                    className="suggestion-card"
                    key={item.title}
                    onClick={() => sendMessage(item.prompt)}
                    disabled={loading}
                  >
                    <span className="suggestion-icon">{item.icon}</span>
                    <strong>{item.title}</strong>
                    <span className="suggestion-prompt">
                      {item.prompt}
                    </span>
                    <span className="suggestion-arrow">↗</span>
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="messages">
              {messages.map((message, index) => (
                <div
                  className={`message-row ${message.role}`}
                  key={`${index}-${message.role}`}
                >
                  {message.role === "assistant" && (
                    <div className="avatar assistant-avatar">✳</div>
                  )}

                  <div className="message-content">
                    <span className="message-author">
                      {message.role === "user" ? "You" : "Orbit AI"}
                    </span>
                    <div className="message-bubble">
                      {message.content}
                    </div>
                  </div>

                  {message.role === "user" && (
                    <div className="avatar user-avatar">Y</div>
                  )}
                </div>
              ))}

              {loading && (
                <div className="message-row assistant">
                  <div className="avatar assistant-avatar">✳</div>
                  <div className="message-content">
                    <span className="message-author">Orbit AI</span>
                    <div className="message-bubble typing">
                      <span />
                      <span />
                      <span />
                      <small>Thinking and checking tools...</small>
                    </div>
                  </div>
                </div>
              )}

              <div />
            </div>
          )}

          {error && (
            <div className="error-banner" role="alert">
              <span>{error}</span>
              <button onClick={() => setError("")}>Dismiss</button>
            </div>
          )}
        </section>

        <footer className="composer-area">
          <form
            className="composer"
            onSubmit={(event) => sendMessage(input, event)}
          >
            <textarea
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={(event) => {
                if (
                  event.key === "Enter" &&
                  !event.shiftKey &&
                  !event.nativeEvent.isComposing
                ) {
                  event.preventDefault();
                  void sendMessage(input);
                }
              }}
              placeholder="Ask about weather, stocks, or anything else..."
              rows={1}
              maxLength={2000}
              disabled={loading}
              aria-label="Message"
            />
            <button
              className="send-button"
              type="submit"
              disabled={loading || !input.trim()}
              aria-label="Send message"
            >
              {loading ? "…" : "↑"}
            </button>
          </form>
          <div className="composer-note">
            <span>Gemini with Python tools</span>
            <span>Enter to send · Shift + Enter for a new line</span>
          </div>
        </footer>
      </main>
    </div>
  );
}

export default App;
