import streamlit as st
from groq import Groq
import google.generativeai as genai
import os

VERSION = "6.5"

st.set_page_config(page_title="AI Context Manager", page_icon="🔄", layout="wide", initial_sidebar_state="collapsed")

# Elegant, refined design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    /* Force hide all Streamlit elements */
    #MainMenu {display: none !important; visibility: hidden !important;}
    footer {display: none !important; visibility: hidden !important;}
    header {display: none !important; visibility: hidden !important;}
    .stDeployButton {display: none !important; visibility: hidden !important;}
    [data-testid="stHeader"] {display: none !important; visibility: hidden !important;}
    [data-testid="stDecoration"] {display: none !important; visibility: hidden !important;}
    [data-testid="stToolbar"] {display: none !important; visibility: hidden !important;}

    .stApp {
        background: linear-gradient(160deg, #0f0f14 0%, #16161d 45%, #1a1b26 100%);
        min-height: 100vh;
    }

    section[data-testid="stSidebar"] {
        display: none !important;
    }

    .block-container {
        padding: 1.25rem 2rem !important;
        max-width: 100% !important;
    }

    /* ============ CHAT BUBBLES ============ */

    .user-bubble {
        display: flex;
        justify-content: flex-end;
        margin: 18px 0;
        animation: slideInRight 0.35s cubic-bezier(0.22, 1, 0.36, 1);
    }

    .user-bubble-content {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 50%, #7c3aed 100%);
        border-radius: 20px 20px 6px 20px;
        padding: 14px 20px;
        max-width: 65%;
        color: rgba(255, 255, 255, 0.98);
        font-size: 15px;
        font-weight: 450;
        line-height: 1.65;
        box-shadow: 0 8px 24px rgba(79, 70, 229, 0.25), 0 2px 6px rgba(0, 0, 0, 0.15);
        word-wrap: break-word;
        letter-spacing: 0.01em;
    }

    .ai-bubble {
        display: flex;
        align-items: flex-start;
        gap: 14px;
        margin: 18px 0;
        animation: slideInLeft 0.35s cubic-bezier(0.22, 1, 0.36, 1);
    }

    .ai-avatar {
        width: 40px;
        height: 40px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        flex-shrink: 0;
        margin-top: 4px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }

    .groq-avatar {
        background: linear-gradient(145deg, rgba(251, 146, 60, 0.2) 0%, rgba(234, 88, 12, 0.15) 100%);
        border: 1px solid rgba(251, 146, 60, 0.35);
    }

    .gemini-avatar {
        background: linear-gradient(145deg, rgba(59, 130, 246, 0.2) 0%, rgba(37, 99, 235, 0.15) 100%);
        border: 1px solid rgba(96, 165, 250, 0.35);
    }

    .ai-bubble-content {
        background: rgba(26, 28, 42, 0.92);
        border: 1px solid;
        border-radius: 20px 20px 20px 6px;
        padding: 16px 20px;
        max-width: 65%;
        font-size: 15px;
        font-weight: 450;
        line-height: 1.7;
        word-wrap: break-word;
        letter-spacing: 0.01em;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }

    .groq-bubble {
        border-color: rgba(251, 146, 60, 0.35);
    }

    .gemini-bubble {
        border-color: rgba(96, 165, 250, 0.35);
    }

    .ai-label {
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 8px;
        opacity: 0.92;
    }

    .groq-label {
        color: #fbbf77;
    }

    .gemini-label {
        color: #93c5fd;
    }

    .ai-text {
        color: #e8eaed;
    }

    .thinking-bubble {
        display: flex;
        align-items: flex-start;
        gap: 14px;
        margin: 18px 0;
    }

    .thinking-bubble-content {
        background: rgba(26, 28, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 12px 18px;
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 13px;
        font-weight: 500;
        color: #9ca3af;
        font-style: italic;
    }

    .thinking-dots {
        display: flex;
        gap: 5px;
    }

    .thinking-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: currentColor;
        animation: bounce 1.4s ease-in-out infinite;
    }

    .thinking-dot:nth-child(1) { animation-delay: 0s; }
    .thinking-dot:nth-child(2) { animation-delay: 0.2s; }
    .thinking-dot:nth-child(3) { animation-delay: 0.4s; }

    @keyframes bounce {
        0%, 80%, 100% { transform: translateY(0); opacity: 0.6; }
        40% { transform: translateY(-6px); opacity: 1; }
    }

    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(16px); }
        to { opacity: 1; transform: translateX(0); }
    }

    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-16px); }
        to { opacity: 1; transform: translateX(0); }
    }

    .switch-indicator {
        background: rgba(79, 70, 229, 0.12);
        border: 1px solid rgba(99, 102, 241, 0.28);
        border-radius: 14px;
        padding: 12px 20px;
        margin: 18px auto;
        max-width: 400px;
        text-align: center;
        color: #a5b4fc;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.02em;
    }

    .empty-state {
        text-align: center;
        padding: 64px 40px;
        color: white;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .empty-title {
        font-size: 26px;
        font-weight: 800;
        margin-bottom: 14px;
        color: rgba(255, 255, 255, 0.95);
        letter-spacing: -0.02em;
    }

    .empty-subtitle {
        font-size: 15px;
        font-weight: 450;
        color: rgba(255, 255, 255, 0.55);
        line-height: 1.65;
        max-width: 380px;
    }

    /* ============ BUTTONS ============ */
    .stButton > button {
        background: rgba(26, 28, 42, 0.9) !important;
        color: rgba(255, 255, 255, 0.9) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 14px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 11px 22px !important;
        transition: all 0.22s ease !important;
        letter-spacing: 0.01em !important;
    }

    .stButton > button:hover {
        background: rgba(79, 70, 229, 0.2) !important;
        border-color: rgba(99, 102, 241, 0.4) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.15) !important;
    }

    .stButton > button[kind="primary"],
    .stButton > button[data-baseweb="button"][kind="primary"] {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 50%, #7c3aed 100%) !important;
        border: 1px solid rgba(99, 102, 241, 0.5) !important;
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.3) !important;
        color: white !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #5b21b6 0%, #4f46e5 100%) !important;
        border-color: rgba(99, 102, 241, 0.7) !important;
        box-shadow: 0 8px 24px rgba(79, 70, 229, 0.35) !important;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .brand-icon {
        font-size: 30px;
        filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
    }

    .brand-title {
        font-size: 22px;
        font-weight: 800;
        color: rgba(255, 255, 255, 0.96);
        letter-spacing: -0.03em;
    }

    /* Chat container border */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        background: rgba(22, 22, 29, 0.6) !important;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.15) !important;
    }

    /* Input divider */
    .stChatInput > div {
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background: rgba(26, 28, 42, 0.6) !important;
    }
    .stChatInput > div:focus-within {
        border-color: rgba(99, 102, 241, 0.4) !important;
        box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.15) !important;
    }
    .stChatInput textarea {
        color: #e8eaed !important;
        font-size: 15px !important;
    }
    .stChatInput textarea::placeholder {
        color: rgba(255, 255, 255, 0.4) !important;
    }

    /* ============ TOKEN BAR ============ */
    .token-bar {
        padding: 6px 4px;
    }
    .token-bar-inner {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 11px;
        color: rgba(255, 255, 255, 0.38);
    }
    .token-track {
        flex: 1;
        height: 3px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.08);
        overflow: hidden;
    }
    .token-fill {
        height: 100%;
        border-radius: 999px;
        transition: width .3s;
    }
    .fill-ok   { background: #4f46e5; }
    .fill-warn { background: #f59e0b; }
    .fill-bad  { background: #ef4444; }

    /* Collapse Streamlit's wrapper so the bar takes only its natural height */
    .element-container:has(.token-bar) {
        margin: 0 !important;
        padding: 0 !important;
        line-height: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'active_llm' not in st.session_state:
    st.session_state.active_llm = 'groq'
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'context_history' not in st.session_state:
    st.session_state.context_history = []
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'message_count' not in st.session_state:
    st.session_state.message_count = {'groq': 0, 'gemini': 0}

# API setup
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

try:
    groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-2.5-flash-lite')
    else:
        gemini_model = None
except:
    groq_client = None
    gemini_model = None

if not GROQ_API_KEY or not GEMINI_API_KEY:
    st.error("⚠️ Add GROQ_API_KEY and GEMINI_API_KEY to Replit Secrets")
    st.stop()

# ==================== HEADER ====================
col1, col2, col3 = st.columns([2.5, 2.5, 1])

with col1:
    st.markdown('''
    <div class="brand">
        <span class="brand-icon">🔄</span>
        <span class="brand-title">AI Context Manager</span>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("🔥 Groq", key="groq", use_container_width=True,
                     disabled=st.session_state.processing,
                     type="primary" if st.session_state.active_llm == 'groq' else "secondary"):
            if st.session_state.active_llm != 'groq':
                st.session_state.conversation.append({
                    "role": "switch", "from": st.session_state.active_llm, "to": "groq"
                })
                st.session_state.active_llm = 'groq'
                st.rerun()

    with btn_col2:
        if st.button("✨ Gemini", key="gemini", use_container_width=True,
                     disabled=st.session_state.processing,
                     type="primary" if st.session_state.active_llm == 'gemini' else "secondary"):
            if st.session_state.active_llm != 'gemini':
                st.session_state.conversation.append({
                    "role": "switch", "from": st.session_state.active_llm, "to": "gemini"
                })
                st.session_state.active_llm = 'gemini'
                st.rerun()

with col3:
    if st.button("🗑️ Clear", key="clear", use_container_width=True, disabled=st.session_state.processing):
        st.session_state.conversation = []
        st.session_state.context_history = []
        st.session_state.message_count = {'groq': 0, 'gemini': 0}
        st.rerun()

# ==================== API ====================
def build_context():
    context = ""
    for msg in st.session_state.context_history[-8:]:
        context += f"{msg['role']}: {msg['content']}\n"
    return context

def call_groq(prompt):
    try:
        context = build_context()
        if context:
            full_prompt = f"Here's the conversation history for context:\n{context}\n\nNow respond to this new question: {prompt}\n\nProvide only your response, without repeating the question or context."
        else:
            full_prompt = prompt

        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": full_prompt}],
            max_tokens=2000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def call_gemini(prompt):
    try:
        context = build_context()
        if context:
            full_prompt = f"Here's the conversation history for context:\n{context}\n\nNow respond to this new question: {prompt}\n\nProvide only your response, without repeating the question or context."
        else:
            full_prompt = prompt

        response = gemini_model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(max_output_tokens=2000, temperature=0.7)
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def send_message(user_input):
    st.session_state.conversation.append({"role": "user", "content": user_input})
    st.session_state.conversation.append({"role": "thinking", "llm": st.session_state.active_llm})

    if st.session_state.active_llm == 'groq':
        response = call_groq(user_input)
        st.session_state.message_count['groq'] += 1
    else:
        response = call_gemini(user_input)
        st.session_state.message_count['gemini'] += 1

    st.session_state.conversation.pop()
    st.session_state.conversation.append({"role": st.session_state.active_llm, "content": response})

    st.session_state.context_history.append({"role": "User", "content": user_input})
    st.session_state.context_history.append({"role": st.session_state.active_llm.capitalize(), "content": response})

def estimate_tokens(text): return max(1, len(text) // 4)
def get_context_tokens(): return sum(estimate_tokens(m['content']) for m in st.session_state.context_history[-8:])

# ==================== CHAT WINDOW ====================
chat_window = st.container(border=True)

with chat_window:
    # Messages area
    messages_area = st.container(height=450)

    with messages_area:
        if len(st.session_state.conversation) == 0:
            st.markdown('''
            <div class="empty-state">
                <div style="font-size: 64px; margin-bottom: 20px;">🔄</div>
                <div class="empty-title">Switch Without Losing Context</div>
                <div class="empty-subtitle">
                    Chat with any AI. Switch anytime—your full conversation travels with you.
                </div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            for idx, msg in enumerate(st.session_state.conversation):
                if msg["role"] == "user":
                    # User bubble - right aligned gradient
                    st.markdown(f'''
                    <div class="user-bubble">
                        <div class="user-bubble-content">
                            {msg["content"]}
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)

                elif msg["role"] == "switch":
                    # Switch indicator
                    from_icon = "🔥" if msg["from"] == "groq" else "✨"
                    to_icon = "🔥" if msg["to"] == "groq" else "✨"
                    from_name = "Groq" if msg["from"] == "groq" else "Gemini"
                    to_name = "Groq" if msg["to"] == "groq" else "Gemini"
                    st.markdown(f'''
                    <div class="switch-indicator">
                        🔄 Switched: {from_icon} {from_name} → {to_icon} {to_name}
                    </div>
                    ''', unsafe_allow_html=True)

                elif msg["role"] == "thinking":
                    # Thinking bubble
                    llm = msg["llm"]
                    avatar_emoji = '🔥' if llm == 'groq' else '✨'
                    avatar_class = 'groq-avatar' if llm == 'groq' else 'gemini-avatar'
                    llm_name = 'Groq' if llm == 'groq' else 'Gemini'

                    st.markdown(f'''
                    <div class="thinking-bubble">
                        <div class="ai-avatar {avatar_class}">{avatar_emoji}</div>
                        <div class="thinking-bubble-content">
                            <span>{llm_name} is thinking</span>
                            <div class="thinking-dots">
                                <div class="thinking-dot"></div>
                                <div class="thinking-dot"></div>
                                <div class="thinking-dot"></div>
                            </div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)

                elif msg["role"] == "groq":
                    # Groq bubble - left aligned with avatar
                    st.markdown(f'''
                    <div class="ai-bubble">
                        <div class="ai-avatar groq-avatar">🔥</div>
                        <div class="ai-bubble-content groq-bubble">
                            <div class="ai-label groq-label">🔥 GROQ</div>
                            <div class="ai-text">{msg["content"]}</div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)

                elif msg["role"] == "gemini":
                    # Gemini bubble - left aligned with avatar
                    st.markdown(f'''
                    <div class="ai-bubble">
                        <div class="ai-avatar gemini-avatar">✨</div>
                        <div class="ai-bubble-content gemini-bubble">
                            <div class="ai-label gemini-label">✨ GEMINI</div>
                            <div class="ai-text">{msg["content"]}</div>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)

    # Token bar + divider
    _ctx_tokens  = get_context_tokens()
    _token_limit = 16000 if st.session_state.active_llm == 'groq' else 200000
    _pct         = min(100, _ctx_tokens / _token_limit * 100)
    _fill_cls    = "fill-bad" if _pct > 80 else "fill-warn" if _pct > 50 else "fill-ok"
    st.markdown(f"""
<div class="token-bar">
  <div class="token-bar-inner">
    <span>Token budget: {_ctx_tokens:,} / {_token_limit // 1000}k</span>
    <div class="token-track"><div class="token-fill {_fill_cls}" style="width:{_pct:.1f}%"></div></div>
    <span>{_pct:.1f}%</span>
  </div>
</div>
<div style="border-top:1px solid rgba(255,255,255,0.1);margin-top:6px;margin-bottom:6px;"></div>
""", unsafe_allow_html=True)

    def on_send():
        user_input = st.session_state.input
        if user_input and not st.session_state.processing:
            st.session_state.processing = True
            send_message(user_input)
            st.session_state.processing = False

    active_llm = "🔥 Groq" if st.session_state.active_llm == 'groq' else "✨ Gemini"
    st.chat_input(f"Message {active_llm}...", key="input", on_submit=on_send, disabled=st.session_state.processing)