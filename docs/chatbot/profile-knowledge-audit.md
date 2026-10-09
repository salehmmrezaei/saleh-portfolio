# SECTION A — Evidence report

*Reviewed 2026-10-08. The deployed portfolio URL was not directly retrievable through the browsing interface; the linked, public GitHub source for the portfolio is the primary source for its displayed content.*

### Primary evidence

- Portfolio content, experience/education/skills: https://github.com/salehmmrezaei/saleh-portfolio/blob/main/frontend/src/data/portfolio.ts
- Portfolio about page: https://github.com/salehmmrezaei/saleh-portfolio/blob/main/frontend/src/components/AboutSection.tsx
- Portfolio contact links: https://github.com/salehmmrezaei/saleh-portfolio/blob/main/frontend/src/App.tsx
- Portfolio contact form: https://github.com/salehmmrezaei/saleh-portfolio/blob/main/frontend/src/components/ContactSection.tsx
- Professional profile summary: https://github.com/salehmmrezaei/salehmmrezaei/blob/main/README.md
- Public LinkedIn preview: https://www.linkedin.com/in/salehmmrezaei/
- Code-backed capability evidence: https://github.com/salehmmrezaei/repopilot-ai ; https://github.com/salehmmrezaei/voice-notes-ai ; https://github.com/salehmmrezaei/disagreement-aware-sexism-detection ; https://github.com/salehmmrezaei/reinforcement-learning-lab ; https://github.com/salehmmrezaei/tournament-scheduling-optimization ; https://github.com/salehmmrezaei/facebook-network-analysis

### Category-by-category

1. **Overview:** The portfolio's frontend heading, about page and SEO metadata identify Saleh Rezaei as an AI/ML engineer based in Italy with an M.Sc. in Artificial Intelligence; the GitHub profile README identifies him as a master's graduate in AI from Bologna. LinkedIn uses the fuller display name “Saleh Mir Mohammad Rezaei”; the requested professional display name “Saleh Rezaei” is adopted. No claim about nationality or citizenship is made.
2. **Experience:** `frontend/src/data/portfolio.ts` explicitly names four positions: **CNR (ISMN), AI Engineer, 2025-11 to 2026-08**; **Zutre, R&D AI Engineer, 2025-12 to 2026-06**; **Denxa, Software Engineer, 2022-12 to 2023-05**; and **Sulfate Shargh Co., Software Engineer Intern, 2022-01 to 2022-12**. Responsibilities and skills are edited down from that source. Public LinkedIn independently displays CNR in Bologna and other location rows but hides the remaining company/role details, so specific locations of the other three employers have not been attributed from those unlabeled rows. The CNR and Zutre dates overlap; their nature, hours and contract types were not publicly established and are not inferred.
3. **Education:** The portfolio source explicitly records **M.Sc. Artificial Intelligence, University of Bologna, 2024-09 to 2026-07**, and **B.Sc. Computer Engineering, University of Zanjan, 2017-09 to 2022-05**. The public LinkedIn view confirms the 2024–2026 Bologna record but shows an unnamed second education row of 2017–2021, which may conflict with the portfolio's 2022 end date; since the row is not visibly labeled, use the author's named and date-specific portfolio record conservatively. The source stores full dates that appear standardized; the knowledge base uses month-level precision to avoid implying the encoded first/last day is a verified actual attendance or graduation day.
4. **Skills:** RAG, Python, LangChain, AI agents, vector databases, prompt workflows and document extraction are tied to the portfolio's professional roles. FastAPI, PostgreSQL/pgvector, Redis, Celery, React, TypeScript, Docker, testing and CI are supported by implementation in the linked code repositories. PyTorch, Transformers, scikit-learn and forecasting have implementation/project support. Combinatorial optimization (CP/SAT/MIP), graph/network analysis and search-ranking algorithms are supported by corresponding repositories; no competitive-programming status is inferred. AWS appears on the portfolio's skills list but is **omitted** from the distilled strongest-skills structure because no concrete AWS engineering responsibility was independently confirmed. No skills are inferred only from lockfiles.
5. **Professional interests:** The user explicitly states broad AI positions across Europe, especially ML, LLMs, RAG, agents and NLP; these are marked `explicit`. The emphasis on production AI/backend engineering is `strongly_inferred` from several jobs and separately developed applications. Example roles are illustrative, not restrictive.
6. **Availability:** The user directly states **available to start immediately**. No notice period or condition is added; this first-person statement overrides absent public details.
7. **Work authorization:** The user directly states a valid Italy work permit and an expected **approximately three-month** path to Netherlands work authorization. The Netherlands status is *not* current permission. Other European countries remain *not specified*. No EU citizenship, EU-wide authorization, visa type, relocation or remote-work assertion is made.
8. **Personal interests:** The user directly states a hobby of working on algorithms and solving technical/problem-solving challenges. Repositories independently demonstrate optimization/graph-analysis activity, but the knowledge base does **not** claim competitive-programming achievements.
9. **Public links:** The portfolio, GitHub and LinkedIn links were explicitly provided and are also associated with the portfolio site. The public email **salehmmrezaei@gmail.com** is directly present as a `mailto:` link in `frontend/src/App.tsx`, and the site includes a `#contact` form. No phone number or other personal contact data is added.

### Not included

Salary expectations, preferred employment arrangement, relocation/remote preference, certifications, publications, dates for unverified positions, legal/immigration details beyond the direct statements, and detailed project architectures. Search results for the different domain `salehrezaei.com` and the LinkedIn slug `/in/salehrezaei/` were identified as belonging to a different profile and were excluded.

# SECTION B — Final Python definition

Use `backend/app/profile_knowledge.py` from the attached ZIP archive or the separate Python file. The definition contains the exact nine requested top-level keys and can be imported as `from app.profile_knowledge import PROFILE_KNOWLEDGE` when `backend` is on the Python import path.
