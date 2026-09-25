import type { FormEvent } from 'react';

export function ContactSection() {
  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const name = String(form.get('name') ?? '');
    const email = String(form.get('email') ?? '');
    const message = String(form.get('message') ?? '');
    const subject = encodeURIComponent(`Portfolio message from ${name}`);
    const body = encodeURIComponent(`Name: ${name}\nEmail: ${email}\n\n${message}`);
    window.location.href = `mailto:salehmmrezaei@gmail.com?subject=${subject}&body=${body}`;
  };

  return (
    <footer className="snap-section contact-section" id="contact">
      <div className="contact-copy">
        <p>Have an idea worth building?</p>
        <h2>Let&apos;s talk <span>↗</span></h2>
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
        </div>
        <label>
          Message
          <textarea name="message" rows={4} placeholder="Tell me about your idea..." required />
        </label>
        <button type="submit">Send message <span>↗</span></button>
      </form>
      <small>© {new Date().getFullYear()} Saleh Rezaei</small>
    </footer>
  );
}
