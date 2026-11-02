from pydantic import BaseModel, Field

class Citation(BaseModel):
    document_id: str
    document_name: str
    page: int
    excerpt: str

class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    history: list[dict[str, str]] = Field(default_factory=list)

class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation]
