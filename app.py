import streamlit as st
import time
import sys
import io
from contextlib import redirect_stdout

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · Multi-Agent Research",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

/* ── Root tokens ── */
:root {
    --bg:        #0d0a07;
    --surface:   #141008;
    --surface2:  #1a1409;
    --border:    #2a1f0f;
    --accent:    #ff6a00;
    --accent2:   #ff9a3c;
    --accentglow:#ff6a0044;
    --text:      #f0e6d8;
    --muted:     #7a6555;
    --warn:      #ffb347;
    --mono:      'Space Mono', monospace;
    --sans:      'Syne', sans-serif;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--sans) !important;
}

/* Streamlit container */
.block-container { max-width: 1100px; padding: 2rem 2rem 4rem; }

/* ── Header ── */
.rm-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.25rem;
}
.rm-logo {
    font-family: var(--mono);
    font-size: 1.8rem;
    color: var(--accent);
    letter-spacing: -1px;
    line-height: 1;
    text-shadow: 0 0 18px var(--accentglow);
}
.rm-title {
    font-family: var(--sans);
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: -1.5px;
    background: linear-gradient(135deg, #f0e6d8 20%, var(--accent) 60%, var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
}
.rm-sub {
    font-family: var(--mono);
    font-size: 0.72rem;
    color: var(--muted);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 2.5rem;
}

/* ── Search bar wrapper ── */
.rm-search-label {
    font-family: var(--mono);
    font-size: 0.7rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 6px;
}

/* Override streamlit text input */
div[data-testid="stTextInput"] > div > div > input {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    caret-color: var(--accent);
}
div[data-testid="stTextInput"] > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(255,106,0,0.15) !important;
}

/* ── Button ── */
div[data-testid="stButton"] > button {
    background: var(--accent) !important;
    color: #0a0c10 !important;
    font-family: var(--mono) !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.7rem 2rem !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}
div[data-testid="stButton"] > button:hover {
    background: var(--accent2) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(255,106,0,0.45) !important;
}
div[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── Pipeline steps ── */
.pipeline-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin: 2rem 0 1.5rem;
}
.step-card {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: 10px;
    padding: 1rem 0.9rem;
    transition: border-color 0.3s, box-shadow 0.3s;
    position: relative;
    overflow: hidden;
}
.step-card.active {
    border-color: var(--accent);
    box-shadow: 0 0 24px rgba(255,106,0,0.2);
}
.step-card.done {
    border-color: rgba(255,106,0,0.4);
    background: rgba(255,106,0,0.05);
}
.step-card.error {
    border-color: #ef4444;
    box-shadow: 0 0 16px rgba(239,68,68,0.15);
}
.step-num {
    font-family: var(--mono);
    font-size: 0.6rem;
    color: var(--muted);
    letter-spacing: 2px;
    margin-bottom: 6px;
}
.step-icon { font-size: 1.4rem; margin-bottom: 6px; }
.step-label {
    font-family: var(--sans);
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 4px;
}
.step-desc {
    font-family: var(--mono);
    font-size: 0.62rem;
    color: var(--muted);
    line-height: 1.4;
}
.step-status {
    font-family: var(--mono);
    font-size: 0.65rem;
    margin-top: 8px;
}
.step-status.running { color: var(--accent); }
.step-status.done    { color: var(--accent); }
.step-status.error   { color: #ef4444; }
.step-status.idle    { color: var(--muted); }

/* Pulse ring for active step */
.step-card.active::before {
    content: '';
    position: absolute;
    top: -1px; right: -1px; bottom: -1px; left: -1px;
    border-radius: 10px;
    background: transparent;
    border: 2px solid var(--accent);
    animation: pulse-ring 1.4s ease-out infinite;
}
@keyframes pulse-ring {
    0%   { opacity: 1; }
    70%  { opacity: 0.2; }
    100% { opacity: 0; }
}

/* ── Result panels ── */
.result-panel {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: 10px;
    padding: 1.25rem 1.4rem;
    margin-bottom: 1rem;
}
.result-panel-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 0.75rem;
}
.result-panel-icon { font-size: 1.1rem; }
.result-panel-title {
    font-family: var(--sans);
    font-weight: 700;
    font-size: 0.9rem;
    letter-spacing: 0.5px;
}
.result-panel-tag {
    font-family: var(--mono);
    font-size: 0.6rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    background: rgba(255,106,0,0.12);
    color: var(--accent2);
    padding: 2px 8px;
    border-radius: 99px;
    margin-left: auto;
}
.result-content {
    font-family: var(--mono);
    font-size: 0.78rem;
    line-height: 1.7;
    color: #c8cad8;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 280px;
    overflow-y: auto;
    border-top: 1px solid var(--border);
    padding-top: 0.75rem;
}
.result-content::-webkit-scrollbar { width: 4px; }
.result-content::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

/* ── Report panel (special) ── */
.report-panel {
    background: linear-gradient(135deg, #141008 0%, #1a1005 100%);
    border: 1.5px solid rgba(255,106,0,0.35);
    border-radius: 12px;
    padding: 1.5rem 1.6rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 30px rgba(255,106,0,0.08);
}
.report-panel-title {
    font-family: var(--sans);
    font-weight: 800;
    font-size: 1.05rem;
    letter-spacing: -0.5px;
    color: var(--accent2);
    margin-bottom: 1rem;
}
.report-content {
    font-family: var(--mono);
    font-size: 0.79rem;
    line-height: 1.8;
    color: #e0cebc;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 500px;
    overflow-y: auto;
}
.report-content::-webkit-scrollbar { width: 4px; }
.report-content::-webkit-scrollbar-thumb { background: rgba(255,106,0,0.3); border-radius: 4px; }

/* ── Critic panel ── */
.critic-panel {
    background: rgba(245,158,11,0.04);
    border: 1.5px solid rgba(245,158,11,0.25);
    border-radius: 10px;
    padding: 1.25rem 1.4rem;
    margin-bottom: 1rem;
}
.critic-panel-title {
    font-family: var(--sans);
    font-weight: 700;
    font-size: 0.9rem;
    color: var(--warn);
    margin-bottom: 0.75rem;
}
.critic-content {
    font-family: var(--mono);
    font-size: 0.78rem;
    line-height: 1.7;
    color: #e6c98a;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 280px;
    overflow-y: auto;
}

/* ── Success banner ── */
.success-banner {
    background: rgba(255,106,0,0.08);
    border: 1px solid rgba(255,106,0,0.35);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 1.5rem;
    font-family: var(--mono);
    font-size: 0.8rem;
    color: var(--accent2);
    letter-spacing: 0.5px;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 2rem 0 !important; }

/* ── Expander ── */
details summary { font-family: var(--mono) !important; font-size: 0.78rem !important; color: var(--muted) !important; }
details { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; padding: 0.5rem 1rem !important; }

/* ── Download button ── */
div[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    color: var(--accent2) !important;
    border: 1.5px solid var(--accent) !important;
    font-family: var(--mono) !important;
    font-size: 0.75rem !important;
    letter-spacing: 1px !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.2s !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: rgba(255,106,0,0.12) !important;
    box-shadow: 0 0 16px rgba(255,106,0,0.3) !important;
}

/* ── Spinner override ── */
div[data-testid="stSpinner"] > div {
    border-top-color: var(--accent) !important;
}

/* hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="rm-header">
    <div class="rm-logo">◈</div>
    <div class="rm-title">ResearchMind</div>
</div>
<div class="rm-sub">multi-agent research pipeline · powered by langchain</div>
""", unsafe_allow_html=True)


# ── Session state init ─────────────────────────────────────────────────────────
for key in ["state", "step_states", "running", "done", "error_msg"]:
    if key not in st.session_state:
        st.session_state[key] = None

if st.session_state.step_states is None:
    st.session_state.step_states = {1: "idle", 2: "idle", 3: "idle", 4: "idle"}


# ── Pipeline step cards ────────────────────────────────────────────────────────
STEPS = [
    (1, "🔍", "Search Agent",    "Finds recent & reliable sources across the web"),
    (2, "📖", "Reader Agent",    "Scrapes & extracts insights from top URLs"),
    (3, "✍️",  "Writer Chain",   "Drafts a structured research report"),
    (4, "🔎", "Critic Chain",    "Reviews quality and flags improvements"),
]

STATUS_LABEL = {
    "idle":    "— waiting",
    "running": "⟳ running...",
    "done":    "✓ complete",
    "error":   "✗ failed",
}

def render_pipeline_cards():
    ss = st.session_state.step_states or {1:"idle",2:"idle",3:"idle",4:"idle"}
    cards_html = '<div class="pipeline-grid">'
    for num, icon, label, desc in STEPS:
        status = ss.get(num, "idle")
        cls = "active" if status == "running" else ("done" if status == "done" else ("error" if status == "error" else ""))
        cards_html += f"""
        <div class="step-card {cls}">
            <div class="step-num">STEP {num:02d}</div>
            <div class="step-icon">{icon}</div>
            <div class="step-label">{label}</div>
            <div class="step-desc">{desc}</div>
            <div class="step-status {status}">{STATUS_LABEL[status]}</div>
        </div>"""
    cards_html += '</div>'
    return cards_html

pipeline_placeholder = st.empty()
pipeline_placeholder.markdown(render_pipeline_cards(), unsafe_allow_html=True)


# ── Input row ─────────────────────────────────────────────────────────────────
st.markdown('<div class="rm-search-label">Research Topic</div>', unsafe_allow_html=True)
col_input, col_btn = st.columns([5, 1])
with col_input:
    topic = st.text_input(
        label="topic",
        placeholder="e.g.  Retrieval-Augmented Generation in production systems",
        label_visibility="collapsed",
        key="topic_input",
    )
with col_btn:
    run_btn = st.button("▶  Run", use_container_width=True)


# ── Results placeholders ───────────────────────────────────────────────────────
results_placeholder = st.empty()


# ── Run pipeline ──────────────────────────────────────────────────────────────
def set_step(n, status):
    st.session_state.step_states[n] = status
    pipeline_placeholder.markdown(render_pipeline_cards(), unsafe_allow_html=True)


if run_btn and topic.strip():
    st.session_state.state = {}
    st.session_state.step_states = {1:"idle",2:"idle",3:"idle",4:"idle"}
    st.session_state.done = False
    st.session_state.error_msg = None

    try:
        from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain
    except ImportError as e:
        st.error(f"⚠️  Could not import agents module: `{e}`  \nMake sure `agents.py` is in the same directory as `app.py`.")
        st.stop()

    # ── STEP 1 ────────────────────────────────────────────────────────────
    set_step(1, "running")
    results_placeholder.empty()

    try:
        with st.spinner("Search agent is working…"):
            search_agent = build_search_agent()
            search_result = search_agent.invoke({
                "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
            })
        st.session_state.state["search_results"] = search_result["messages"][-1].content
        set_step(1, "done")
    except Exception as e:
        set_step(1, "error")
        st.session_state.error_msg = str(e)
        st.error(f"Search agent failed: {e}")
        st.stop()

    # ── STEP 2 ────────────────────────────────────────────────────────────
    set_step(2, "running")

    try:
        with st.spinner("Reader agent scraping top resources…"):
            reader_agent = build_reader_agent()
            reader_result = reader_agent.invoke({
                "messages": [("user", f"""
Use the scrape_url tool.
From the search results below:
1. Find the most relevant VALID URL
2. Use the scrape_url tool on that URL
3. Extract important insights and detailed information
4. Return clean summarized content

Search Results:
{st.session_state.state['search_results']}
""")]
            })
        st.session_state.state["scraped_content"] = reader_result["messages"][-1].content
        set_step(2, "done")
    except Exception as e:
        set_step(2, "error")
        st.session_state.error_msg = str(e)
        st.error(f"Reader agent failed: {e}")
        st.stop()

    # ── STEP 3 ────────────────────────────────────────────────────────────
    set_step(3, "running")

    try:
        with st.spinner("Writer drafting the research report…"):
            research_combined = (
                f"SEARCH RESULTS:\n{st.session_state.state['search_results'][:1000]}\n\n"
                f"SCRAPED CONTENT:\n{st.session_state.state['scraped_content'][:1000]}"
            )
            st.session_state.state["report"] = writer_chain.invoke({
                "topic": topic,
                "research": research_combined,
            })
        # save report.txt
        with open("report.txt", "w", encoding="utf-8") as f:
            f.write(st.session_state.state["report"])
        set_step(3, "done")
    except Exception as e:
        set_step(3, "error")
        st.session_state.error_msg = str(e)
        st.error(f"Writer chain failed: {e}")
        st.stop()

    # ── STEP 4 ────────────────────────────────────────────────────────────
    set_step(4, "running")

    try:
        with st.spinner("Critic reviewing the report…"):
            st.session_state.state["feedback"] = critic_chain.invoke(
                {"report": st.session_state.state["report"]}
            )
        set_step(4, "done")
    except Exception as e:
        set_step(4, "error")
        st.session_state.error_msg = str(e)
        st.error(f"Critic chain failed: {e}")
        st.stop()

    st.session_state.done = True


elif run_btn and not topic.strip():
    st.warning("Please enter a research topic before running.")


# ── Display results ───────────────────────────────────────────────────────────
if st.session_state.done and st.session_state.state:
    s = st.session_state.state

    results_placeholder.markdown("""
    <div class="success-banner">
        <span style="font-size:1.2rem">✅</span>
        Research pipeline completed successfully — all 4 agents finished.
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs for results ──
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Search Results", "📖 Scraped Content", "📄 Report", "🔎 Critic Feedback"])

    with tab1:
        st.markdown('<div class="result-panel"><div class="result-panel-header"><span class="result-panel-icon">🔍</span><span class="result-panel-title">Search Agent Output</span><span class="result-panel-tag">STEP 01</span></div>'
                    f'<div class="result-content">{s.get("search_results","—")}</div></div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="result-panel"><div class="result-panel-header"><span class="result-panel-icon">📖</span><span class="result-panel-title">Reader Agent Output</span><span class="result-panel-tag">STEP 02</span></div>'
                    f'<div class="result-content">{s.get("scraped_content","—")}</div></div>', unsafe_allow_html=True)

    with tab3:
        report_text = s.get("report", "")
        st.markdown(f'<div class="report-panel"><div class="report-panel-title">📄 Final Research Report</div>'
                    f'<div class="report-content">{report_text}</div></div>', unsafe_allow_html=True)
        st.download_button(
            label="⬇  Download report.txt",
            data=report_text,
            file_name="report.txt",
            mime="text/plain",
        )

    with tab4:
        st.markdown('<div class="critic-panel"><div class="critic-panel-title">🔎 Critic Feedback</div>'
                    f'<div class="critic-content">{s.get("feedback","—")}</div></div>', unsafe_allow_html=True)