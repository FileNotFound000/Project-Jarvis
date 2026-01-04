---
description: How to set up Ollama for local AI models
---

# Setting up Ollama on Windows

Ollama allows you to run powerful AI models like Llama 3 locally on your machine, which is free and private.

## 1. Download and Install
1.  Go to [ollama.com/download](https://ollama.com/download).
2.  Click **Download for Windows**.
3.  Run the installer (`OllamaSetup.exe`) and follow the prompts.

## 2. Verify Installation
1.  Open a new **Command Prompt** or **PowerShell** window.
2.  Type `ollama` and press Enter.
3.  You should see a help message with available commands.

## 3. Download a Model
To use the app, you need a model. We recommend `llama3` (8GB RAM required) or `llama3:8b`.

Run this command in your terminal:
```powershell
ollama pull llama3
```
*This will download the model (approx 4.7GB).*

## 4. Start the Server
Ollama usually runs in the background after installation. If not, run:
```powershell
ollama serve
```

## 5. Connect Antigravity
1.  Open the Antigravity App.
2.  Go to **Settings**.
3.  Select **AI Provider**: `Ollama (Local)`.
4.  Click **Save**.

## Troubleshooting
- **"Connection refused"**: Make sure `ollama serve` is running.
- **Slow performance**: Ensure you have GPU acceleration enabled or enough RAM.
