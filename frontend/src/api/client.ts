const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL || '/api').replace(/\/$/, '');

export class ApiError extends Error {
  readonly status?: number;

  constructor(message: string, status?: number) {
    super(message);
    this.status = status;
    this.name = 'ApiError';
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null;
}

async function request<T>(
  path: string,
  validate: (value: unknown) => value is T,
  options?: RequestInit,
): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`, options);
  const body: unknown = await response.json().catch(() => null);

  if (!response.ok) {
    const detail =
      isRecord(body) && typeof body.detail === 'string'
        ? body.detail
        : `Request failed (${response.status})`;
    throw new ApiError(detail, response.status);
  }

  if (!validate(body)) {
    throw new ApiError(`Unexpected response from ${path}`);
  }

  return body;
}

export interface ContactPayload {
  name: string;
  email: string;
  subject: string;
  message: string;
  website: string;
  turnstile_token: string;
}

export async function sendContactMessage(payload: ContactPayload) {
  return request(
    '/contact',
    (value): value is { message: string } =>
      isRecord(value) && typeof value.message === 'string',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    },
  );
}
