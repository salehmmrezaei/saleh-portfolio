interface IconProps {
  className?: string;
}

import githubIcon from '../assets/github.svg';
import gmailIcon from '../assets/gmail.svg';
import homeIcon from '../assets/home.svg';
import linkedinIcon from '../assets/linkedin.svg';
import contactIcon from '../assets/mail-and-phone.svg';

export function LinkedInIcon({ className }: IconProps) {
  return <img className={className} src={linkedinIcon} alt="" aria-hidden="true" />;
}

export function GitHubIcon({ className }: IconProps) {
  return <img className={className} src={githubIcon} alt="" aria-hidden="true" />;
}

export function MailIcon({ className }: IconProps) {
  return <img className={className} src={gmailIcon} alt="" aria-hidden="true" />;
}

export function ContactIcon({ className }: IconProps) {
  return <img className={className} src={contactIcon} alt="" aria-hidden="true" />;
}

export function ChatBubbleIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="M7 18.5 3.5 20V6.5A2.5 2.5 0 0 1 6 4h12a2.5 2.5 0 0 1 2.5 2.5v8A2.5 2.5 0 0 1 18 17H7Z" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M8.5 9.5h7M8.5 12.5h5" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
    </svg>
  );
}

export function HomeIcon({ className }: IconProps) {
  return <img className={className} src={homeIcon} alt="" aria-hidden="true" />;
}

export function HomeButton({ onClick }: { onClick: () => void }) {
  return <a className="section-home" href="#home" onClick={(event) => { event.preventDefault(); onClick(); }} aria-label="Back to home"><HomeIcon /></a>;
}

export function ArrowIcon({ direction = 'right', className }: IconProps & { direction?: 'left' | 'right' }) {
  return <svg className={className} viewBox="0 0 24 24" aria-hidden="true"><path d={direction === 'left' ? 'M19 12H5m6-6-6 6 6 6' : 'M5 12h14m-6-6 6 6-6 6'} /></svg>;
}

export function ExternalLinkIcon({ className }: IconProps) {
  return <svg className={className} viewBox="0 0 24 24" aria-hidden="true"><path d="M14 5h5v5M19 5l-8 8M18 13v5a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5" /></svg>;
}
