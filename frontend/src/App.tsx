import { useState, useEffect } from 'react';
import './index.css'; // Add this line back to restore Tailwind!

interface Project {
  id: number;
  name: string;
  skills: string[];
  url: string;
  description: string[];
}

interface Experience {
  id: number;
  company: string;
  role: string;
  start_date: string;
  end_date: string;
  skills: string[];
  url: string;
  description: string[];
}

interface Education {
  id: number;
  institution: string;
  degree: string;
  grade: string;
  start_date: string;
  end_date: string;
  country: string;
}

export default function App() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [experiences, setExperiences] = useState<Experience[]>([]);
  const [educations, setEducations] = useState<Education[]>([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/projects')
      .then((response) => response.json())
      .then((data) => setProjects(data))
      .catch((error) => console.error("Error fetching projects:", error));

    fetch('http://127.0.0.1:8000/api/experiences')
      .then((response) => response.json())
      .then((data) => setExperiences(data))
      .catch((error) => console.error("Error fetching experiences:", error));

    fetch('http://127.0.0.1:8000/api/educations')
      .then((response) => response.json())
      .then((data) => setEducations(data))
      .catch((error) => console.error("Error fetching educations:", error));
  }, []);

  return (
    <main className="p-8 font-sans max-w-3xl mx-auto text-left">
      <header className="mb-10">
        <h1 className="text-4xl font-bold">Saleh Rezaei</h1>
        <h2 className="text-xl text-gray-600 mt-2">AI/ML Engineer | LLMs</h2>
      </header>

      <section className="mb-8">
        <h3 className="text-2xl font-semibold border-b pb-2 mb-4">Education</h3>
        <div className="space-y-6">
          {educations.length > 0 ? (
            educations.map((edu) => (
              <div key={edu.id} className="border p-4 rounded-lg shadow-sm">
                <div className="flex justify-between items-baseline mb-1">
                  <h4 className="text-xl font-bold">{edu.degree}</h4>
                  <span className="text-sm text-gray-500">{edu.start_date} to {edu.end_date}</span>
                </div>
                <p className="text-gray-700"><strong>{edu.institution}</strong>, {edu.country}</p>
                <p className="text-sm text-gray-600 mt-1">Grade: {edu.grade}</p>
              </div>
            ))
          ) : (
            <p>Loading education from backend...</p>
          )}
        </div>
      </section>

      <section className="mb-8">
        <h3 className="text-2xl font-semibold border-b pb-2 mb-4">Experience</h3>
        <div className="space-y-6">
          {experiences.length > 0 ? (
            experiences.map((exp) => (
              <div key={exp.id} className="border p-4 rounded-lg shadow-sm">
                <div className="flex justify-between items-baseline mb-1">
                  <h4 className="text-xl font-bold">
                    <a href={exp.url} target="_blank" rel="noreferrer" className="text-blue-600 hover:underline">
                      {exp.role} at {exp.company}
                    </a>
                  </h4>
                  <span className="text-sm text-gray-500">{exp.start_date} to {exp.end_date}</span>
                </div>
                <div className="flex flex-wrap gap-2 my-2">
                  {exp.skills.map((skill, index) => (
                    <span key={index} className="bg-gray-200 text-sm px-2 py-1 rounded">{skill}</span>
                  ))}
                </div>
                <ul className="list-disc list-inside space-y-1 mt-2 text-gray-700">
                  {exp.description.map((line, index) => (
                    <li key={index}>{line}</li>
                  ))}
                </ul>
              </div>
            ))
          ) : (
            <p>Loading experiences from backend...</p>
          )}
        </div>
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
                  {project.skills.map((skill, index) => (
                    <span key={index} className="bg-gray-200 text-sm px-2 py-1 rounded">{skill}</span>
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