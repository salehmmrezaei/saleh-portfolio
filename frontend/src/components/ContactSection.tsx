import { useState, type FormEvent } from 'react';
import { ApiError, sendContactMessage } from '../api/client';
import { ChatBubbleIcon, HomeButton } from './Icons';
import { TurnstileWidget } from './TurnstileWidget';

type FormStatus = {
  type: 'success' | 'error';
  heading: string;
  message: string;
};

function getErrorStatus(error: unknown): FormStatus {
  if (error instanceof ApiError) {
    if (error.status === 429) {
      return {
        type: 'error',
        heading: 'PLEASE WAIT',
        message: 'Too many attempts. Please wait a minute and try again.',
      };
    }

    if (error.status === 400 && /turnstile|verification/i.test(error.message)) {
      return {
        type: 'error',
        heading: 'VERIFICATION FAILED',
        message: 'Verification failed or expired. Please try again.',
      };
    }

    if (error.status === 502 || error.status === 503) {
      return {
        type: 'error',
        heading: 'SERVICE UNAVAILABLE',
        message: 'The contact service is temporarily unavailable. Please try again soon.',
      };
    }
  }

  return {
    type: 'error',
    heading: 'MESSAGE NOT SENT',
    message: "Couldn't send your message. Please try again.",
  };
}

function StatusIcon({ type }: { type: FormStatus['type'] }) {
  if (type === 'success') {
    return (
      <svg className="form-status-icon" viewBox="0 0 24 24" aria-hidden="true">
        <path d="m5 12.5 4.5 4.5L19 7.5" />
      </svg>
    );
  }

  return (
    <svg className="form-status-icon" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 4 3.5 19h17L12 4Z" />
      <path d="M12 9v4M12 16.5h.01" />
    </svg>
  );
}

export function ContactSection({ onBackHome }: { onBackHome: () => void }) {
  const [isSending, setIsSending] = useState(false);
  const [status, setStatus] = useState<FormStatus | null>(null);
  const [turnstileToken, setTurnstileToken] = useState('');
  const [turnstileKey, setTurnstileKey] = useState(0);
  
  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (isSending || !turnstileToken) return;
    const formElement = event.currentTarget;
    const form = new FormData(formElement);
    setIsSending(true);
    setStatus(null);

    const value = (name: string) => String(form.get(name) ?? '');
    sendContactMessage({
      name: value('name'),
      email: value('email'),
      subject: value('subject'),
      message: value('message'),
      website: '',
      turnstile_token: turnstileToken,
    })
      .then(() => {
        formElement.reset();
      setStatus({
        type: 'success',
        heading: 'MESSAGE SENT',
        message: "Thanks — I'll get back to you soon.",
      });
    })
    .catch((error: unknown) => setStatus(getErrorStatus(error)))
      .finally(() => {
        setIsSending(false);
        setTurnstileToken('');
        setTurnstileKey((current) => current + 1);
      });
  };

  return (
    <footer className="snap-section contact-section" id="contact">
      <div className="contact-copy">
        <p>Have an idea worth building?</p>
        <h2>Let&apos;s talk <span><ChatBubbleIcon className="contact-chat-icon" /></span></h2>
      </div>
      <form className="contact-form" onSubmit={handleSubmit}>
        <div className="form-row">
          <label>
            Name
            <input name="name" type="text" autoComplete="name" placeholder="Your name" required />
          </label>
          <label>
            Email
            <input name="email" type="email" autoComplete="email" placeholder="you@example.com" required />
          </label>
          <label>
            Subject
            <input name="subject" type="text" placeholder="How can I help?" maxLength={160} required />
          </label>
        </div>
        <label>
          Message
          <textarea name="message" rows={4} placeholder="Tell me about your idea..." required />
        </label>
        <TurnstileWidget
        key={turnstileKey}
        onTokenChange={setTurnstileToken}
      />

      <button
        type="submit"
        disabled={isSending || !turnstileToken}
      >
        {isSending ? 'SENDING…' : 'SEND MESSAGE ↗'}
      </button>
        {status && (
          <div
            className={`form-status ${status.type}`}
            role={status.type === 'error' ? 'alert' : 'status'}
            aria-live={status.type === 'error' ? 'assertive' : 'polite'}
          >
            <StatusIcon type={status.type} />
            <div>
              <strong>{status.heading}</strong>
              <p>{status.message}</p>
            </div>
          </div>
        )}
      </form>
      <small>© {new Date().getFullYear()} Saleh Rezaei</small>
      <HomeButton onClick={onBackHome} />
    </footer>
  );
}
