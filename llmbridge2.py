import streamlit as st
from groq import Groq
import google.generativeai as genai
import os

VERSION = "6.5"

st.set_page_config(page_title="AI Context Manager", page_icon="🔄", layout="wide", initial_sidebar_state="collapsed")

# Clean, modern design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    * {
        font-family: 'Inter', sans-serif;
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
        background: linear-gradient(135deg, #0B0D1E 0%, #1a1a2e 100%);
    }

    section[data-testid="stSidebar"] {
        display: none !important;
    }

    .block-container {
        padding: 1rem 2rem !important;
        max-width: 100% !important;
    }

    /* ============ CHAT BUBBLES ============ */

    /* User message - right aligned gradient bubble */
    .user-bubble {
        display: flex;
        justify-content: flex-end;
        margin: 16px 0;
        animation: slideInRight 0.3s ease-out;
    }

    .user-bubble-content {
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
        border-radius: 18px 18px 4px 18px;
        padding: 12px 18px;
        max-width: 65%;
        color: white;
        font-size: 14px;
        line-height: 1.6;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        word-wrap: break-word;
    }

    /* AI message - left aligned with avatar */
    .ai-bubble {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        margin: 16px 0;
        animation: slideInLeft 0.3s ease-out;
    }

    .ai-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        flex-shrink: 0;
        margin-top: 4px;
    }

    .groq-avatar {
        background: rgba(251, 146, 60, 0.15);
        border: 1px solid rgba(251, 146, 60, 0.3);
    }

    .gemini-avatar {
        background: rgba(96, 165, 250, 0.15);
        border: 1px solid rgba(96, 165, 250, 0.3);
    }

    .ai-bubble-content {
        background: rgba(20, 25, 45, 0.8);
        border: 1px solid;
        border-radius: 18px 18px 18px 4px;
        padding: 14px 18px;
        max-width: 65%;
        font-size: 14px;
        line-height: 1.7;
        word-wrap: break-word;
    }

    .groq-bubble {
        border-color: rgba(251, 146, 60, 0.4);
    }

    .gemini-bubble {
        border-color: rgba(96, 165, 250, 0.4);
    }

    .ai-label {
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
        opacity: 0.8;
    }

    .groq-label {
        color: #FBA66F;
    }

    .gemini-label {
        color: #93C5FD;
    }

    .ai-text {
        color: #E5E7EB;
    }

    /* Thinking bubble */
    .thinking-bubble {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        margin: 16px 0;
    }

    .thinking-bubble-content {
        background: rgba(20, 25, 45, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 18px;
        padding: 10px 16px;
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 13px;
        color: #9ca3af;
        font-style: italic;
    }

    .thinking-dots {
        display: flex;
        gap: 4px;
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
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    /* Switch indicator */
    .switch-indicator {
        background: rgba(102, 126, 234, 0.15);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        padding: 10px 16px;
        margin: 16px auto;
        max-width: 400px;
        text-align: center;
        color: #C4B5FD;
        font-size: 12px;
        font-weight: 600;
    }

    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 60px 40px;
        color: white;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .empty-title {
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 12px;
    }

    .empty-subtitle {
        font-size: 14px;
        color: rgba(255, 255, 255, 0.6);
        line-height: 1.6;
    }

    /* ============ BUTTONS ============ */
    .stButton > button {
        background: rgba(20, 25, 45, 0.8) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        transition: all 0.2s !important;
    }

    .stButton > button:hover {
        background: rgba(102, 126, 234, 0.3) !important;
        border-color: rgba(102, 126, 234, 0.5) !important;
        transform: translateY(-1px) !important;
    }

    /* Primary button (active LLM) */
    .stButton > button[kind="primary"],
    .stButton > button[data-baseweb="button"][kind="primary"] {
        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%) !important;
        border: 2px solid rgba(102, 126, 234, 0.8) !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
        color: white !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #764BA2 0%, #667EEA 100%) !important;
        border-color: rgba(102, 126, 234, 1) !important;
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.5) !important;
    }

    /* Brand styling */
    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .brand-icon {
        font-size: 28px;
    }

    .brand-title {
        font-size: 20px;
        font-weight: 800;
        color: white;
        letter-spacing: -0.5px;
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

    # Input area at the bottom of the chat window
    st.markdown('<div style="border-top: 1px solid rgba(255, 255, 255, 0.1); padding-top: 12px; margin-top: 12px;"></div>', unsafe_allow_html=True)

    def on_send():
        user_input = st.session_state.input
        if user_input and not st.session_state.processing:
            st.session_state.processing = True
            send_message(user_input)
            st.session_state.processing = False

    active_llm = "🔥 Groq" if st.session_state.active_llm == 'groq' else "✨ Gemini"
    st.chat_input(f"Message {active_llm}...", key="input", on_submit=on_send, disabled=st.session_state.processing)