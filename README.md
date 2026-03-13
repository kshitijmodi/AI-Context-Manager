---
title: AI Context Manager
emoji: 💬
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: "1.32.0"
python_version: "3.10"
app_file: app.py
pinned: false
---

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

Whether you hit a token limit on one model or simply need a different model's strengths mid-task, LLM Bridge keeps your conversation intact and hands it off seamlessly. It also lets you pit two AIs against each other in a structured debate — and have a third AI judge the winner.

---

## 😤 The Problem

If you've ever:
- Hit a token limit mid-conversation and had to start over
- Copy-pasted your entire chat history into a new model
- Re-explained your project context for the fifth time this week
- Wondered what happens when two AIs actually argue with each other

...LLM Bridge was built for you.

---

## ✨ Features

- **Seamless Model Switching** — Switch between Groq and Gemini mid-conversation with full context preserved
- **Context Continuity Engine** — Automatically injects conversation history into new models as system context
- **Messenger-Style UI** — Clean chat interface with model-specific avatars and color-coded bubbles
- **Discussion Mode** — Chat with your selected AI; switch models at any point without losing context
- **Debate Mode** — Enter any topic and watch Gemini and Groq argue it out across 3 structured rounds, concluded by an impartial LLM judge
- **Dark-Mode First** — Minimal, professional interface built for deep work sessions

---

## 🆚 Discussion vs Debate Mode

LLM Bridge ships with two distinct interaction modes, switchable via a tab in the sidebar.

### Discussion Mode
The default mode. You pick a model (Groq or Gemini), ask questions, and switch models mid-conversation at any point. The context travels with you — the new model is fully briefed on everything discussed so far.

```
User: "Help me design a REST API for a task manager"
→ [Groq responds with architecture outline]
User: [Switches to Gemini mid-conversation]
→ Gemini picks up with full context — no re-prompting needed
```

### Debate Mode
You don't pick a model. Instead, you enter a topic and both AIs go head-to-head automatically across 3 rounds. No manual turn management — just type the topic and watch it unfold.

**How it works:**
1. You enter a debate topic (e.g. *"AI will replace software engineers"*)
2. Gemini opens with its strongest argument
3. Groq responds and challenges Gemini's position
4. This continues for 3 full rounds — each model building on and rebutting the last
5. A neutral LLM judge reviews the full transcript, identifies the strongest arguments from each side, and declares a winner with reasoning

Gemini bubbles appear left-aligned (blue), Groq right-aligned (orange). Each round is separated by a divider, and the judge's verdict appears in a distinct gold card at the end.

```
Topic: "Remote work is better than office work"

[Round 1] ────────────────────────────────
GEMINI  →  Opens with flexibility and productivity data
                        GROQ  →  Counters with collaboration and culture arguments

[Round 2] ────────────────────────────────
GEMINI  →  Rebuts with async tools and output-based metrics
                        GROQ  →  Pushes back on isolation and career growth risks

[Round 3] ────────────────────────────────
GEMINI  →  Final position: hybrid as a middle ground
                        GROQ  →  Final position: in-person wins for high-stakes work

⚖️ LLM JUDGE — VERDICT
Both sides made strong cases. Groq's focus on career development and
in-person collaboration for complex tasks was more concrete and evidence-grounded.
Winner: Groq
```

---

## 🗂️ Sidebar Controls

- **Mode Tab** — Switch between Discussion and Debate with a single click
- **Model Selector** *(Discussion only)* — Switch between Groq (Llama 3.1) and Gemini (2.0 Flash) with one click
- **Context Strategy** *(Discussion only)* — Three modes: `Full`, `Summary + 5`, or `Last 5 messages`
- **Context Preview** — Live preview of the history being injected into the active model
- **Token Budget Bar** — Real-time usage tracker with color-coded status relative to each model's limit (16k for Groq, 200k for Gemini)
- **Reset Context** — One-click wipe to start fresh

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- A [Groq API key](https://console.groq.com)
- A [Gemini API key](https://aistudio.google.com)

### Automatic deployment to Hugging Face Space

- This repo is wired so that **every push to the `main` branch on GitHub automatically mirrors the code to the Hugging Face Space** `iamkshitij/AI-Context-Manager`.
- The GitHub Actions workflow at `.github/workflows/deploy-hf.yml`:
  - Runs on `push` to `main`.
  - Uses the repository secret `GH_HF_AICONTEXTMGR` as the Hugging Face access token.
  - Pushes the `main` branch to `https://huggingface.co/spaces/iamkshitij/AI-Context-Manager`.
- To (re)configure in GitHub:
  - Go to **Settings → Secrets and variables → Actions**.
  - Add or update a **Repository secret** named `GH_HF_AICONTEXTMGR` with a valid Hugging Face access token that has write permission to the Space.

### Installation

```bash
git clone https://github.com/yourusername/llm-bridge.git
cd llm-bridge

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### Run

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

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
- [x] Discussion Mode with seamless model switching
- [x] Debate Mode — 3-round AI debate with LLM judge verdict
- [ ] GPT-4 + Claude integration
- [ ] Long-term memory store
- [ ] Auto model routing by task type
- [ ] Prompt library
- [ ] Team collaboration features
- [ ] REST API for developers
- [ ] Mobile app

---

## 🤝 Contributing

Contributions are welcome. Please open an issue first to discuss what you'd like to change.

```bash
git checkout -b feature/your-feature-name
git commit -m "feat: add your feature"
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
