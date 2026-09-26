import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { ContentMessage } from './ContentMessage';

describe('ContentMessage', () => {
  it('renders loading and error states', () => {
    const { rerender } = render(<ContentMessage status="loading" label="projects" count={0} />);
    expect(screen.getByText('Loading projects...')).toBeInTheDocument();

    rerender(<ContentMessage status="error" label="projects" count={0} />);
    expect(screen.getByText('projects are temporarily unavailable.')).toBeInTheDocument();
  });
});
