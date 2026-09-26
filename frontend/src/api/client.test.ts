import { afterEach, describe, expect, it, vi } from 'vitest';
import { ApiError, getProjects } from './client';

describe('portfolio API client', () => {
  afterEach(() => vi.restoreAllMocks());

  it('returns validated project data', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(JSON.stringify([{
      id: 1,
      name: 'Project',
      skills: ['React'],
      url: 'https://example.com',
      description: ['Description'],
    }]), { status: 200 }));

    await expect(getProjects()).resolves.toHaveLength(1);
  });

  it('rejects malformed responses', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(JSON.stringify({ projects: [] }), { status: 200 }));

    await expect(getProjects()).rejects.toBeInstanceOf(ApiError);
  });
});
