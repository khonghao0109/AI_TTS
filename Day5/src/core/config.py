import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:01092004@localhost:5432/blog_db",
)
DB_ECHO = os.getenv("DB_ECHO", "false").lower() == "true"


@dataclass(frozen=True)
class Settings:
    database_url: str = DATABASE_URL
    db_echo: bool = DB_ECHO


settings = Settings()
