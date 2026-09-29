import { HomeButton } from './Icons';
import aboutPhoto from '../assets/about-photo.jpg';

export function AboutSection({ onBackHome }: { onBackHome: () => void }) {
  return (
    <section className="content-section about-section snap-section" id="about">
      <div className="about-visual">
        <div className="section-heading"><p className="eyebrow">A LITTLE ABOUT ME</p><h2><span className="heading-line">Curious by nature.</span><br /><em>Builder by choice.</em></h2></div>
        <img className="about-photo" src={aboutPhoto} alt="Saleh exploring a forest trail" />
      </div>
      <div className="about-copy about-copy-desktop">
        <p>Hey 👋 I’m Saleh, an AI Engineer based in Italy with a background in both artificial intelligence and software engineering.
          I completed my M.Sc. in Artificial Intelligence at the University of Bologna, and my work has focused on building practical AI systems with LLMs, RAG, AI agents, NLP, and machine learning.</p>
        <p>I enjoy turning ideas and prototypes into reliable applications, whether that means designing RAG pipelines, building agentic workflows, developing Python/FastAPI backends, or experimenting with new models and evaluation methods.</p>
        <p>Outside of work, I’m always exploring new AI tools, improving my projects, and learning how to build better systems that are useful, scalable, and production-ready.</p>
      </div>
      <p className="about-copy about-copy-mobile">
        Hey 👋 I’m Saleh, an AI Engineer based in Italy with an M.Sc. in Artificial Intelligence from the University of Bologna.
        I build practical AI systems with LLMs, RAG, AI agents, NLP, and machine learning—turning ideas into reliable, production-ready applications.      </p>
      <HomeButton onClick={onBackHome} />
    </section>
  );
}
