import logging
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.models.schemas import ChatRequest, ChatResponse
from app.rag.store import store
from app.services.chat import ask
from app.services.documents import save_and_extract

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="PDF Intelligence API")
app.add_middleware(CORSMiddleware, allow_origins=[o.strip() for o in settings.cors_origins.split(",")], allow_methods=["*"], allow_headers=["*"])

@app.get("/api/health")
def health(): return {"status":"ok", "documents":len(store.list_documents()), "groq_configured":bool(settings.groq_api_key), "gemini_embeddings_configured":bool(settings.gemini_api_key)}
@app.get("/api/documents")
def documents(): return [{k:v for k,v in d.items() if k != "path"} for d in store.list_documents()]
@app.post("/api/documents/upload")
async def upload(files: list[UploadFile] = File(...)):
    results=[]
    for file in files:
        doc, chunks = await save_and_extract(file)
        try: results.append(store.add(doc, chunks))
        except Exception:
            from pathlib import Path; Path(doc["path"]).unlink(missing_ok=True); raise
    return {"documents":results}
@app.delete("/api/documents/{document_id}")
def delete_document(document_id: str):
    if not store.delete(document_id): raise HTTPException(404, "Document not found")
    return {"ok":True}
@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer, citations = ask(request.question, request.history)
    return {"answer":answer, "citations":citations}
@app.post("/api/chat/clear")
def clear(): return {"ok":True}
