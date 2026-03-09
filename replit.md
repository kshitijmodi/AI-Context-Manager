# LLM Bridge

## Overview

LLM Bridge is a Streamlit-based web application that enables users to interact with multiple Large Language Models simultaneously. The application queries both Groq and Google Gemini APIs in parallel, presenting responses from each model and potentially synthesizing them into a unified output. This multi-model approach allows users to compare AI responses and leverage the strengths of different LLM providers.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit (Python-based web framework)
- **Layout**: Wide layout configuration for optimal content display
- **Styling**: Custom CSS embedded via `st.markdown()` for dark theme with color-coded message boxes
  - Purple theme for user messages
  - Orange borders for Groq responses
  - Blue borders for Gemini responses
  - Purple borders for synthesized responses

### Backend Architecture
- **Language**: Python
- **Pattern**: Single-file application architecture with direct API integration
- **LLM Integration Strategy**: Parallel querying of multiple AI providers
  - Groq API for fast inference (likely using Llama or Mixtral models)
  - Google Generative AI (Gemini) for Google's foundation models

### Design Decisions
- **Multi-LLM Approach**: Rather than relying on a single AI provider, the app queries multiple models to enable comparison or synthesis of responses
- **Streamlit Choice**: Selected for rapid prototyping and built-in UI components, avoiding the need for separate frontend/backend codebases
- **No Database**: Application appears stateless with no persistent storage layer

## External Dependencies

### AI/LLM Services
- **Groq API** (`groq==0.4.1`): High-speed LLM inference platform
- **Google Generative AI** (`google-generativeai==0.8.0`): Access to Gemini models

### Additional API Libraries (in requirements but not visible in code)
- **Anthropic** (`anthropic==0.18.1`): Claude API client (may be planned for future use)
- **OpenAI** (`openai==1.12.0`): OpenAI API client (may be planned for future use)

### Frontend Dependencies
- **lucide-react**: Icon library (present in package.json but unclear usage with Streamlit app)

### Environment Variables Required
- Groq API key
- Google Generative AI API key