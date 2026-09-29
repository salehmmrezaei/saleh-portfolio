import { useState, type FormEvent } from 'react';
import { sendContactMessage } from '../api/client';
import { ChatBubbleIcon, HomeButton } from './Icons';
import { TurnstileWidget } from './TurnstileWidget';

export function ContactSection({ onBackHome }: { onBackHome: () => void }) {
  const [isSending, setIsSending] = useState(false);
  const [status, setStatus] = useState<{ type: 'success' | 'error'; message: string } | null>(null);
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
        setStatus({ type: 'success', message: 'Thanks! Your message has been sent.' });
      })
      .catch((error: unknown) => setStatus({ type: 'error', message: error instanceof Error ? error.message : 'Unable to send your message' }))
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
        {isSending ? 'Sending...' : 'Send message'} <span>↗</span>
      </button>
        {status && <p className={`form-status ${status.type}`} role={status.type === 'error' ? 'alert' : 'status'}>{status.message}</p>}
      </form>
      <small>© {new Date().getFullYear()} Saleh Rezaei</small>
      <HomeButton onClick={onBackHome} />
    </footer>
  );
}
