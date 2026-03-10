from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Supabase Config
    supabase_url: str
    supabase_key: str

    # Database Config (Supabase PostgreSQL)
    # Preferred in production/Render: set DATABASE_URL
    database_url: Optional[str] = None

    # Fallback split fields (used if DATABASE_URL is not provided)
    db_username: Optional[str] = None
    db_password: Optional[str] = None
    db_hostname: Optional[str] = None
    db_port: Optional[str] = None
    db_name: Optional[str] = None
    db_sslmode: str = "require"

    # JWT Config
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
