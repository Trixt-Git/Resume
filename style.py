STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Fraunces:opsz,wght@9..144,500&display=swap');

:root {
  --bg: #FAFBF9;
  --surface: #FFFFFF;
  --ink: #14251A;
  --muted: #55665C;
  --line: #E1E8E2;
  --accent: #3F7623;
  --refusal: #B4842A;
}

html, body, [data-testid="stAppViewContainer"] {
  background-color: var(--bg);
  color: var(--ink);
  font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif;
}

.block-container {
  max-width: 720px;
  padding-top: 2rem;
}

h1, h2 {
  font-family: 'Fraunces', Georgia, serif;
  font-weight: 500;
  color: var(--ink);
}

.askwil-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 2px;
}

.askwil-marker {
  font-size: 0.75rem;
  margin-top: 6px;
  padding-left: 10px;
  border-left: 3px solid var(--line);
}

.askwil-marker--source {
  border-left-color: var(--accent);
  color: var(--muted);
}

.askwil-marker--refusal {
  border-left-color: var(--refusal);
  color: var(--refusal);
  font-weight: 600;
}

.stButton button {
  border-radius: 10px !important;
  border: 1px solid var(--line) !important;
  min-height: 44px;
}

.stButton button:focus-visible,
textarea:focus-visible,
input:focus-visible {
  outline: 2px solid var(--accent) !important;
  outline-offset: 2px;
}

.askwil-flow {
  display: flex;
  flex-direction: column;
  gap: 0;
  margin: 1rem 0;
}

.askwil-flow-step {
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 10px 14px;
  background: var(--surface);
  font-size: 0.95rem;
}

.askwil-flow-arrow {
  text-align: center;
  color: var(--muted);
  font-size: 1.1rem;
  padding: 2px 0;
}

@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
}
</style>
"""
