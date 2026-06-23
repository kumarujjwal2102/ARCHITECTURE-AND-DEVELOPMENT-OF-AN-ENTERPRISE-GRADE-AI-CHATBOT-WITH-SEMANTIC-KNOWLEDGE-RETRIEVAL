# Enterprise AI Chatbot with Semantic Retrieval

A professional, locally-hosted RAG (Retrieval-Augmented Generation) chatbot using Ollama, ChromaDB, and FastAPI.

## Features
- **Semantic Retrieval (RAG)**: Answers questions based on uploaded PDF documents.
- **General Knowledge**: Can answer normal questions even without document context.
- **Local LLM**: Powered by Ollama (`llama3.2`).
- **Premium UI**: Modern, glassmorphic design with dark mode and smooth animations.
- **Privacy First**: Everything runs on your machine. No external APIs used.

## 🚀 Easy Start (Shortcut)
1. Double-click the `run_chatbot.bat` file in the root folder.
2. It will automatically start the server.
3. Once running, visit `http://localhost:8000`.

## 🛠️ Manual Setup
1. Open a terminal in the `backend` folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the server:
   ```bash
   python main.py
   ```
4. Open your browser at `http://localhost:8000`.

## Usage
1. Use the sidebar to upload a PDF.
2. Wait for the "Document indexed" notification.
3. Chat with the bot about your PDF content!
