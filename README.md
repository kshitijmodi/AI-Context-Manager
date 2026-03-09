# 🌉 AI Context Manager
### AI Context Manager — Seamless Cross-Model Conversations

> Switch between AI models mid-conversation without losing context. No copy-pasting. No re-prompting. Just flow.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-API-F55036?style=flat)
![Gemini](https://img.shields.io/badge/Gemini-API-4285F4?style=flat&logo=google&logoColor=white)
---

## 🧠 What is AI Context Manager?

**AI Context Manager** is an LLM Bridge that solves one of the biggest friction points for AI power users — the need to manually transfer conversation history when switching between language models.

Whether you hit a token limit on one model or simply need a different model's strengths mid-task, LLM Bridge keeps your conversation intact and hands it off seamlessly.

---

## 😤 The Problem

If you've ever:
- Hit a **token limit** mid-conversation and had to start over
- **Copy-pasted** your entire chat history into a new model
- Re-explained your project context for the fifth time this week
- Wished GPT-4 and Gemini could just *talk to each other*

...LLM Bridge was built for you.

---

## ✨ Features

- 🔄 **Seamless Model Switching** — Switch between Groq and Gemini mid-conversation with full context preserved
- 🧩 **Context Continuity Engine** — Automatically injects conversation history into new models as system context
- 💬 **Messenger-Style UI** — Clean chat interface with model-specific avatars and color-coded bubbles
- ⚡ **Auto Mode** — Both models analyze your prompt simultaneously with a unified synthesis
- 🥊 **Debate Mode** — Structured multi-round discussions between two AI models
- 📤 **Export Conversations** — Save sessions as Markdown for future reference
- 🎨 **Dark-Mode First** — Minimal, professional interface built for deep work sessions

### 🗂️ Sidebar Controls
- 🔥 **Model Selector** — Switch between Groq (Llama 3.1) and Gemini (2.0 Flash) with one click; active model is highlighted
- 🧠 **Context Strategy** — Three modes to control how much history is sent to the model:
  - `Full` — Entire conversation sent as-is
  - `Summary + 5` — Summarized context plus last 5 messages
  - `Last 5` — Only the 5 most recent messages (token-efficient)
- 👁️ **Context Preview** — Live preview of the conversation history being injected into the active model
- 📊 **Token Budget Bar** — Real-time token usage tracker with color-coded status (green → yellow → red) relative to each model's limit (16k for Groq, 200k for Gemini)
- 🗑️ **Reset Context** — One-click conversation and context wipe to start fresh

---

## 🖥️ Demo

```
User: "Help me design a REST API for a task manager"
→ [Groq responds with architecture outline]

User: [Switches to Gemini mid-conversation]
→ Gemini picks up with full context — no re-prompting needed
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A [Groq API key](https://console.groq.com)
- A [Gemini API key](https://aistudio.google.com)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/llm-bridge.git
cd llm-bridge

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### Run the App

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` and start chatting.

---

## 🗂️ Project Structure

```
llm-bridge/
├── app.py                  # Main Streamlit application
├── context_manager.py      # Core context continuity engine
├── models/
│   ├── groq_handler.py     # Groq API integration
│   └── gemini_handler.py   # Gemini API integration
├── utils/
│   ├── token_optimizer.py  # Token counting & compression
│   └── exporter.py         # Conversation export utilities
├── styles/
│   └── chat.css            # Custom UI styling
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🛣️ Roadmap

- [x] Groq + Gemini integration
- [x] Context continuity engine
- [x] Messenger-style chat UI
- [x] Auto Mode & Debate Mode
- [ ] GPT-4 + Claude integration
- [ ] Long-term memory store
- [ ] Auto model routing by task type
- [ ] Prompt library
- [ ] Team collaboration features
- [ ] REST API for developers
- [ ] Mobile app

---

## 🤝 Contributing

Contributions are welcome! Please open an issue first to discuss what you'd like to change.

```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Commit your changes
git commit -m "feat: add your feature"

# Push and open a PR
git push origin feature/your-feature-name
```

---

## 👤 Author

**Kshitij** · Product Manager & Builder
- GitHub: [@iamkshitij](https://github.com/iamkshitij)
- LinkedIn: [modikshitij](https://www.linkedin.com/in/modikshitij)

---

<p align="center">
  <i>Stop re-prompting. Start bridging.</i>
</p>
