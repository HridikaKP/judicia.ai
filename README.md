# judicia.ai


## 🎯 Project Objective

Judicia AI is an AI-powered legal chatbot that enables users to interact with legal documents such as IPC sections, case notes, and legal texts.

It uses Retrieval-Augmented Generation (RAG) to provide accurate, context-aware legal responses, making legal information easier to understand and access.

🧠 Custom LLM: LEGAL_TINYLAMA
⭐ Model Name

👉 hridika/LEGAL_TINYLAMA

## 🔍 About the Model

LEGAL_TINYLAMA is a domain-adapted legal language model built on TinyLLaMA, designed specifically for:

Understanding Indian Penal Code (IPC) sections

Interpreting legal terminology

Answering legal queries with contextual awareness

## ⚙️ Model Architecture

Base Model: TinyLLaMA

Type: Lightweight LLM

Domain Adaptation: Legal (IPC-based knowledge)

👉 Designed for:

Fast inference ⚡

Low resource usage 💻

Real-time chatbot applications

## 🧠 How the LLM Works

This project uses a hybrid LLM architecture:

🔹 Primary Model

👉 hridika/LEGAL_TINYLAMA

Provides domain-specific legal understanding

🔹 Supporting Models

LLaMA 3.1 (Groq – llama-3.1-8b-instant) → high-quality responses

Mistral-7B-Instruct (Hugging Face) → optional fallback

🔹 Enhancement

✔ Retrieval-Augmented Generation (RAG)
✔ FAISS vector database
✔ IPC-based document context injection

## ⭐ Key Insight

🧠 Judicia AI combines a custom legal LLM (LEGAL_TINYLAMA) with advanced LLMs using RAG to simulate a fine-tuned legal assistant.

🧩 Core Learning Outcomes

Build a domain-specific AI (Legal AI)

Implement RAG using LangChain

Work with vector databases (FAISS)

Integrate multiple LLM providers

Apply OOP for scalable AI systems

Develop interactive apps using Streamlit

## ⚙️ Tech Stack

| Category        | Technology                                   |
| --------------- | -------------------------------------------- |
| Frontend        | Streamlit                                    |
| Backend         | LangChain                                    |
| LLMs            | LEGAL_TINYLAMA, LLaMA 3.1 (Groq), Mistral-7B |
| Vector DB       | FAISS                                        |
| Embeddings      | all-MiniLM-L6-v2                             |
| Language        | Python 3.10+                                 |
| Env Management  | python-dotenv                                |
| Version Control | Git & GitHub                                 |

## 📁 Project Structure

judicia.ai/
│
├── app.py
│
├── chatbot/
│   ├── __init__.py
│   ├── config.py
│   ├── llm_handler.py
│   ├── document_handler.py
│   ├── chat_manager.py
│   └── utils.py
│
├── .env
├── requirements.txt
└── README.md

## ⚙️ Setup & Installation
🔹 1. Install Dependencies
pip install -r requirements.txt
🔹 2. Configure Environment
Create a .env file:

MODEL_PROVIDER=groq
GROQ_API_KEY=your_api_key
🔹 3. Run the Application
streamlit run app.py

<img width="1911" height="1010" alt="Screenshot 2026-03-17 194219" src="https://github.com/user-attachments/assets/6993968f-73db-4689-90f6-57502ca84198" />

🧱 System Workflow

Upload legal document (PDF / TXT)

Text is split into chunks

Embeddings are generated

Stored in FAISS vector database

User asks a legal query

Relevant context is retrieved

LLM generates response

## 🧩 OOP Modules

🔹 Config

Manages environment variables

Validates API keys

🔹 LLMHandler

Loads LEGAL_TINYLAMA / Groq / Hugging Face models

Handles LLM communication

🔹 DocumentHandler

Processes documents

Creates embeddings & FAISS index

🔹 ChatManager

Maintains chat history

Handles retrieval + response pipeline


## 💬 Features

✔ Chat with legal documents
✔ IPC-based legal understanding
✔ Context-aware answers
✔ Supports PDF & TXT files
✔ Fast response (Groq integration)
✔ Clean UI with Streamlit


## ⚖️ Use Cases

Legal education

IPC section understanding

Beginner legal assistance

Document summarization

## ⚠️ Disclaimer

This project is for educational purposes only.
It does not provide professional legal advice.

## 🧾 Git Workflow
git add .
git commit -m "feat: build Judicia AI with custom LEGAL_TINYLAMA model"
git push origin main
👩‍💻 Author

HRIDIKA KP &
MOHAMMED SHAMIL PK
