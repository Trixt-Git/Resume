STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,500&display=swap');

:root {
  --bg: #F7F8F5;
  --surface: #FFFFFF;
  --ink: #17251B;
  --muted: #5C6B61;
  --line: #DCE5DB;

  /* Fidelity-inspired palette */
  --green: #2E7D32;
  --green-dark: #1B5E20;
  --green-soft: #EAF4EA;

  --gold: #A46F18;
  --gold-soft: #FBF4E3;
}


/* Page */
html, body, [data-testid="stAppViewContainer"] {
  background-color: var(--bg);
  color: var(--ink);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}


/* Layout */
.block-container {
  max-width: 760px;
  padding-top: 3rem;
  padding-bottom: 4rem;
}


/* WilOS branding */
.wilos-title {
  font-family: 'Fraunces', Georgia, serif;
  font-size: 3.4rem;
  font-weight: 500;
  letter-spacing: -0.06em;
  line-height: 1;
  color: var(--ink);
  margin-bottom: 0.4rem;
}

.wilos-title span {
  font-size: 1.25em;
  font-weight: 700;
  color: var(--green);
  letter-spacing: -0.05em;
}

.wilos-subtitle {
  color: var(--muted);
  font-size: 1rem;
  line-height: 1.6;
  max-width: 600px;
  margin-bottom: 2rem;
}


/* Headers */
h1, h2 {
  font-family: 'Fraunces', Georgia, serif;
  font-weight: 500;
  color: var(--green-dark);
}


/* Text */
.stMarkdown p {
  color: var(--muted);
  line-height: 1.65;
}


/* Chat cards */
[data-testid="stChatMessage"] {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 1rem 1.2rem;
  margin-bottom: 1rem;
}


/* Wil label */
.askwil-label {
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--green);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 0.5rem;
}


/* Citation markers */
.askwil-marker {
  margin-top: 0.8rem;
  padding: 0.5rem 0.8rem;
  border-left: 3px solid var(--line);
  border-radius: 6px;
  font-size: 0.78rem;
  line-height: 1.4;
}


.askwil-marker--source {
  border-left-color: var(--green);
  background: var(--green-soft);
  color: var(--muted);
}


.askwil-marker--refusal {
  border-left-color: var(--gold);
  background: var(--gold-soft);
  color: var(--gold);
  font-weight: 600;
}


/* Prompt buttons */
.stButton button {
  width: 100%;
  min-height: 46px;
  border-radius: 12px !important;
  border: 1px solid var(--line) !important;
  background: var(--surface) !important;
  color: var(--green-dark) !important;
  font-weight: 600;
  transition: all 0.15s ease;
}


.stButton button:hover {
  background: var(--green-soft) !important;
  border-color: var(--green) !important;
}


/* Chat input */
[data-testid="stChatInput"] {
  border-radius: 14px;
}


/* Focus accessibility */
.stButton button:focus-visible,
textarea:focus-visible,
input:focus-visible {
  outline: 2px solid var(--green) !important;
  outline-offset: 2px;
}


/* Optional timeline / flow components */
.wilos-flow {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin: 1.5rem 0;
}


.wilos-flow-step {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 0.9rem 1rem;
}


.wilos-flow-arrow {
  text-align: center;
  color: var(--muted);
}


/* Mobile */
@media (max-width: 640px) {

  .block-container {
    padding-left: 1rem;
    padding-right: 1rem;
  }

  .wilos-title {
    font-size: 2.6rem;
  }

}


/* Accessibility: respect reduced-motion preference */
@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
}

</style>
"""
