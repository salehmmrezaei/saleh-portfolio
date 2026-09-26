import type { Education, Experience, Project, SkillCategory } from '../types';

const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL || '/api').replace(/\/$/, '');

export class ApiError extends Error {
  readonly status?: number;

  constructor(message: string, status?: number) {
    super(message);
    this.status = status;
    this.name = 'ApiError';
  }
}

async function request<T>(path: string, validate: (value: unknown) => value is T, options?: RequestInit): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`, options);
  const body: unknown = await response.json().catch(() => null);

  if (!response.ok) {
    const detail = isRecord(body) && typeof body.detail === 'string' ? body.detail : `Request failed (${response.status})`;
    throw new ApiError(detail, response.status);
  }
  if (!validate(body)) throw new ApiError(`Unexpected response from ${path}`);
  return body;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null;
}

function isStringArray(value: unknown): value is string[] {
  return Array.isArray(value) && value.every((item) => typeof item === 'string');
}

function isProject(value: unknown): value is Project {
  return isRecord(value) && typeof value.id === 'number' && typeof value.name === 'string'
    && isStringArray(value.skills) && typeof value.url === 'string' && isStringArray(value.description);
}

function isExperience(value: unknown): value is Experience {
  return isRecord(value) && typeof value.id === 'number' && typeof value.company === 'string'
    && typeof value.company_slug === 'string'
    && typeof value.role === 'string' && typeof value.start_date === 'string' && typeof value.end_date === 'string'
    && isStringArray(value.skills) && typeof value.url === 'string' && isStringArray(value.description);
}

function isEducation(value: unknown): value is Education {
  return isRecord(value) && typeof value.id === 'number' && typeof value.institution === 'string'
    && typeof value.degree === 'string'
    && typeof value.start_date === 'string' && typeof value.end_date === 'string' && typeof value.country === 'string';
}

function isSkillCategory(value: unknown): value is SkillCategory {
  return isRecord(value) && typeof value.id === 'number' && typeof value.title === 'string'
    && isStringArray(value.skills) && typeof value.description === 'string' && typeof value.featured === 'boolean';
}

function isArrayOf<T>(guard: (value: unknown) => value is T) {
  return (value: unknown): value is T[] => Array.isArray(value) && value.every(guard);
}

export async function getProjects(signal?: AbortSignal) {
  return request('/projects', isArrayOf(isProject), { signal });
}

export async function getExperiences(signal?: AbortSignal) {
  return request('/experiences', isArrayOf(isExperience), { signal });
}

export async function getEducations(signal?: AbortSignal) {
  return request('/educations', isArrayOf(isEducation), { signal });
}

export async function getSkills(signal?: AbortSignal) {
  return request('/skills', isArrayOf(isSkillCategory), { signal });
}

export interface ContactPayload {
  name: string;
  email: string;
  subject: string;
  message: string;
  website: string;
}

export async function sendContactMessage(payload: ContactPayload) {
  return request('/contact', (value): value is { message: string } => (
    isRecord(value) && typeof value.message === 'string'
  ), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
}
