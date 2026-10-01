import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { ContactSection } from './ContactSection';
import { useEffect } from 'react';

vi.mock('./TurnstileWidget', () => ({
  TurnstileWidget: ({
    onTokenChange,
  }: {
    onTokenChange: (token: string) => void;
  }) => {
    useEffect(() => {
      onTokenChange('test-turnstile-token');
    }, [onTokenChange]);

    return <div data-testid="turnstile-widget" />;
  },
}));


describe('ContactSection', () => {
  afterEach(() => {
    cleanup();
    vi.restoreAllMocks();
  });

  beforeEach(() => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(JSON.stringify({ message: 'sent' }), { status: 200 }));
  });

  it('submits the contact form and reports success', async () => {
    render(<ContactSection onBackHome={vi.fn()} />);
    expect(screen.queryByLabelText('Website')).not.toBeInTheDocument();
    fireEvent.change(screen.getByLabelText('Name'), { target: { value: 'Saleh' } });
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'saleh@example.com' } });
    fireEvent.change(screen.getByLabelText('Subject'), { target: { value: 'Hello' } });
    fireEvent.change(screen.getByLabelText('Message'), { target: { value: 'Message' } });
    fireEvent.submit(screen.getByRole('button', { name: /send message/i }).closest('form')!);

    await waitFor(() => expect(screen.getByText('Thanks for your message! I’ll get back to you soon.')).toBeInTheDocument());
  });

  it('shows a rate-limit error toast', async () => {
    vi.mocked(globalThis.fetch).mockResolvedValueOnce(
      new Response(JSON.stringify({ detail: 'Too many contact requests. Please try again later.' }), { status: 429 }),
    );
    render(<ContactSection onBackHome={vi.fn()} />);
    fireEvent.change(screen.getByLabelText('Name'), { target: { value: 'Saleh' } });
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'saleh@example.com' } });
    fireEvent.change(screen.getByLabelText('Subject'), { target: { value: 'Hello' } });
    fireEvent.change(screen.getByLabelText('Message'), { target: { value: 'Message' } });
    fireEvent.submit(screen.getByRole('button', { name: /send message/i }).closest('form')!);

    await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent('You’ve sent too many messages. Please wait a minute and try again.'));
  });
});
