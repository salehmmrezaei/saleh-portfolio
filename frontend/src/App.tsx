import { useState, useEffect } from 'react';

interface Project {
  id: number;
  name: string;
  skills: string[];
  url: string;
  description: string[];
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
        <h3 className="text-2xl font-semibold border-b pb-2 mb-4">Education</h3>
        <p><strong>Master's Student in AI</strong> - University of Bologna</p>
      </section>

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
        <div className="space-y-6">
          {projects.length > 0 ? (
            projects.map((project) => (
              <div key={project.id} className="border p-4 rounded-lg shadow-sm">
                <h4 className="text-xl font-bold">
                  <a href={project.url} target="_blank" rel="noreferrer" className="text-blue-600 hover:underline">
                    {project.name}
                  </a>
                </h4>
                <div className="flex flex-wrap gap-2 my-2">
                  {project.skills.map(skill => (
                    <span key={skill} className="bg-gray-200 text-sm px-2 py-1 rounded">{skill}</span>
                  ))}
                </div>
                <ul className="list-disc list-inside space-y-1 mt-2 text-gray-700">
                  {project.description.map((line, index) => (
                    <li key={index}>{line}</li>
                  ))}
                </ul>
              </div>
            ))
          ) : (
            <p>Loading projects from backend...</p>
          )}
        </div>
      </section>
    </main>
  );
}