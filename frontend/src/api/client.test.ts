import { afterEach, describe, expect, it, vi } from 'vitest';
import { ApiError, sendContactMessage } from './client';

const payload = {
  name: 'Saleh',
  email: 'saleh@example.com',
  subject: 'Hello',
  message: 'Test message',
  website: '',
  turnstile_token: 'test-token',
};

describe('API client', () => {
  afterEach(() => vi.restoreAllMocks());

  it('returns a validated contact response', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ message: 'Message sent successfully' }), {
        status: 200,
      }),
    );

    await expect(sendContactMessage(payload)).resolves.toEqual({
      message: 'Message sent successfully',
    });
  });

  it('rejects malformed contact responses', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ ok: true }), { status: 200 }),
    );

    await expect(sendContactMessage(payload)).rejects.toBeInstanceOf(ApiError);
  });
});
