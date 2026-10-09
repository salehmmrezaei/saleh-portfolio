import {
  useState,
  type FormEvent,
} from 'react';

import {
  ApiError,
  sendChatMessage,
  type ChatTurn,
} from '../api/client';
import chatbotIcon from '../assets/chatbot.svg';

const MAX_HISTORY_TURNS = 6;

function getErrorMessage(error: unknown): string {
  if (!(error instanceof ApiError)) {
    return 'I couldn’t connect to the assistant. Please try again.';
  }

  if (error.status === 422) {
    return 'Please shorten or check your message and try again.';
  }

  if (error.status === 429) {
    return 'The assistant is receiving too many requests. Please try again later.';
  }

  if (error.status === 502 || error.status === 503) {
    return 'The assistant is temporarily unavailable. Please try again shortly.';
  }

  return 'Something went wrong. Please try again.';
}

export function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatTurn[]>([]);
  const [message, setMessage] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (
    event: FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault();

    const trimmedMessage = message.trim();

    if (!trimmedMessage || isSending) {
      return;
    }

    const history = messages.slice(-MAX_HISTORY_TURNS);
    const userTurn: ChatTurn = {
      role: 'user',
      content: trimmedMessage,
    };

    setMessages((current) => [...current, userTurn]);
    setMessage('');
    setError(null);
    setIsSending(true);

    try {
      const response = await sendChatMessage({
        message: trimmedMessage,
        history,
      });

      setMessages((current) => [
        ...current,
        {
          role: 'assistant',
          content: response.answer,
        },
      ]);
    } catch (requestError: unknown) {
      setError(getErrorMessage(requestError));
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="chat-widget">
      {isOpen && (
        <section
          className="chat-panel"
          aria-label="Portfolio assistant"
        >
          <header className="chat-header">
            <div>
              <span className="chat-eyebrow">
                Portfolio assistant
              </span>
              <strong>Ask about Saleh</strong>
            </div>

            <button
              className="chat-close"
              type="button"
              onClick={() => setIsOpen(false)}
              aria-label="Close assistant"
            >
              ×
            </button>
          </header>

          <div
            className="chat-messages"
            aria-live="polite"
          >
            {messages.length === 0 && (
              <div className="chat-intro">
                <p>
                  Ask me about Saleh&apos;s experience,
                  projects, skills, or education.
                </p>

                <span>
                  Try: “What experience does Saleh have
                  with RAG?”
                </span>
              </div>
            )}

            {messages.map((turn, index) => (
              <div
                className={`chat-message ${turn.role}`}
                key={`${turn.role}-${index}`}
              >
                <span>
                  {turn.role === 'user' ? 'You' : 'Assistant'}
                </span>
                <p>{turn.content}</p>
              </div>
            ))}

            {isSending && (
              <div className="chat-message assistant">
                <span>Assistant</span>
                <p className="chat-thinking">
                  Thinking…
                </p>
              </div>
            )}

            {error && (
              <p className="chat-error" role="alert">
                {error}
              </p>
            )}
          </div>

          <form
            className="chat-form"
            onSubmit={handleSubmit}
          >
            <label className="sr-only" htmlFor="chat-message">
              Ask about Saleh
            </label>

            <textarea
              id="chat-message"
              value={message}
              onChange={(event) =>
                setMessage(event.target.value)
              }
              onKeyDown={(event) => {
                if (
                  event.key === 'Enter'
                  && !event.shiftKey
                  && !event.nativeEvent.isComposing
                ) {
                  event.preventDefault();
                  event.currentTarget.form?.requestSubmit();
                }
              }}
              placeholder="Ask about experience, projects, skills..."
              maxLength={800}
              rows={2}
              disabled={isSending}
            />

            <div className="chat-form-footer">
              <span>{message.length}/800</span>

              <button
                type="submit"
                disabled={
                  isSending || !message.trim()
                }
              >
                {isSending ? 'Sending…' : 'Send'}
              </button>
            </div>
          </form>
        </section>
      )}

      <button
        className="chat-launcher"
        type="button"
        onClick={() => setIsOpen((current) => !current)}
        aria-label={
          isOpen
            ? 'Close portfolio assistant'
            : 'Open portfolio assistant'
        }
        aria-expanded={isOpen}
      >
        <img
          src={chatbotIcon}
          alt=""
          aria-hidden="true"
        />
      </button>
    </div>
  );
}
