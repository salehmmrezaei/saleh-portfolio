import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { ContactSection } from './ContactSection';

describe('ContactSection', () => {
  beforeEach(() => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(JSON.stringify({ message: 'sent' }), { status: 200 }));
  });

  it('submits the contact form and reports success', async () => {
    render(<ContactSection onBackHome={vi.fn()} />);
    fireEvent.change(screen.getByLabelText('Name'), { target: { value: 'Saleh' } });
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'saleh@example.com' } });
    fireEvent.change(screen.getByLabelText('Subject'), { target: { value: 'Hello' } });
    fireEvent.change(screen.getByLabelText('Message'), { target: { value: 'Message' } });
    fireEvent.submit(screen.getByRole('button', { name: /send message/i }).closest('form')!);

    await waitFor(() => expect(screen.getByText('Thanks! Your message has been sent.')).toBeInTheDocument());
  });
});
