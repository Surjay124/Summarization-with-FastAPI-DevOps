import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

class Settings:
    PROJECT_NAME: str = "AI Summarizer Service"
    MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    API_V1_STR: str = "/api/v1"
    
    # Database Configuration
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "app_db")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "db")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # 1. Prefer explicit DATABASE_URL
        if os.getenv("DATABASE_URL"):
             return os.getenv("DATABASE_URL")
        
        # 2. Check if validation/production postgres is intended
        # We check if POSTGRES_SERVER/HOST is explicitly set to something other than default, 
        # or if a specific flag is set. For Docker, we will set these.
        if os.getenv("POSTGRES_HOST") or os.getenv("USE_POSTGRES"):
            return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        
        # 3. Default to SQLite for local development
        return f"sqlite:///{DATA_DIR}/app.db"

    
    # Logging
    LOG_FILE_PATH: str = str(DATA_DIR / "ai_interactions.log")

settings = Settings()
