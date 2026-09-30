import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { ContactSection } from './ContactSection';
import { useEffect } from 'react';

const { getTurnstileToken } = vi.hoisted(() => ({
  getTurnstileToken: vi.fn(() => 'test-turnstile-token'),
}));

vi.mock('./TurnstileWidget', () => ({
  TurnstileWidget: ({
    onTokenChange,
  }: {
    onTokenChange: (token: string) => void;
  }) => {
    useEffect(() => {
      onTokenChange(getTurnstileToken());
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

  function fillForm() {
    fireEvent.change(screen.getByLabelText('Name'), { target: { value: 'Saleh' } });
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'saleh@example.com' } });
    fireEvent.change(screen.getByLabelText('Subject'), { target: { value: 'Hello' } });
    fireEvent.change(screen.getByLabelText('Message'), { target: { value: 'Message' } });
  }

  it('submits the contact form and reports success', async () => {
    render(<ContactSection onBackHome={vi.fn()} />);
    expect(screen.queryByLabelText('Website')).not.toBeInTheDocument();
    fillForm();
    fireEvent.submit(screen.getByRole('button', { name: /send message/i }).closest('form')!);

    await waitFor(() => expect(screen.getByText('MESSAGE SENT')).toBeInTheDocument());
    expect(screen.getByText("Thanks — I'll get back to you soon.")).toBeInTheDocument();
    expect(screen.getByRole('status')).toHaveAttribute('aria-live', 'polite');
    expect(screen.getByLabelText('Name')).toHaveValue('');
  });

  it.each([
    [429, 'PLEASE WAIT', 'Too many attempts. Please wait a minute and try again.'],
    [400, 'VERIFICATION FAILED', 'Verification failed or expired. Please try again.'],
    [503, 'SERVICE UNAVAILABLE', 'The contact service is temporarily unavailable. Please try again soon.'],
  ])('reports a helpful message for API status %s', async (status, heading, message) => {
    vi.mocked(globalThis.fetch).mockResolvedValueOnce(
      new Response(JSON.stringify({ detail: status === 400 ? 'Turnstile verification failed' : 'failed' }), { status }),
    );
    render(<ContactSection onBackHome={vi.fn()} />);
    fillForm();
    fireEvent.submit(screen.getByRole('button', { name: /send message/i }).closest('form')!);

    await waitFor(() => expect(screen.getByText(heading)).toBeInTheDocument());
    expect(screen.getByText(message)).toBeInTheDocument();
    expect(screen.getByRole('alert')).toHaveAttribute('aria-live', 'assertive');
    expect(screen.getByLabelText('Name')).toHaveValue('Saleh');
  });

  it('shows a loading state and prevents duplicate submissions', async () => {
    let resolveRequest!: (response: Response) => void;
    vi.mocked(globalThis.fetch).mockImplementationOnce(
      () => new Promise((resolve) => { resolveRequest = resolve; }),
    );
    render(<ContactSection onBackHome={vi.fn()} />);
    fillForm();
    const form = screen.getByRole('button', { name: /send message/i }).closest('form')!;
    fireEvent.submit(form);
    fireEvent.submit(form);

    expect(screen.getByRole('button', { name: 'SENDING…' })).toBeDisabled();
    expect(globalThis.fetch).toHaveBeenCalledTimes(1);
    resolveRequest(new Response(JSON.stringify({ message: 'sent' }), { status: 200 }));
    await waitFor(() => expect(screen.getByRole('status')).toBeInTheDocument());
  });

  it('disables submission until Turnstile verification provides a token', () => {
    getTurnstileToken.mockReturnValueOnce('');
    render(<ContactSection onBackHome={vi.fn()} />);

    expect(screen.getByRole('button', { name: /send message/i })).toBeDisabled();
  });

  it('keeps the form available for retry after a failed submission', async () => {
    vi.mocked(globalThis.fetch)
      .mockResolvedValueOnce(new Response(JSON.stringify({ detail: 'failed' }), { status: 500 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({ message: 'sent' }), { status: 200 }));
    render(<ContactSection onBackHome={vi.fn()} />);
    fillForm();
    const form = screen.getByRole('button', { name: /send message/i }).closest('form')!;
    fireEvent.submit(form);
    await waitFor(() => expect(screen.getByRole('alert')).toBeInTheDocument());
    fireEvent.submit(form);

    await waitFor(() => expect(screen.getByRole('status')).toBeInTheDocument());
    expect(globalThis.fetch).toHaveBeenCalledTimes(2);
  });
});
