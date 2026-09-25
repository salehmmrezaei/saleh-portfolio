interface IconProps {
  className?: string;
}

export function LinkedInIcon({ className }: IconProps) {
  return <svg className={className} viewBox="0 0 24 24" aria-hidden="true"><path d="M5.2 8.3H2.8V21h2.4V8.3ZM4 3a1.8 1.8 0 1 0 0 3.6A1.8 1.8 0 0 0 4 3Zm5.1 5.3H6.8V21h2.3v-6.3c0-1.7.3-3.4 2.5-3.4s2.2 2 2.2 3.5V21h2.4v-7c0-3.4-.7-6-4.1-6-1.6 0-2.6.9-3 1.7h-.1V8.3Z" /></svg>;
}

export function GitHubIcon({ className }: IconProps) {
  return <svg className={className} viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5a9.5 9.5 0 0 0-3 18.5c.5.1.7-.2.7-.5v-1.8c-2.8.6-3.4-1.2-3.4-1.2-.5-1.1-1.1-1.4-1.1-1.4-.9-.6.1-.6.1-.6 1 0 1.5 1 1.5 1 .9 1.5 2.4 1.1 3 .8.1-.7.4-1.1.7-1.3-2.2-.3-4.5-1.1-4.5-4.8 0-1.1.4-2 1-2.7-.1-.3-.4-1.3.1-2.7 0 0 .8-.3 2.8 1a9.8 9.8 0 0 1 5.1 0c2-1.3 2.8-1 2.8-1 .5 1.4.2 2.4.1 2.7.6.7 1 1.6 1 2.7 0 3.7-2.3 4.5-4.5 4.8.4.3.7 1 .7 1.9v2.8c0 .3.2.6.7.5A9.5 9.5 0 0 0 12 2.5Z" /></svg>;
}

export function MailIcon({ className }: IconProps) {
  return <svg className={className} viewBox="0 0 24 24" aria-hidden="true"><path d="M3.5 5.5h17v13h-17v-13Z" /><path d="m4 6 8 6 8-6" /></svg>;
}

export function HomeIcon({ className }: IconProps) {
  return <svg className={className} viewBox="0 0 24 24" aria-hidden="true"><path d="m3.5 10.5 8.5-7 8.5 7v9h-5.5v-5h-6v5H3.5v-9Z" /></svg>;
}

export function ArrowIcon({ direction = 'right', className }: IconProps & { direction?: 'left' | 'right' }) {
  return <svg className={className} viewBox="0 0 24 24" aria-hidden="true"><path d={direction === 'left' ? 'M19 12H5m6-6-6 6 6 6' : 'M5 12h14m-6-6 6 6-6 6'} /></svg>;
}

export function ExternalLinkIcon({ className }: IconProps) {
  return <svg className={className} viewBox="0 0 24 24" aria-hidden="true"><path d="M14 5h5v5M19 5l-8 8M18 13v5a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5" /></svg>;
}
