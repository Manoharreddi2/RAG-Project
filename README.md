# 📄 PDF Intelligence – AI-Powered PDF Question Answering System

PDF Intelligence is an AI-powered application that allows users to upload PDF documents and ask questions about their content. Instead of manually searching through lengthy documents, users can get relevant answers using AI.

The application uses **Retrieval-Augmented Generation (RAG)** to retrieve information from uploaded PDFs and generate answers with page-level citations.

## 🚀 Features

- Upload and manage multiple PDF documents.
- Extract text from uploaded PDFs.
- Generate embeddings and store them in ChromaDB.
- Ask questions in natural language.
- Get AI-generated answers based on document content.
- Display page-level citations for answers.
- Maintain conversation context for follow-up questions.
- Delete uploaded documents.
- No authentication required.
- Local-first architecture with persistent storage support.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| React + Vite | Frontend |
| Python | Backend |
| FastAPI | REST API |
| Groq | AI answer generation |
| Google Gemini | Text embeddings |
| ChromaDB | Vector database |
| RAG | Information retrieval and question answering |

## ⚙️ How It Works

1. Upload PDF documents.
2. Extract and split PDF text into smaller chunks.
3. Generate embeddings using Gemini.
4. Store embeddings in ChromaDB.
5. Retrieve relevant information based on user questions.
6. Generate grounded answers using Groq.
7. Display answers with page-level citations.

## 📂 Project Structure

```text
PDF-Intelligence/
│
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

## 💻 Installation and Setup

### Prerequisites

- Python 3.10+
- Node.js and npm
- Groq API Key
- Gemini API Key

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd PDF-Intelligence
```

### 2. Backend Setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Add your API keys to `backend/.env`:

```env
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key
```

Start the backend:

```bash
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite development URL in your browser:

```text
http://localhost:5173
```

## 🔗 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/documents/upload` | Upload PDF documents |
| GET | `/api/documents` | Get uploaded documents |
| DELETE | `/api/documents/{document_id}` | Delete a document |
| POST | `/api/chat` | Ask questions about PDFs |
| POST | `/api/chat/clear` | Clear chat history |
| GET | `/api/health` | Check backend health |

## 🔐 Environment Variables

Keep API
