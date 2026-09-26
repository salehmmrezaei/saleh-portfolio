import { useEffect, useState } from 'react';
import { ContactIcon, GitHubIcon, HomeButton, LinkedInIcon, MailIcon } from './Icons';
import profileImage from '../assets/profile.png';

interface HeroProps {
  onBackHome: () => void;
}

const rotatingLines = ['Hi, the name\'s Saleh', 'I build intelligent products.', 'I make AI feel useful.'];

export function Hero({ onBackHome }: HeroProps) {
  const [lineIndex, setLineIndex] = useState(0);
  const [visibleText, setVisibleText] = useState('');
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    const line = rotatingLines[lineIndex];
    const complete = visibleText === line;
    const timer = window.setTimeout(() => {
      const next = isDeleting ? line.slice(0, visibleText.length - 1) : line.slice(0, visibleText.length + 1);
      setVisibleText(next);
      if (!isDeleting && next === line) setIsDeleting(true);
      if (isDeleting && next === '') { setIsDeleting(false); setLineIndex((index) => (index + 1) % rotatingLines.length); }
    }, isDeleting ? 45 : complete ? 1500 : 85);
    return () => window.clearTimeout(timer);
  }, [isDeleting, lineIndex, visibleText]);

  return (
    <section className="hero snap-section" id="home">
      <nav className="topbar" aria-label="Primary navigation">
        <div className="social-links">
          <a className="linkedin-link" href="https://www.linkedin.com/in/salehmmrezaei/" target="_blank" rel="noreferrer" aria-label="LinkedIn"><LinkedInIcon /></a>
          <a className="github-link" href="https://github.com/salehmmrezaei" target="_blank" rel="noreferrer" aria-label="GitHub"><GitHubIcon /></a>
          <a className="email-link" href="mailto:salehmmrezaei@gmail.com" aria-label="Email"><MailIcon /></a>
        </div>
        <a className="contact-corner" href="#contact"><ContactIcon /> Get in touch</a>
      </nav>
      <div className="hero-orbit orbit-one" /><div className="hero-orbit orbit-two" /><div className="hero-orbit orbit-three" />
      <div className="hero-content">
        <img className="avatar" src={profileImage} alt="Saleh Rezaei" />
        <p className="eyebrow">AI / ML ENGINEER</p>
        <h1>{visibleText}<span className="cursor" aria-hidden="true" /></h1>
        <nav className="hero-navigation" aria-label="Portfolio sections">
          <a href="#about">About me</a><a href="#experience">My experiences</a><a href="#projects">My projects</a><a href="#skills">Skills</a><a href="#contact">Contact me</a>
        </nav>
      </div>
      <HomeButton onClick={onBackHome} />
    </section>
  );
}
