from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# BASE_DIR = /TFM/backend
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    # Variables públicas
    PUBLIC_BACKEND_URL: str = "http://127.0.0.1:8000"

    # Configuración obligatoria cargada desde .env
    ENVIRONMENT: str
    HOST: str
    PORT: int
    SQLALCHEMY_DATABASE_URL: str
    OPENAI_API_KEY: str
    OPENAI_MODEL: str
    OPENWEBUI_DB_PATH: str

    # Opcionales con valores por defecto
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "openai-compatible-model"

    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8"
    )

settings = Settings() # type: ignore
