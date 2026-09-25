import './App.css'


function App() {
  return (
    <main className="p-8 font-sans max-w-3xl mx-auto">
      <header className="mb-10">
        <h1 className="text-4xl font-bold">Saleh Rezaei</h1>
        <h2 className="text-xl text-gray-600 mt-2">AI/ML Engineer | LLMs</h2>
      </header>

      <section className="mb-8">
        <h3 className="text-2xl font-semibold border-b pb-2 mb-4">Experience</h3>
        <ul className="space-y-4">
          <li>
            <strong>AI Engineer</strong> at CNR (ISMN)
          </li>
          <li>
            <strong>R&D AI Engineer</strong> at Zutre
          </li>
          <li>
            <strong>Software Engineer</strong> at Denxa
          </li>
        </ul>
      </section>

      <section className="mb-8">
        <h3 className="text-2xl font-semibold border-b pb-2 mb-4">Projects</h3>
        <ul className="space-y-4">
          <li>
            <strong>RepoPilot AI</strong> - Production-oriented codebase intelligence platform.
          </li>
          <li>
            <strong>Voice Notes AI</strong> - Local-first AI application for audio transcription.
          </li>
        </ul>
      </section>
    </main>
  );
}

export default App
