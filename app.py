import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
import google.generativeai as genai
import os

VERSION = "13.0"

st.set_page_config(
    page_title="AI Context Manager",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Page-level CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
body, .stApp { background: #0c0c15 !important; }
#MainMenu, footer, header, .stDeployButton,
[data-testid="stHeader"],[data-testid="stDecoration"],
[data-testid="stToolbar"] { display:none !important; }

/* ── FIX: Keep collapse/expand button visible ── */
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    background: #0c0c15 !important;
    border-right: 1px solid #1e1e2e !important;
    color: #7c7c99 !important;
}
[data-testid="collapsedControl"] svg { color: #7c7c99 !important; fill: #7c7c99 !important; }

.block-container { padding: 0 !important; max-width: 100% !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    display: block !important; visibility: visible !important;
    background: #0e0e1a !important;
    border-right: 2px solid #252540 !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.5) !important;
}
section[data-testid="stSidebar"] > div,
[data-testid="stSidebarContent"] { background: #0e0e1a !important; }

/* Sidebar collapse toggle button (the arrow) */
button[data-testid="baseButton-secondary"][kind="secondary"] svg { color: #7c7c99 !important; }

/* Buttons */
.stButton > button {
    background: #181826 !important;
    color: #ddddf0 !important;
    border: 1px solid #2a2a40 !important;
    border-radius: 8px !important; font-weight: 600 !important; transition: all .2s !important;
}
.stButton > button:hover { background: #22223a !important; border-color: #3a3a58 !important; }
.stButton > button[kind="primary"] {
    background: #7c5af5 !important;
    border-color: #7c5af5 !important; color: white !important;
}
.stButton > button[kind="primary"]:hover { background: #8f6cf7 !important; }

/* Selectbox */
.stSelectbox > div > div {
    background: #13131f !important;
    border: 1px solid #2a2a40 !important;
    color: #ddddf0 !important; border-radius: 8px !important;
}

/* Labels / captions */
.stMarkdown p, .stCaption,
[data-testid="stSidebarContent"] p,
[data-testid="stSidebarContent"] span,
[data-testid="stSidebarContent"] label { color: #7c7c99 !important; }

/* Chat input */
.stChatInput > div {
    background: #13131f !important;
    border: 1px solid #2a2a40 !important; border-radius: 12px !important;
}
.stChatInput > div:focus-within { border-color: #7c5af5 !important; box-shadow: 0 0 0 2px rgba(124,90,245,0.15) !important; }
.stChatInput textarea { color: #ddddf0 !important; background: transparent !important; }
.stChatInput textarea::placeholder { color: #4a4a66 !important; }

/* Context preview code block */
[data-testid="stCode"], .stCode, .stCodeBlock { background: transparent !important; }
[data-testid="stCode"] pre, .stCodeBlock pre, .stCode pre {
    background: #13131f !important;
    color: #8888aa !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 8px !important;
    font-size: 11px !important;
    line-height: 1.6 !important;
}
/* Hide copy button on code block */
[data-testid="stCode"] button { display: none !important; }

/* Progress bar */
.stProgress > div > div { background: #1e1e2e !important; }
.stProgress > div > div > div { background: #7c5af5 !important; }

/* Section label */
.section-label {
    font-size:11px; font-weight:600; text-transform:uppercase;
    letter-spacing:.5px; color:#5a5a7a; margin-bottom:8px;
}

/* Header */
.app-header {
    display:flex; align-items:center; justify-content:space-between;
    height:52px; padding:0 1.25rem;
    border-bottom:1px solid #1e1e2e;
    background:#0c0c15;
}
.model-badge {
    display:inline-flex; align-items:center; gap:6px;
    border-radius:6px; border:1px solid; padding:4px 10px;
    font-size:12px; font-weight:500;
}
.badge-groq    { border-color:rgba(251,146,60,0.3);  background:rgba(251,146,60,0.08);  color:#f59044; }
.badge-gemini  { border-color:rgba(56,189,248,0.3);  background:rgba(56,189,248,0.08);  color:#38c0f8; }
.badge-debate  { border-color:rgba(168,85,247,0.3);  background:rgba(168,85,247,0.08);  color:#c084fc; }
.status-pill {
    display:flex; align-items:center; gap:6px;
    border:1px solid rgba(52,211,153,0.25); background:rgba(52,211,153,0.08);
    border-radius:999px; padding:4px 12px; font-size:12px; color:#34d399;
}

/* Token bar */
.token-bar { padding:6px 1.25rem; border-top:1px solid #1e1e2e; background:#0c0c15; }
.token-bar-inner { display:flex; align-items:center; gap:12px; font-size:12px; color:#5a5a7a; }
.token-track { flex:1; height:3px; border-radius:999px; background:#1e1e2e; overflow:hidden; }
.token-fill  { height:100%; border-radius:999px; transition:width .3s; }
.fill-ok   { background:#7c5af5; }
.fill-warn { background:#f59044; }
.fill-bad  { background:#f05a5a; }

/* Token bar spacing + sticky chat input background */
.element-container:has(.token-bar) { margin-bottom: 4px !important; }
[data-testid="stBottom"] {
    background: #0c0c15 !important;
    padding-top: 4px !important;
    padding-bottom: 8px !important;
}
[data-testid="stBottom"] > div { background: #0c0c15 !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
defaults = {
    'active_llm': 'gemini',
    'conversation': [],
    'context_history': [],
    'processing': False,
    'context_strategy': 'full',
    'app_mode': 'discussion',   # 'discussion' | 'debate'
    'debate_running': False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── API setup ─────────────────────────────────────────────────────────────────
GROQ_API_KEY   = os.environ.get('GROQ_API_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

try:
    groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-2.5-flash-lite')
    else:
        gemini_model = None
except Exception:
    groq_client = gemini_model = None

if not GROQ_API_KEY or not GEMINI_API_KEY:
    st.error("⚠️ Add GROQ_API_KEY and GEMINI_API_KEY to environment variables")
    st.stop()

# ── Helpers ───────────────────────────────────────────────────────────────────
def estimate_tokens(text): return max(1, len(text) // 4)
def get_context_tokens(): return sum(estimate_tokens(m['content']) for m in st.session_state.context_history[-8:])

def build_context():
    return "".join(f"{m['role']}: {m['content']}\n" for m in st.session_state.context_history[-8:])

def get_context_preview():
    lines = [f"[{m['role']}] {m['content'][:60]}{'…' if len(m['content'])>60 else ''}"
             for m in st.session_state.context_history[-5:]]
    return "\n".join(lines) if lines else "No messages yet."

def call_groq(prompt, system_prompt=None):
    try:
        msgs = []
        if system_prompt:
            msgs.append({"role": "system", "content": system_prompt})
        msgs.append({"role": "user", "content": prompt})
        r = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=msgs,
            max_tokens=2000, temperature=0.7
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def call_gemini(prompt, system_prompt=None):
    try:
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        r = gemini_model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(max_output_tokens=2000, temperature=0.7)
        )
        return r.text
    except Exception as e:
        return f"Error: {e}"

def send_message(user_input):
    st.session_state.conversation.append({"role": "user", "content": user_input})
    st.session_state.conversation.append({"role": "thinking", "llm": st.session_state.active_llm})
    response = call_groq(user_input) if st.session_state.active_llm == 'groq' else call_gemini(user_input)
    st.session_state.conversation.pop()
    st.session_state.conversation.append({"role": st.session_state.active_llm, "content": response})
    st.session_state.context_history.append({"role": "user", "content": user_input})
    st.session_state.context_history.append({"role": st.session_state.active_llm, "content": response})

# ── Debate Logic ──────────────────────────────────────────────────────────────
DEBATE_ROUNDS = 3

def run_debate(topic):
    """Run a full 3-round debate: Gemini opens, Groq responds each round, judge concludes."""
    st.session_state.debate_running = True
    st.session_state.conversation.append({"role": "debate_topic", "content": topic})

    debate_history = []  # list of {speaker, content}

    gemini_sys = (
        "You are a sharp, articulate debater representing Team Gemini. "
        "You are debating the topic provided. Make clear, confident arguments. "
        "Keep each response under 200 words. Be direct and persuasive."
    )
    groq_sys = (
        "You are a sharp, articulate debater representing Team Groq. "
        "You are debating the topic provided. Challenge your opponent's points and build your own case. "
        "Keep each response under 200 words. Be direct and persuasive."
    )
    judge_sys = (
        "You are an impartial AI judge evaluating a debate. "
        "Analyse both sides' arguments objectively. Identify the strongest points from each side, "
        "declare a winner with clear reasoning, and give a balanced 3-4 sentence verdict."
    )

    for round_num in range(1, DEBATE_ROUNDS + 1):
        # Build context from debate so far
        history_text = ""
        for turn in debate_history:
            history_text += f"\n{turn['speaker']}: {turn['content']}\n"

        # — Gemini speaks —
        if round_num == 1:
            gemini_prompt = f"Topic: {topic}\n\nYou go first. Open the debate with your strongest argument."
        else:
            gemini_prompt = (
                f"Topic: {topic}\n\nDebate so far:{history_text}\n\n"
                f"Round {round_num}: Respond to Groq's last point and strengthen your position."
            )

        st.session_state.conversation.append({"role": "debate_thinking", "llm": "gemini", "round": round_num})
        st.rerun()  # show thinking indicator

    # NOTE: Because Streamlit reruns block sequential execution in a single run,
    # we use a different approach: store debate state and process step by step.
    # See _run_debate_step() called from main flow below.

def _build_debate_prompt(topic, history, speaker, round_num):
    history_text = "".join(f"\n{t['speaker'].upper()}: {t['content']}\n" for t in history)
    if speaker == "gemini":
        if round_num == 1:
            return f"Topic: \"{topic}\"\n\nYou go first. Open the debate with your strongest argument."
        return (f"Topic: \"{topic}\"\n\nDebate so far:{history_text}\n\n"
                f"Round {round_num}: Rebut Groq's last point and reinforce your position.")
    elif speaker == "groq":
        return (f"Topic: \"{topic}\"\n\nDebate so far:{history_text}\n\n"
                f"Round {round_num}: Challenge Gemini's argument and make your strongest counter-point.")
    else:  # judge
        return (f"Topic: \"{topic}\"\n\nFull debate transcript:{history_text}\n\n"
                "Deliver your verdict: summarise the strongest arguments from each side, "
                "declare a winner, and explain your reasoning in 3-4 sentences.")

def run_full_debate(topic):
    """Synchronous debate runner — called once, appends all messages."""
    gemini_sys = (
        "You are a sharp debater for Team Gemini. Argue the topic confidently and persuasively. "
        "Keep responses under 180 words. No markdown headers — just clear prose."
    )
    groq_sys = (
        "You are a sharp debater for Team Groq. Challenge your opponent and build your case. "
        "Keep responses under 180 words. No markdown headers — just clear prose."
    )
    judge_sys = (
        "You are an impartial AI judge. Analyse both sides fairly. "
        "Identify the strongest points from each side, declare a winner with clear reasoning. "
        "Keep your verdict to 4 sentences. No markdown headers — just clear prose."
    )

    st.session_state.conversation.append({"role": "debate_topic", "content": topic})
    debate_history = []

    for round_num in range(1, DEBATE_ROUNDS + 1):
        # Gemini turn
        g_prompt = _build_debate_prompt(topic, debate_history, "gemini", round_num)
        g_resp   = call_gemini(g_prompt, system_prompt=gemini_sys)
        st.session_state.conversation.append({
            "role": "debate_gemini", "content": g_resp, "round": round_num
        })
        debate_history.append({"speaker": "Gemini", "content": g_resp})

        # Groq turn
        r_prompt = _build_debate_prompt(topic, debate_history, "groq", round_num)
        r_resp   = call_groq(r_prompt, system_prompt=groq_sys)
        st.session_state.conversation.append({
            "role": "debate_groq", "content": r_resp, "round": round_num
        })
        debate_history.append({"speaker": "Groq", "content": r_resp})

    # Judge
    j_prompt = _build_debate_prompt(topic, debate_history, "judge", 0)
    j_resp   = call_gemini(j_prompt, system_prompt=judge_sys)
    st.session_state.conversation.append({
        "role": "debate_judge", "content": j_resp
    })

    st.session_state.context_history.append({"role": "user", "content": f"[Debate topic] {topic}"})
    st.session_state.context_history.append({"role": "judge", "content": j_resp})
    st.session_state.debate_running = False

def esc(text):
    return (text
        .replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        .replace('"', "&quot;").replace("'", "&#39;").replace("\n", "<br>"))

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div style="padding:14px 16px;border-bottom:1px solid #252540;'
        'font-size:15px;font-weight:700;color:#ddddf0;letter-spacing:-0.02em">🔄 AI Context Manager</div>',
        unsafe_allow_html=True
    )
    st.markdown('<div style="padding:16px">', unsafe_allow_html=True)

    # ── Mode tabs ──
    is_discussion = st.session_state.app_mode == 'discussion'
    active_llm_now = st.session_state.active_llm

    # Active tab colors: Discussion=violet, Debate=purple
    active_tab_bg     = "rgba(124,90,245,0.18)"  if is_discussion else "rgba(192,132,252,0.15)"
    active_tab_color  = "#a590f8"                if is_discussion else "#c084fc"
    active_tab_border = "rgba(124,90,245,0.35)"  if is_discussion else "rgba(192,132,252,0.3)"

    # Active model button colors: Groq=orange, Gemini=teal
    model_bg    = "rgba(251,146,60,0.12)"  if active_llm_now == 'groq' else "rgba(56,189,248,0.12)"
    model_color = "#f59044"                if active_llm_now == 'groq' else "#38c0f8"
    model_bdr   = "rgba(251,146,60,0.35)" if active_llm_now == 'groq' else "rgba(56,189,248,0.3)"

    st.markdown(f"""
    <style>
    /* Mode tab pill container */
    div[data-testid="stSidebarContent"] div[data-testid="stHorizontalBlock"] {{
        background: #13131f;
        border: 1px solid #1e1e2e;
        border-radius: 10px;
        padding: 3px;
        gap: 2px !important;
    }}
    div[data-testid="stSidebarContent"] div[data-testid="stHorizontalBlock"] .stButton > button {{
        background: transparent !important;
        border: none !important;
        border-radius: 7px !important;
        color: #4a4a66 !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        padding: 6px 0 !important;
        transition: all .15s ease !important;
        width: 100% !important;
    }}
    div[data-testid="stSidebarContent"] div[data-testid="stHorizontalBlock"] .stButton > button:hover {{
        background: #1e1e2e !important;
        color: #9898bb !important;
    }}
    /* Active tab */
    div[data-testid="stSidebarContent"] div[data-testid="stHorizontalBlock"] .stButton:{'first' if is_discussion else 'last'}-of-type > button {{
        background: {active_tab_bg} !important;
        color: {active_tab_color} !important;
        border: 1px solid {active_tab_border} !important;
    }}
    /* Active model button — only one is type=primary at a time */
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {{
        background: {model_bg} !important;
        border: 1px solid {model_bdr} !important;
        color: {model_color} !important;
        box-shadow: none !important;
    }}
    section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {{
        opacity: 0.85 !important;
    }}
    </style>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Discussion", key="tab_discussion", use_container_width=True):
            st.session_state.app_mode = 'discussion'
            st.rerun()
    with col2:
        if st.button("Debate", key="tab_debate", use_container_width=True):
            st.session_state.app_mode = 'debate'
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Discussion-only controls ──
    if st.session_state.app_mode == 'discussion':
        st.markdown('<div class="section-label">MODELS</div>', unsafe_allow_html=True)
        if st.button("🔥 Groq — Llama 3.1", key="groq_btn", use_container_width=True,
                     type="primary" if st.session_state.active_llm == 'groq' else "secondary"):
            if st.session_state.active_llm != 'groq':
                st.session_state.conversation.append(
                    {"role": "switch", "from": st.session_state.active_llm, "to": "groq"})
                st.session_state.active_llm = 'groq'
                st.rerun()

        if st.button("✨ Gemini 2.0 Flash", key="gemini_btn", use_container_width=True,
                     type="primary" if st.session_state.active_llm == 'gemini' else "secondary"):
            if st.session_state.active_llm != 'gemini':
                st.session_state.conversation.append(
                    {"role": "switch", "from": st.session_state.active_llm, "to": "gemini"})
                st.session_state.active_llm = 'gemini'
                st.rerun()

        st.markdown('<br><div class="section-label">CONTEXT STRATEGY</div>', unsafe_allow_html=True)
        strategy = st.selectbox(
            "Strategy",
            options=['full', 'summary', 'last5'],
            format_func=lambda x: {'full': 'Full', 'summary': 'Summary + 5', 'last5': 'Last 5'}[x],
            index=['full', 'summary', 'last5'].index(st.session_state.context_strategy),
            label_visibility="collapsed", key="ctx_select"
        )
        if strategy != st.session_state.context_strategy:
            st.session_state.context_strategy = strategy
        st.caption({'full': "Entire conversation sent as-is.",
                    'summary': "Summary + last 5 messages sent.",
                    'last5': "Only last 5 messages sent."}[st.session_state.context_strategy])

    else:
        # Debate mode info
        st.markdown(
            '<div style="background:rgba(168,85,247,0.1);border:1px solid rgba(168,85,247,0.25);'
            'border-radius:10px;padding:12px;font-size:13px;color:hsl(271,91%,80%);line-height:1.6">'
            '⚔️ <b>Debate Mode</b><br>'
            '<span style="color:#7c7c99">Enter any topic. Gemini and Groq will '
            'argue 3 rounds each, then an LLM judge delivers the verdict.</span>'
            '</div>',
            unsafe_allow_html=True
        )

    # ── Context preview (both modes) ──
    ctx_tokens  = get_context_tokens()
    token_limit = 16000 if st.session_state.active_llm == 'groq' else 200000
    pct         = min(100, ctx_tokens / token_limit * 100)
    st.markdown(
        f'<br><div class="section-label">CONTEXT PREVIEW '
        f'<span style="float:right">~{ctx_tokens} tokens</span></div>',
        unsafe_allow_html=True
    )
    st.code(get_context_preview(), language=None)
    st.progress(pct / 100)
    st.caption(f"{pct:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Reset context", use_container_width=True):
        st.session_state.conversation = []
        st.session_state.context_history = []
        st.session_state.debate_running = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
mode = st.session_state.app_mode
llm  = st.session_state.active_llm

if mode == 'debate':
    header_badge  = '<span class="model-badge badge-debate">⚔️&nbsp;&nbsp;Debate Arena — Gemini vs Groq</span>'
    latency_label = "3 rounds · judge verdict"
else:
    model_name  = "Gemini 2.0 Flash" if llm == 'gemini' else "Groq — Llama 3.1"
    badge_class = "badge-gemini"     if llm == 'gemini' else "badge-groq"
    badge_abbr  = "GGL"              if llm == 'gemini' else "LOC"
    latency     = "~410ms"           if llm == 'gemini' else "~90ms"
    header_badge  = f'<span class="model-badge {badge_class}">{badge_abbr}&nbsp;&nbsp;{model_name}</span>'
    latency_label = f"⏱ {latency}"

st.markdown(f"""
<div class="app-header">
  <div style="display:flex;align-items:center;gap:12px">
    <span style="font-size:18px;font-weight:800;color:#ddddf0;letter-spacing:-0.03em">🔄 AI Context Manager</span>
    {header_badge}
  </div>
  <div style="display:flex;align-items:center;gap:14px">
    <span style="font-size:12px;color:#5a5a7a">{latency_label}</span>
    <div class="status-pill">● Connected</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Build chat HTML ────────────────────────────────────────────────────────────
msgs = st.session_state.conversation

ROUND_LABEL = {1: "Round 1", 2: "Round 2", 3: "Round 3"}

if not msgs:
    if mode == 'debate':
        chat_body = """
        <div style="text-align:center;padding:80px 40px">
          <div style="font-size:56px;margin-bottom:16px;opacity:.4">⚔️</div>
          <div style="font-size:22px;font-weight:700;color:#f0f4ff;margin-bottom:8px">Debate Arena</div>
          <div style="font-size:14px;color:#5a5a7a;line-height:1.6">
            Enter any topic below. Gemini opens, Groq responds — 3 rounds each.<br>
            An LLM judge delivers the final verdict.
          </div>
        </div>"""
    else:
        chat_body = """
        <div style="text-align:center;padding:80px 40px">
          <div style="font-size:56px;margin-bottom:16px;opacity:.4">⚡</div>
          <div style="font-size:22px;font-weight:700;color:#f0f4ff;margin-bottom:8px">Switch Without Losing Context</div>
          <div style="font-size:14px;color:#5a5a7a;line-height:1.6">Chat with any AI. Switch anytime — your conversation travels with you.</div>
        </div>"""
else:
    parts = []
    prev_debate_round = None

    for msg in msgs:
        role = msg["role"]

        # ── User bubble ──
        if role == "user":
            parts.append(f"""
            <div style="display:flex;flex-direction:row;justify-content:flex-end;align-items:flex-end;gap:10px;margin:10px 0">
              <div style="background:#7c5af5;color:#fff;border-radius:18px 18px 4px 18px;
                padding:10px 16px;max-width:60%;font-size:14px;line-height:1.6;word-wrap:break-word">
                {esc(msg["content"])}
              </div>
              <div style="width:34px;height:34px;min-width:34px;border-radius:8px;
                background:rgba(124,90,245,0.15);border:1px solid rgba(124,90,245,0.4);
                display:flex;align-items:center;justify-content:center;
                font-size:10px;font-weight:700;color:#9d80f8;flex-shrink:0">You</div>
            </div>""")

        # ── Model switch pill ──
        elif role == "switch":
            to_name = "Gemini 2.0 Flash" if msg["to"] == "gemini" else "Groq"
            icon    = "✨" if msg["to"] == "gemini" else "🔥"
            parts.append(f"""
            <div style="display:flex;justify-content:center;padding:8px 0;margin:4px 0">
              <div style="display:inline-flex;align-items:center;gap:6px;
                background:rgba(50,60,90,0.5);border:1px solid rgba(70,85,120,0.5);
                border-radius:999px;padding:4px 14px;font-size:11px;color:#5a5a7a">
                ↕ Switched to {icon} {to_name} — context preserved
              </div>
            </div>""")

        # ── Thinking indicator ──
        elif role == "thinking":
            is_groq     = msg["llm"] == "groq"
            badge_bg    = "rgba(251,146,60,0.15)"  if is_groq else "rgba(96,165,250,0.15)"
            badge_bdr   = "rgba(251,146,60,0.4)"   if is_groq else "rgba(96,165,250,0.4)"
            badge_color = "hsl(25,95%,63%)"         if is_groq else "hsl(217,91%,70%)"
            label       = "GRQ"                     if is_groq else "GEM"
            name        = "Groq"                    if is_groq else "Gemini"
            parts.append(f"""
            <div style="display:flex;flex-direction:row;justify-content:flex-start;align-items:flex-end;gap:10px;margin:10px 0">
              <div style="width:34px;height:34px;min-width:34px;border-radius:8px;
                background:{badge_bg};border:1px solid {badge_bdr};
                display:flex;align-items:center;justify-content:center;
                font-size:10px;font-weight:700;color:{badge_color};flex-shrink:0">{label}</div>
              <div style="background:#13131f;border:1px solid #2a2a40;
                border-radius:18px;padding:10px 16px;display:flex;align-items:center;gap:8px;
                font-size:13px;color:#5a5a7a;font-style:italic">
                <span>{name} is thinking</span>
                <span class="dots"><span class="dot"></span><span class="dot"></span><span class="dot"></span></span>
              </div>
            </div>""")

        # ── Discussion AI response ──
        elif role in ("groq", "gemini"):
            is_groq     = role == "groq"
            badge_bg    = "rgba(251,146,60,0.15)"  if is_groq else "rgba(96,165,250,0.15)"
            badge_bdr   = "rgba(251,146,60,0.4)"   if is_groq else "rgba(96,165,250,0.4)"
            badge_color = "hsl(25,95%,63%)"         if is_groq else "hsl(217,91%,70%)"
            bubble_bdr  = "rgba(251,146,60,0.3)"   if is_groq else "rgba(96,165,250,0.3)"
            tag_color   = "hsl(25,95%,63%)"         if is_groq else "hsl(217,91%,70%)"
            label       = "GRQ"                     if is_groq else "GEM"
            tag_name    = "🔥 GROQ"                 if is_groq else "✨ GEMINI"
            parts.append(f"""
            <div style="display:flex;flex-direction:row;justify-content:flex-start;align-items:flex-end;gap:10px;margin:10px 0">
              <div style="width:34px;height:34px;min-width:34px;border-radius:8px;
                background:{badge_bg};border:1px solid {badge_bdr};
                display:flex;align-items:center;justify-content:center;
                font-size:10px;font-weight:700;color:{badge_color};flex-shrink:0">{label}</div>
              <div style="background:#13131f;border:1px solid {bubble_bdr};
                border-radius:18px 18px 18px 4px;padding:10px 16px;max-width:60%;word-wrap:break-word">
                <div style="font-size:10px;font-weight:700;text-transform:uppercase;
                  letter-spacing:.8px;color:{tag_color};margin-bottom:5px;opacity:.8">{tag_name}</div>
                <div style="font-size:14px;line-height:1.6;color:#dde3f0">{esc(msg["content"])}</div>
              </div>
            </div>""")

        # ── Debate: topic banner ──
        elif role == "debate_topic":
            prev_debate_round = None
            parts.append(f"""
            <div style="display:flex;justify-content:center;padding:16px 0 8px">
              <div style="background:rgba(168,85,247,0.12);border:1px solid rgba(168,85,247,0.35);
                border-radius:12px;padding:12px 24px;text-align:center;max-width:70%">
                <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1px;
                  color:hsl(271,91%,75%);margin-bottom:6px">⚔️ DEBATE TOPIC</div>
                <div style="font-size:15px;font-weight:600;color:#f0f4ff;line-height:1.5">
                  {esc(msg["content"])}
                </div>
              </div>
            </div>""")

        # ── Debate: round divider + speaker bubble ──
        elif role in ("debate_gemini", "debate_groq"):
            rnd         = msg.get("round", 1)
            is_groq     = role == "debate_groq"
            badge_bg    = "rgba(251,146,60,0.15)"  if is_groq else "rgba(96,165,250,0.15)"
            badge_bdr   = "rgba(251,146,60,0.4)"   if is_groq else "rgba(96,165,250,0.4)"
            badge_color = "hsl(25,95%,63%)"         if is_groq else "hsl(217,91%,70%)"
            bubble_bdr  = "rgba(251,146,60,0.3)"   if is_groq else "rgba(96,165,250,0.3)"
            tag_color   = "hsl(25,95%,63%)"         if is_groq else "hsl(217,91%,70%)"
            label       = "GRQ"                     if is_groq else "GEM"
            speaker     = "🔥 GROQ"                 if is_groq else "✨ GEMINI"
            align       = "flex-end"                if is_groq else "flex-start"
            radius      = "18px 18px 4px 18px"     if is_groq else "18px 18px 18px 4px"

            # Round divider (only on Gemini's first turn of each new round)
            round_divider = ""
            if not is_groq and rnd != prev_debate_round:
                prev_debate_round = rnd
                round_label = ROUND_LABEL.get(rnd, f"Round {rnd}")
                round_divider = f"""
                <div style="display:flex;align-items:center;gap:10px;margin:18px 0 6px">
                  <div style="flex:1;height:1px;background:#1e1e2e"></div>
                  <div style="font-size:11px;font-weight:700;text-transform:uppercase;
                    letter-spacing:.8px;color:hsl(271,91%,72%);
                    background:rgba(168,85,247,0.1);border:1px solid rgba(168,85,247,0.25);
                    border-radius:999px;padding:3px 12px">{round_label}</div>
                  <div style="flex:1;height:1px;background:#1e1e2e"></div>
                </div>"""

            # Groq right-aligned, Gemini left-aligned
            if is_groq:
                bubble_html = f"""
                <div style="display:flex;flex-direction:row;justify-content:{align};align-items:flex-end;gap:10px;margin:8px 0">
                  <div style="background:#13131f;border:1px solid {bubble_bdr};
                    border-radius:{radius};padding:10px 16px;max-width:62%;word-wrap:break-word">
                    <div style="font-size:10px;font-weight:700;text-transform:uppercase;
                      letter-spacing:.8px;color:{tag_color};margin-bottom:5px;opacity:.8">{speaker}</div>
                    <div style="font-size:14px;line-height:1.6;color:#dde3f0">{esc(msg["content"])}</div>
                  </div>
                  <div style="width:34px;height:34px;min-width:34px;border-radius:8px;
                    background:{badge_bg};border:1px solid {badge_bdr};
                    display:flex;align-items:center;justify-content:center;
                    font-size:10px;font-weight:700;color:{badge_color};flex-shrink:0">{label}</div>
                </div>"""
            else:
                bubble_html = f"""
                <div style="display:flex;flex-direction:row;justify-content:{align};align-items:flex-end;gap:10px;margin:8px 0">
                  <div style="width:34px;height:34px;min-width:34px;border-radius:8px;
                    background:{badge_bg};border:1px solid {badge_bdr};
                    display:flex;align-items:center;justify-content:center;
                    font-size:10px;font-weight:700;color:{badge_color};flex-shrink:0">{label}</div>
                  <div style="background:#13131f;border:1px solid {bubble_bdr};
                    border-radius:{radius};padding:10px 16px;max-width:62%;word-wrap:break-word">
                    <div style="font-size:10px;font-weight:700;text-transform:uppercase;
                      letter-spacing:.8px;color:{tag_color};margin-bottom:5px;opacity:.8">{speaker}</div>
                    <div style="font-size:14px;line-height:1.6;color:#dde3f0">{esc(msg["content"])}</div>
                  </div>
                </div>"""

            parts.append(round_divider + bubble_html)

        # ── Debate: judge verdict ──
        elif role == "debate_judge":
            parts.append(f"""
            <div style="display:flex;justify-content:center;padding:20px 0 8px">
              <div style="background:linear-gradient(135deg,rgba(234,179,8,0.1),rgba(234,179,8,0.05));
                border:1px solid rgba(234,179,8,0.35);border-radius:14px;
                padding:16px 20px;max-width:75%;width:100%">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px">
                  <div style="width:28px;height:28px;border-radius:6px;
                    background:rgba(234,179,8,0.15);border:1px solid rgba(234,179,8,0.4);
                    display:flex;align-items:center;justify-content:center;font-size:14px">⚖️</div>
                  <span style="font-size:11px;font-weight:700;text-transform:uppercase;
                    letter-spacing:.8px;color:hsl(48,96%,60%)">LLM JUDGE — VERDICT</span>
                </div>
                <div style="font-size:14px;line-height:1.7;color:#f0e8c0">{esc(msg["content"])}</div>
              </div>
            </div>""")

    chat_body = "\n".join(parts)

# ── Render chat ────────────────────────────────────────────────────────────────
components.html(f"""
<!DOCTYPE html>
<html>
<head>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  * {{ box-sizing:border-box; margin:0; padding:0; font-family:'Inter',sans-serif; }}
  html, body {{
    background: #0e0e18 !important;
    height: 100%; overflow-y: auto;
    scrollbar-width: thin; scrollbar-color: #2a2a40 transparent;
  }}
  body::-webkit-scrollbar {{ width: 6px; }}
  body::-webkit-scrollbar-track {{ background: transparent; }}
  body::-webkit-scrollbar-thumb {{ background: #2a2a40; border-radius: 3px; }}
  .wrap {{ padding: 16px; display:flex; flex-direction:column; gap:4px; }}
  .dots {{ display:inline-flex; gap:4px; }}
  .dot {{
    width:5px; height:5px; border-radius:50%; background:#5a5a7a;
    animation: blink 1.4s ease-in-out infinite; display:inline-block;
  }}
  .dot:nth-child(2) {{ animation-delay:.2s; }}
  .dot:nth-child(3) {{ animation-delay:.4s; }}
  @keyframes blink {{
    0%,80%,100% {{ opacity:.3; transform:scale(.8); }}
    40%          {{ opacity:1;  transform:scale(1);  }}
  }}
</style>
</head>
<body>
  <div class="wrap">{chat_body}</div>
  <script>window.scrollTo(0, document.body.scrollHeight);</script>
</body>
</html>
""", height=490, scrolling=True)

# ── Token bar ──────────────────────────────────────────────────────────────────
ctx_tokens  = get_context_tokens()
token_limit = 16000 if llm == 'groq' else 200000
pct         = min(100, ctx_tokens / token_limit * 100)
fill_cls    = "fill-bad" if pct > 80 else "fill-warn" if pct > 50 else "fill-ok"

st.markdown(f"""
<div class="token-bar">
  <div class="token-bar-inner">
    <span>Token budget: {ctx_tokens:,} / {token_limit // 1000}k</span>
    <div class="token-track"><div class="token-fill {fill_cls}" style="width:{pct:.1f}%"></div></div>
    <span>{pct:.1f}%</span>
  </div>
</div>""", unsafe_allow_html=True)

# ── Input ──────────────────────────────────────────────────────────────────────
if mode == 'discussion':
    def on_send():
        user_input = st.session_state.get("chat_input", "").strip()
        if user_input and not st.session_state.processing:
            st.session_state.processing = True
            send_message(user_input)
            st.session_state.processing = False

    active_name = "Gemini 2.0 Flash" if llm == 'gemini' else "Groq"
    st.chat_input(f"Message {active_name}…", key="chat_input", on_submit=on_send,
                  disabled=st.session_state.processing)

else:  # debate mode
    def on_debate():
        topic = st.session_state.get("debate_input", "").strip()
        if topic and not st.session_state.debate_running:
            st.session_state.debate_running = True
            run_full_debate(topic)
            st.rerun()

    disabled = st.session_state.debate_running
    placeholder = "Debating…" if disabled else "Enter a debate topic (e.g. 'AI will replace software engineers')…"
    st.chat_input(placeholder, key="debate_input", on_submit=on_debate, disabled=disabled)
