import json
import chromadb
import httpx
from fastapi import HTTPException
from app.config import settings

class RagStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=str(settings.chroma_dir))
        self.collection = self.client.get_or_create_collection("pdf_chunks", metadata={"hnsw:space": "cosine"})
        self.docs_file = settings.chroma_dir / "documents.json"

    def _docs(self):
        return json.loads(self.docs_file.read_text()) if self.docs_file.exists() else []
    def _save_docs(self, docs): self.docs_file.write_text(json.dumps(docs, indent=2))
    def list_documents(self): return self._docs()
    def _embed(self, texts, task_type="RETRIEVAL_DOCUMENT"):
        if not settings.gemini_api_key:
            raise HTTPException(503, "Gemini embeddings are not configured. Add GEMINI_API_KEY to backend/.env and restart the server.")
        try:
            model = settings.gemini_embedding_model
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:batchEmbedContents"
            vectors = []
            for start in range(0, len(texts), 64):
                batch = texts[start:start + 64]
                payload = {"requests": [{"model": f"models/{model}", "content": {"parts": [{"text": text}]}, "taskType": task_type} for text in batch]}
                response = httpx.post(url, headers={"x-goog-api-key": settings.gemini_api_key}, json=payload, timeout=60)
                response.raise_for_status()
                vectors.extend(item["values"] for item in response.json()["embeddings"])
            return vectors
        except Exception as exc:
            raise HTTPException(502, f"Gemini embedding request failed: {exc}")
    def add(self, document, chunks):
        vectors = self._embed([c["text"] for c in chunks])
        self.collection.add(ids=[c["id"] for c in chunks], documents=[c["text"] for c in chunks], embeddings=vectors, metadatas=[{"document_id": document["id"], "document_name": document["name"], "page": c["page"]} for c in chunks])
        public = {k:v for k,v in document.items() if k != "path"}
        self._save_docs(self._docs() + [document])
        return public
    def delete(self, document_id):
        docs = self._docs(); target = next((d for d in docs if d["id"] == document_id), None)
        if not target: return False
        self.collection.delete(where={"document_id": document_id})
        self._save_docs([d for d in docs if d["id"] != document_id])
        from pathlib import Path; Path(target["path"]).unlink(missing_ok=True)
        return True
    def search(self, question, limit=5):
        if not self._docs(): return []
        vector = self._embed([question], "RETRIEVAL_QUERY")
        result = self.collection.query(query_embeddings=vector, n_results=min(limit, self.collection.count()), include=["documents", "metadatas", "distances"])
        return [{"text": text, **meta, "distance": distance} for text, meta, distance in zip(result["documents"][0], result["metadatas"][0], result["distances"][0])]

store = RagStore()
