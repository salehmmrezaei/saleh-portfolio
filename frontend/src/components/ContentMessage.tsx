import type { ContentStatus } from '../hooks/usePortfolioData';

export function ContentMessage({ status, label, count }: { status: ContentStatus; label: string; count: number }) {
  if (status === 'loading') return <p className="empty-state">Loading {label}...</p>;
  if (status === 'error') return <p className="empty-state">{label} are temporarily unavailable.</p>;
  if (count === 0) return <p className="empty-state">No {label} found.</p>;
  return null;
}
