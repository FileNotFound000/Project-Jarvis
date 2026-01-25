# Project K
> *Formerly known as Project Jarvis / Aether*

**Project K** is an advanced, locally-hosted AI assistant designed to be a "Second Brain" for your computer. It combines local LLM inference with autonomous web research, system control, computer vision, and a futuristic voice interface.

## Key Features

- **Local & Private Intelligence**
  - Powered by **Ollama** (supports Llama 3, Mistral) or **Gemini 2.5 Flash**.
  - **Second Brain (RAG)**: Ingest, search, and forget local files (PDF, Code, Text).
  - **Memory**: Persistent long-term memory of user preferences and facts.

- **"Always-On" Voice Interface**
  - **Wake Word**: Just say **"Karan"**, **"Computer"**, or **"Jarvis"** (Powered by Vosk Offline).
  - **Interactive Mode**: Replies "Yes Boss" and listens for commands.
  - **Smart Media**: "Play [Song] on YouTube" plays directly (no search results).

- ** Deep Research Agent**
  - Recursive web research capabilities.
  - Can search the web, scrape content, and synthesize comprehensive reports on complex topics.
  - Usage: *"Research the history of quantum computing"*

- **Deep System Control**
  - **Macros ("Jarvis Protocols")**: Trigger complex setups (Work/Game/Sleep) with one command.
  - **Automation**: Open apps, control volume/media/brightness/power.
  - **High-Speed Typing**: Dictate essays or code directly into apps.

- **Deep Research Agent**
  - Recursive web research with unicode support.
  - Synthesizes comprehensive reports from multiple sources.

- **Autonomous Coding Agent**
  - **Read & Write**: Can read your project files and create new code files.
  - **Patch & Fix**: Can surgically edit files to fix bugs or add features.

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **AI Orchestration**: Custom Agent (ReAct Loop)
- **Vision**: Gemini 1.5/2.0 Flash
- **Vector DB**: ChromaDB (RAG)
- **Speech**: Vosk (STT) + Edge TTS

### Frontend
- **Framework**: Next.js (React / TypeScript)
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **State**: React Hooks (Custom Voice Hooks)

## Getting Started

### Prerequisites
- **Python** 3.10+
- **Node.js** 18+
- **Gemini API Key** (Google AI Studio)
- **Ollama** (Optional, for local inference)

### Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/FileNotFound000/Project-K.git
    cd Project-K
    ```

2.  **Backend Setup**
    ```bash
    cd backend
    # Create virtual environment
    python -m venv .venv
    
    # Activate (Windows)
    .venv\Scripts\activate
    # Activate (Mac/Linux)
    # source .venv/bin/activate
    
    # Install dependencies
    pip install -r requirements.txt
    ```

3.  **Frontend Setup**
    ```bash
    cd frontend
    npm install
    ```

### Running the Application

1.  **Start Backend**
    ```bash
    cd backend
    uvicorn main:app --reload
    ```
    *Server: http://localhost:8000*

2.  **Start Frontend**
    ```bash
    cd frontend
    npm run dev
    ```
    *Client: http://localhost:3000*

## Usage Guide

-   **Voice Mode**: Toggle "VOICE OFF" -> "VOICE ON". Say **"Computer"** to wake.
-   **Macros**: "Activate Work Mode" (VS Code + Spotify).
-   **Second Brain**: "Memorize `plan.pdf`", then "What's in the plan?".
-   **Vision**: "Click the [Description]".

## Roadmap & Status
Check [PROJECT_STATUS.md](./PROJECT_STATUS.md) for the latest tracking.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

##  License
[MIT](LICENSE)
