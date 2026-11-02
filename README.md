# PDF Intelligence

A local-first PDF RAG application with no authentication. Upload PDFs, then ask grounded questions with page-level citations.

## Quick start

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload --port 8000
```

The application uses Groq for grounded chat answers and Gemini for embeddings. Configure `GROQ_API_KEY` and `GEMINI_API_KEY` in `backend/.env`. Missing credentials return a clear configuration error rather than fabricating an answer.

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open the displayed Vite address (normally `http://localhost:5173`). The development server proxies `/api` to FastAPI.

## Production notes

Set `UPLOAD_DIR` and `CHROMA_DIR` to mounted persistent volumes (not temporary storage). Set `CORS_ORIGINS` to the deployed frontend origin. The backend never exposes credentials to the browser.

## API

- `POST /api/documents/upload` multipart `files`
- `GET /api/documents`
- `DELETE /api/documents/{document_id}`
- `POST /api/chat` `{ question, history? }`
- `POST /api/chat/clear`
- `GET /api/health`
