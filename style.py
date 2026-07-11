STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,500&display=swap');

:root {
  /* Starbucks-inspired warm café palette — cream canvas anchoring a
     four-tier green system, with gold reserved for ceremony accents only. */
  --bg: #F2F0EB;           /* Neutral Warm — the load-bearing cream canvas */
  --surface: #FFFFFF;       /* white card / chat-panel surface */
  --surface-soft: #EDEBE9;  /* Ceramic — warmer wash for nested message cards */

  --ink: rgba(0, 0, 0, 0.87);   /* Text Black — warm 87% black, never pure */
  --muted: rgba(0, 0, 0, 0.58); /* Text Black Soft — secondary/metadata */
  --line: #E1DED4;              /* warm hairline that reads on cream */

  /* Four-tier green, each mapped to a surface role (not one "brand green") */
  --primary: #00754A;       /* Green Accent — interactive: labels, focus, CTA */
  --primary-dark: #006241;  /* Starbucks Green — headings */
  --primary-soft: #D4E9E2;  /* Green Light — hover / active tints */

  /* Gold — Starbucks reserves this for ceremony; here, sparing accent only */
  --accent: #CBA258;
  --accent-soft: #FAF6EE;   /* Gold Lightest — cream-gold wash */

  /* Refusal / outside-verified-facts notice — warm gold-brown, readable */
  --warning: #8A6A2E;
  --warning-soft: #FAF6EE;
}


/* Page */
html, body, [data-testid="stAppViewContainer"] {
  background-color: var(--bg);
  color: var(--ink);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  /* SoDoSans reads slightly compressed; Inter (its substitute) gets the same
     tight -0.01em tracking to keep that confident, café-signage voice. */
  letter-spacing: -0.01em;
}

/* The top chrome (Deploy button, menu) is disabled via client.toolbarMode in
   config.toml; this just collapses the now-empty header bar's reserved space. */
[data-testid="stHeader"] {
  height: 2.5rem;
  background: transparent;
}


/* Layout */
.block-container {
  max-width: 700px;
  padding-top: 1.5rem;
  padding-bottom: 2rem;
}


/* Sidebar navigation */
[data-testid="stSidebar"] {
  background: var(--surface);
  border-right: 1px solid var(--line);
}

[data-testid="stSidebarNavLink"] {
  border-radius: 8px;
  color: var(--muted) !important;
  font-weight: 500;
}

[data-testid="stSidebarNavLink"]:hover {
  background: var(--primary-soft) !important;
}

[data-testid="stSidebarNavLink"][aria-current="page"] {
  background: var(--primary-soft) !important;
  color: var(--primary-dark) !important;
  font-weight: 700;
}


/* WilOS branding */
.wilos-title {
  font-family: 'Fraunces', Georgia, serif;
  font-size: 2.6rem;
  font-weight: 500;
  letter-spacing: -0.06em;
  line-height: 1;
  color: var(--ink);
  margin-bottom: 0.4rem;
}

.wilos-title span {
  font-size: 1.25em;
  font-weight: 700;
  color: #3F7623;  /* Fidelity green — the "OS" wordmark accent */
  letter-spacing: -0.05em;
}

/* Chat-mode wordmark: same treatment as the hero, just a little more room
   before the conversation panel. */
.wilos-title--chat {
  margin-bottom: 1rem;
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
  color: var(--primary-dark);
}

/* The "WilOS" page title in chat mode — tighter than Streamlit's default
   heading margins so the conversation panel starts right under it. */
[data-testid="stHeading"] h1 {
  margin: 0 0 1rem;
}


/* Text */
.stMarkdown p {
  color: var(--muted);
  line-height: 1.65;
}


/* Chat panel: gives the transcript a defined boundary instead of loose
   bubbles floating on the page background. */
.st-key-wilos_chat_panel {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 1.25rem 1.25rem 0.25rem;
  /* Whisper-soft dual shadow (Starbucks card spec) — flat-plus-hint-of-lift,
     never a single heavy drop shadow. */
  box-shadow: 0 0 0.5px rgba(0, 0, 0, 0.14), 0 1px 1px rgba(0, 0, 0, 0.24);
}

.st-key-wilos_chat_panel [data-testid="stChatMessage"]:last-child {
  margin-bottom: 0;
}

/* Chat cards — nested inside the white panel, so they use the warmer Ceramic
   wash and stay flat (borders, no own shadow) per the nested-content rule. */
[data-testid="stChatMessage"] {
  background: var(--surface-soft);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 1rem 1.2rem;
  margin-bottom: 0.9rem;
}


/* Wil label */
.askwil-label {
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--primary);
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
  border-left-color: var(--primary);
  background: var(--primary-soft);
  color: var(--muted);
}


.askwil-marker--refusal {
  border-left-color: var(--warning);
  background: var(--warning-soft);
  color: var(--warning);
  font-weight: 600;
}


/* Prompt buttons — Starbucks full-pill (50px) with the signature
   scale(0.95) active press. */
.stButton button {
  width: 100%;
  min-height: 46px;
  border-radius: 50px !important;
  border: 1px solid var(--line) !important;
  background: var(--surface) !important;
  color: var(--primary-dark) !important;
  font-weight: 600;
  transition: all 0.2s ease;
}


.stButton button:hover {
  background: var(--primary-soft) !important;
  border-color: var(--primary) !important;
}


.stButton button:active {
  transform: scale(0.95);
}


/* Chat input */
[data-testid="stChatInput"] {
  border-radius: 14px;
}


/* Focus accessibility */
.stButton button:focus-visible,
textarea:focus-visible,
input:focus-visible {
  outline: 2px solid var(--primary) !important;
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
  box-shadow: 0 0 0.5px rgba(0, 0, 0, 0.14), 0 1px 1px rgba(0, 0, 0, 0.24);
}


.wilos-flow-arrow {
  text-align: center;
  color: var(--muted);
}


/* Quick-action pill row, shared by the empty-state hero and the persistent
   bottom bar — same column/button treatment in both places. */
.st-key-wilos_hero [data-testid="stHorizontalBlock"],
.st-key-wilos_bottom [data-testid="stHorizontalBlock"] {
  justify-content: center !important;
  gap: 0.5rem !important;
  flex-wrap: wrap !important;
  width: auto !important;
}

.st-key-wilos_bottom [data-testid="stHorizontalBlock"] {
  margin: 0.6rem auto 0 !important;
}

.st-key-wilos_hero [data-testid="stColumn"],
.st-key-wilos_bottom [data-testid="stColumn"] {
  width: fit-content !important;
  flex: 0 0 auto !important;
  min-width: 0 !important;
}

.st-key-wilos_hero .stButton button,
.st-key-wilos_bottom .stButton button {
  width: auto !important;
  padding-left: 1.1rem;
  padding-right: 1.1rem;
}


/* Centered landing hero (empty-state only) */
.st-key-wilos_hero {
  display: flex !important;
  flex-direction: column !important;
  justify-content: center !important;
  align-items: center !important;
  min-height: 35vh !important;
  text-align: center !important;
}

.st-key-wilos_hero [data-testid="stMarkdownContainer"],
.st-key-wilos_hero [data-testid="stMarkdownContainer"] p {
  text-align: center !important;
}

.st-key-wilos_hero [data-testid="stChatInput"] {
  width: 100% !important;
  margin: 1.5rem 0 1.25rem !important;
}


/* Mobile */
@media (max-width: 640px) {

  .block-container {
    padding-left: 1rem;
    padding-right: 1rem;
  }

  .wilos-title {
    font-size: 2.1rem;
  }

}


/* Accessibility: respect reduced-motion preference */
@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
}

</style>
"""
