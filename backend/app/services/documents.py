import re, uuid
from datetime import datetime, timezone
from pathlib import Path
import fitz
from fastapi import HTTPException, UploadFile
from app.config import settings

def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def chunk_text(text: str):
    step = settings.chunk_size - settings.chunk_overlap
    if step <= 0: raise ValueError("CHUNK_OVERLAP must be lower than CHUNK_SIZE")
    return [text[i:i + settings.chunk_size] for i in range(0, len(text), step) if len(text[i:i + settings.chunk_size].strip()) > 40]

async def save_and_extract(upload: UploadFile) -> tuple[dict, list[dict]]:
    if upload.content_type not in {"application/pdf", "application/x-pdf"} and not (upload.filename or "").lower().endswith(".pdf"):
        raise HTTPException(415, f"{upload.filename}: only PDF files are supported")
    data = await upload.read()
    if len(data) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(413, f"{upload.filename}: exceeds {settings.max_upload_mb} MB limit")
    doc_id = str(uuid.uuid4())
    path = settings.upload_dir / f"{doc_id}.pdf"
    path.write_bytes(data)
    try:
        pdf = fitz.open(stream=data, filetype="pdf")
        chunks = []
        for page_num, page in enumerate(pdf, 1):
            for order, text in enumerate(chunk_text(clean(page.get_text()))):
                chunks.append({"id": f"{doc_id}-{page_num}-{order}", "text": text, "page": page_num})
        pdf.close()
    except Exception as exc:
        path.unlink(missing_ok=True)
        raise HTTPException(422, f"{upload.filename}: unreadable PDF ({exc})")
    if not chunks:
        path.unlink(missing_ok=True)
        raise HTTPException(422, f"{upload.filename}: no extractable text found")
    return ({"id": doc_id, "name": Path(upload.filename or "document.pdf").name, "size": len(data), "pages": max(c["page"] for c in chunks), "chunks": len(chunks), "uploaded_at": datetime.now(timezone.utc).isoformat(), "path": str(path)}, chunks)
