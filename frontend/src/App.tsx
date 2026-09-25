import { useState, useEffect } from 'react';

interface Project {
  id: number;
  name: string;
  description: string;
}

export default function App() {
  const [projects, setProjects] = useState<Project[]>([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/projects')
      .then((response) => response.json())
      .then((data) => setProjects(data))
      .catch((error) => console.error("Error fetching projects:", error));
  }, []);

  return (
    <main className="p-8 font-sans max-w-3xl mx-auto text-left">
      <header className="mb-10">
        <h1 className="text-4xl font-bold">Saleh Rezaei</h1>
        <h2 className="text-xl text-gray-600 mt-2">AI/ML Engineer | LLMs</h2>
      </header>

      <section className="mb-8">
        <h3 className="text-2xl font-semibold border-b pb-2 mb-4">Experience</h3>
        <ul className="space-y-4 list-disc list-inside">
          <li><strong>AI Engineer</strong> at CNR (ISMN)</li>
          <li><strong>R&D AI Engineer</strong> at Zutre</li>
          <li><strong>Software Engineer</strong> at Denxa</li>
        </ul>
      </section>

      <section className="mb-8">
        <h3 className="text-2xl font-semibold border-b pb-2 mb-4">Projects</h3>
        <ul className="space-y-4 list-disc list-inside">
          {projects.length > 0 ? (
            projects.map((project) => (
              <li key={project.id}>
                <strong>{project.name}</strong> - {project.description}
              </li>
            ))
          ) : (
            <li>Loading projects from backend...</li>
          )}
        </ul>
      </section>
    </main>
  );
}