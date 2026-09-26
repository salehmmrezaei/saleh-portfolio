import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { ExperienceCarousel } from './ExperienceCarousel';

describe('ExperienceCarousel', () => {
  it('uses the stable company slug for the logo while showing the display name', () => {
    render(
      <ExperienceCarousel
        experiences={[{
          id: 1,
          company: 'CNR (ISMN)',
          company_slug: 'cnr',
          role: 'AI Engineer',
          start_date: '2025-11-01',
          end_date: '2026-08-31',
          skills: ['Python'],
          url: 'https://example.com',
          description: ['Built systems.'],
        }]}
      />,
    );

    expect(screen.getByText('CNR (ISMN)')).toBeInTheDocument();
    expect(screen.getByRole('img', { name: 'CNR (ISMN) logo' })).toBeInTheDocument();
  });
});
