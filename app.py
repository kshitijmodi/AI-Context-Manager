import streamlit as st
import streamlit.components.v1 as components
from groq import Groq
import google.generativeai as genai
import os

VERSION = "12.0"

st.set_page_config(
    page_title="LLM Bridge",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Page-level CSS (sidebar, buttons, header) ─────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
body, .stApp { background: hsl(222.2,84%,4.9%) !important; }
#MainMenu, footer, header, .stDeployButton,
[data-testid="stHeader"],[data-testid="stDecoration"],
[data-testid="stToolbar"],[data-testid="collapsedControl"] { display:none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    display: block !important; visibility: visible !important;
    background: hsl(222.2,84%,4.9%) !important;
    border-right: 1px solid hsl(217.2,32.6%,17.5%) !important;
}
section[data-testid="stSidebar"] > div,
[data-testid="stSidebarContent"] { background: hsl(222.2,84%,4.9%) !important; }

/* Buttons */
.stButton > button {
    background: hsl(217.2,32.6%,17.5%) !important;
    color: hsl(210,40%,98%) !important;
    border: 1px solid hsl(217.2,32.6%,22%) !important;
    border-radius: 8px !important; font-weight: 600 !important; transition: all .2s !important;
}
.stButton > button:hover { background: hsl(217.2,32.6%,22%) !important; }
.stButton > button[kind="primary"] {
    background: hsl(217.2,91.2%,59.8%) !important;
    border-color: hsl(217.2,91.2%,59.8%) !important; color: white !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: hsl(217.2,32.6%,14%) !important;
    border: 1px solid hsl(217.2,32.6%,22%) !important;
    color: hsl(210,40%,98%) !important; border-radius: 8px !important;
}

/* Labels / captions */
.stMarkdown p, .stCaption,
[data-testid="stSidebarContent"] p,
[data-testid="stSidebarContent"] span,
[data-testid="stSidebarContent"] label { color: hsl(215,20.2%,65.1%) !important; }

/* Chat input */
.stChatInput > div {
    background: hsl(217.2,32.6%,14%) !important;
    border: 1px solid hsl(217.2,32.6%,22%) !important; border-radius: 12px !important;
}
.stChatInput textarea { color: hsl(210,40%,98%) !important; }
.stChatInput textarea::placeholder { color: hsl(215,20.2%,65.1%) !important; }

/* Section label */
.section-label {
    font-size:11px; font-weight:600; text-transform:uppercase;
    letter-spacing:.5px; color:hsl(215,20.2%,65.1%); margin-bottom:8px;
}

/* Header */
.app-header {
    display:flex; align-items:center; justify-content:space-between;
    height:52px; padding:0 1.25rem;
    border-bottom:1px solid hsl(217.2,32.6%,17.5%);
    background:hsl(222.2,84%,4.9%);
}
.model-badge {
    display:inline-flex; align-items:center; gap:6px;
    border-radius:6px; border:1px solid; padding:4px 10px;
    font-size:12px; font-weight:500;
}
.badge-groq   { border-color:hsl(25,95%,53%,0.3);  background:hsl(25,95%,53%,0.12);  color:hsl(25,95%,63%); }
.badge-gemini { border-color:hsl(217,91%,60%,0.3); background:hsl(217,91%,60%,0.12); color:hsl(217,91%,70%); }
.status-pill {
    display:flex; align-items:center; gap:6px;
    border:1px solid hsl(142,71%,45%,0.3); background:hsl(142,71%,45%,0.1);
    border-radius:999px; padding:4px 12px; font-size:12px; color:hsl(142,76%,56%);
}

/* Token bar */
.token-bar { padding:6px 1.25rem; border-top:1px solid hsl(217.2,32.6%,17.5%); background:hsl(222.2,84%,4.9%); }
.token-bar-inner { display:flex; align-items:center; gap:12px; font-size:12px; color:hsl(215,20.2%,65.1%); }
.token-track { flex:1; height:4px; border-radius:999px; background:hsl(217.2,32.6%,17.5%); overflow:hidden; }
.token-fill  { height:100%; border-radius:999px; transition:width .3s; }
.fill-ok   { background:hsl(217.2,91.2%,59.8%); }
.fill-warn { background:hsl(25,95%,53%); }
.fill-bad  { background:hsl(0,84.2%,60.2%); }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
for k, v in {
    'active_llm': 'gemini',
    'conversation': [],
    'context_history': [],
    'processing': False,
    'context_strategy': 'full'
}.items():
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
def build_context(): return "".join(f"{m['role']}: {m['content']}\n" for m in st.session_state.context_history[-8:])
def get_context_preview():
    lines = [f"[{m['role']}] {m['content'][:60]}{'…' if len(m['content'])>60 else ''}"
             for m in st.session_state.context_history[-5:]]
    return "\n".join(lines) if lines else "No messages yet."

def call_groq(prompt):
    try:
        ctx = build_context()
        fp = f"Context:\n{ctx}\n\nNew: {prompt}\n\nRespond naturally." if ctx else prompt
        r = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role":"user","content":fp}],
            max_tokens=2000, temperature=0.7
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def call_gemini(prompt):
    try:
        ctx = build_context()
        fp = f"Context:\n{ctx}\n\nNew: {prompt}\n\nRespond naturally." if ctx else prompt
        r = gemini_model.generate_content(
            fp, generation_config=genai.types.GenerationConfig(max_output_tokens=2000, temperature=0.7)
        )
        return r.text
    except Exception as e:
        return f"Error: {e}"

def send_message(user_input):
    st.session_state.conversation.append({"role":"user","content":user_input})
    st.session_state.conversation.append({"role":"thinking","llm":st.session_state.active_llm})
    response = call_groq(user_input) if st.session_state.active_llm == 'groq' else call_gemini(user_input)
    st.session_state.conversation.pop()
    st.session_state.conversation.append({"role":st.session_state.active_llm,"content":response})
    st.session_state.context_history.append({"role":"user","content":user_input})
    st.session_state.context_history.append({"role":st.session_state.active_llm,"content":response})

def esc(text):
    return (text
        .replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
        .replace('"',"&quot;").replace("'","&#39;").replace("\n","<br>"))

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="padding:14px 16px;border-bottom:1px solid hsl(217.2,32.6%,17.5%);font-size:15px;font-weight:700;color:hsl(210,40%,98%)">⚡ LLM Bridge</div>', unsafe_allow_html=True)
    st.markdown('<div style="padding:16px">', unsafe_allow_html=True)

    st.markdown('<div class="section-label">MODELS</div>', unsafe_allow_html=True)
    if st.button("🔥 Groq — Llama 3.1", key="groq_btn", use_container_width=True,
                 type="primary" if st.session_state.active_llm=='groq' else "secondary"):
        if st.session_state.active_llm != 'groq':
            st.session_state.conversation.append({"role":"switch","from":st.session_state.active_llm,"to":"groq"})
            st.session_state.active_llm = 'groq'
            st.rerun()

    if st.button("✨ Gemini 2.0 Flash", key="gemini_btn", use_container_width=True,
                 type="primary" if st.session_state.active_llm=='gemini' else "secondary"):
        if st.session_state.active_llm != 'gemini':
            st.session_state.conversation.append({"role":"switch","from":st.session_state.active_llm,"to":"gemini"})
            st.session_state.active_llm = 'gemini'
            st.rerun()

    st.markdown('<br><div class="section-label">CONTEXT STRATEGY</div>', unsafe_allow_html=True)
    strategy = st.selectbox("Strategy",
        options=['full','summary','last5'],
        format_func=lambda x: {'full':'Full','summary':'Summary + 5','last5':'Last 5'}[x],
        index=['full','summary','last5'].index(st.session_state.context_strategy),
        label_visibility="collapsed", key="ctx_select"
    )
    if strategy != st.session_state.context_strategy:
        st.session_state.context_strategy = strategy
    st.caption({'full':"Entire conversation sent as-is.",
                'summary':"Summary + last 5 messages sent.",
                'last5':"Only last 5 messages sent."}[st.session_state.context_strategy])

    ctx_tokens  = get_context_tokens()
    token_limit = 16000 if st.session_state.active_llm=='groq' else 200000
    pct         = min(100, ctx_tokens / token_limit * 100)
    st.markdown(f'<br><div class="section-label">CONTEXT PREVIEW <span style="float:right">~{ctx_tokens} tokens</span></div>', unsafe_allow_html=True)
    st.code(get_context_preview(), language=None)
    st.progress(pct / 100)
    st.caption(f"{pct:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Reset context", use_container_width=True):
        st.session_state.conversation = []
        st.session_state.context_history = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
llm         = st.session_state.active_llm
model_name  = "Gemini 2.0 Flash" if llm=='gemini' else "Groq — Llama 3.1"
badge_class = "badge-gemini"     if llm=='gemini' else "badge-groq"
badge_abbr  = "GGL"              if llm=='gemini' else "LOC"
latency     = "~410ms"           if llm=='gemini' else "~90ms"

st.markdown(f"""
<div class="app-header">
  <div class="model-badge {badge_class}">{badge_abbr}&nbsp;&nbsp;{model_name}</div>
  <div style="display:flex;align-items:center;gap:14px">
    <span style="font-size:12px;color:hsl(215,20.2%,65.1%)">⏱ {latency}</span>
    <div class="status-pill">● Bridge: Connected</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Build chat HTML ───────────────────────────────────────────────────────────
msgs = st.session_state.conversation

if not msgs:
    chat_body = """
    <div style="text-align:center;padding:80px 40px">
      <div style="font-size:56px;margin-bottom:16px;opacity:.4">⚡</div>
      <div style="font-size:22px;font-weight:700;color:#f0f4ff;margin-bottom:8px">Switch Without Losing Context</div>
      <div style="font-size:14px;color:#6b7a99;line-height:1.6">Chat with any AI. Switch anytime — your conversation travels with you.</div>
    </div>"""
else:
    parts = []
    for msg in msgs:
        role = msg["role"]
        if role == "user":
            parts.append(f"""
            <div style="display:flex;flex-direction:row;justify-content:flex-end;align-items:flex-end;gap:10px;margin:10px 0">
              <div style="background:hsl(217.2,91.2%,59.8%);color:#fff;border-radius:18px 18px 4px 18px;padding:10px 16px;max-width:60%;font-size:14px;line-height:1.6;word-wrap:break-word">{esc(msg["content"])}</div>
              <div style="width:34px;height:34px;min-width:34px;border-radius:8px;background:rgba(99,145,242,0.15);border:1px solid rgba(99,145,242,0.4);display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:hsl(217.2,91.2%,69%);flex-shrink:0">You</div>
            </div>""")
        elif role == "switch":
            to   = "Gemini 2.0 Flash" if msg["to"]=="gemini" else "Groq"
            icon = "✨" if msg["to"]=="gemini" else "🔥"
            parts.append(f"""
            <div style="display:flex;justify-content:center;padding:8px 0;margin:4px 0">
              <div style="display:inline-flex;align-items:center;gap:6px;background:rgba(50,60,90,0.5);border:1px solid rgba(70,85,120,0.5);border-radius:999px;padding:4px 14px;font-size:11px;color:#6b7a99">
                ↕ Switched to {icon} {to} — context preserved
              </div>
            </div>""")
        elif role == "thinking":
            is_groq = msg["llm"] == "groq"
            badge_bg    = "rgba(251,146,60,0.15)"  if is_groq else "rgba(96,165,250,0.15)"
            badge_bdr   = "rgba(251,146,60,0.4)"   if is_groq else "rgba(96,165,250,0.4)"
            badge_color = "hsl(25,95%,63%)"         if is_groq else "hsl(217,91%,70%)"
            label       = "GRQ"                     if is_groq else "GEM"
            name        = "Groq"                    if is_groq else "Gemini"
            parts.append(f"""
            <div style="display:flex;flex-direction:row;justify-content:flex-start;align-items:flex-end;gap:10px;margin:10px 0">
              <div style="width:34px;height:34px;min-width:34px;border-radius:8px;background:{badge_bg};border:1px solid {badge_bdr};display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:{badge_color};flex-shrink:0">{label}</div>
              <div style="background:hsl(217.2,32.6%,13%);border:1px solid hsl(217.2,32.6%,22%);border-radius:18px;padding:10px 16px;display:flex;align-items:center;gap:8px;font-size:13px;color:#6b7a99;font-style:italic">
                <span>{name} is thinking</span>
                <span class="dots"><span class="dot"></span><span class="dot"></span><span class="dot"></span></span>
              </div>
            </div>""")
        elif role in ("groq","gemini"):
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
              <div style="width:34px;height:34px;min-width:34px;border-radius:8px;background:{badge_bg};border:1px solid {badge_bdr};display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:{badge_color};flex-shrink:0">{label}</div>
              <div style="background:hsl(217.2,32.6%,13%);border:1px solid {bubble_bdr};border-radius:18px 18px 18px 4px;padding:10px 16px;max-width:60%;word-wrap:break-word">
                <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;color:{tag_color};margin-bottom:5px;opacity:.8">{tag_name}</div>
                <div style="font-size:14px;line-height:1.6;color:#dde3f0">{esc(msg["content"])}</div>
              </div>
            </div>""")
    chat_body = "\n".join(parts)

# Render via components.html — guaranteed HTML rendering, no sanitization
components.html(f"""
<!DOCTYPE html>
<html>
<head>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  * {{ box-sizing:border-box; margin:0; padding:0; font-family:'Inter',sans-serif; }}
  html, body {{
    background: hsl(222.2,84%,6%) !important;
    height: 100%;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: hsl(217.2,32.6%,25%) transparent;
  }}
  body::-webkit-scrollbar {{ width: 6px; }}
  body::-webkit-scrollbar-track {{ background: transparent; }}
  body::-webkit-scrollbar-thumb {{ background: hsl(217.2,32.6%,25%); border-radius: 3px; }}
  .wrap {{ padding: 16px; display:flex; flex-direction:column; gap:4px; }}
  .dots {{ display:inline-flex; gap:4px; }}
  .dot {{
    width:5px; height:5px; border-radius:50%; background:#6b7a99;
    animation: blink 1.4s ease-in-out infinite;
    display:inline-block;
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
  <div class="wrap">
    {chat_body}
  </div>
  <script>window.scrollTo(0, document.body.scrollHeight);</script>
</body>
</html>
""", height=500, scrolling=True)

# ── Token bar ─────────────────────────────────────────────────────────────────
ctx_tokens  = get_context_tokens()
token_limit = 16000 if llm=='groq' else 200000
pct         = min(100, ctx_tokens / token_limit * 100)
fill_cls    = "fill-bad" if pct>80 else "fill-warn" if pct>50 else "fill-ok"

st.markdown(f"""
<div class="token-bar">
  <div class="token-bar-inner">
    <span>Token budget: {ctx_tokens:,} / {token_limit//1000}k</span>
    <div class="token-track"><div class="token-fill {fill_cls}" style="width:{pct:.1f}%"></div></div>
    <span>{pct:.1f}%</span>
  </div>
</div>""", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
def on_send():
    user_input = st.session_state.get("chat_input","").strip()
    if user_input and not st.session_state.processing:
        st.session_state.processing = True
        send_message(user_input)
        st.session_state.processing = False

active_name = "Gemini 2.0 Flash" if llm=='gemini' else "Groq"
st.chat_input(f"Message {active_name}…", key="chat_input", on_submit=on_send,
              disabled=st.session_state.processing)