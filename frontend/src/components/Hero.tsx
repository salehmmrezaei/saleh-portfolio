import { ContactIcon, GitHubIcon, LinkedInIcon, MailIcon } from './Icons';
import profileImage from '../assets/profile.png';

interface HeroProps {
  visibleText: string;
}

export function Hero({ visibleText }: HeroProps) {
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
    </section>
  );
}
