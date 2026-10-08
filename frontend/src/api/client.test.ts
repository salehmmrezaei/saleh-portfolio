import { afterEach, describe, expect, it, vi } from 'vitest';
import {
  ApiError,
  sendChatMessage,
  sendContactMessage,
} from './client';


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


it('returns a validated chat response', async () => {
  vi.spyOn(globalThis, 'fetch').mockResolvedValue(
    new Response(
      JSON.stringify({
        answer: 'Saleh has experience with RAG systems.',
      }),
      { status: 200 },
    ),
  );

  await expect(
    sendChatMessage({
      message: 'What experience does Saleh have with RAG?',
      history: [],
    }),
  ).resolves.toEqual({
    answer: 'Saleh has experience with RAG systems.',
  });
});

it('rejects malformed chat responses', async () => {
  vi.spyOn(globalThis, 'fetch').mockResolvedValue(
    new Response(
      JSON.stringify({
        message: 'wrong shape',
      }),
      { status: 200 },
    ),
  );

  await expect(
    sendChatMessage({
      message: 'Tell me about Saleh.',
      history: [],
    }),
  ).rejects.toBeInstanceOf(ApiError);
});