from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")
    groq_api_key: str = ""
    groq_model: str = "openai/gpt-oss-20b"
    gemini_api_key: str = ""
    gemini_embedding_model: str = "gemini-embedding-001"
    chunk_size: int = 1000
    chunk_overlap: int = 160
    max_upload_mb: int = 25
    upload_dir: Path = BASE_DIR / "uploads"
    chroma_dir: Path = BASE_DIR / "chroma_db"
    cors_origins: str = "http://localhost:5173"

settings = Settings()
settings.upload_dir.mkdir(parents=True, exist_ok=True)
settings.chroma_dir.mkdir(parents=True, exist_ok=True)
