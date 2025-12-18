from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Supabase Config
    supabase_url: str
    supabase_key: str
    
    # Database Config (Supabase PostgreSQL)
    db_username: str
    db_password: str
    db_hostname: str
    db_port: str
    db_name: str

    # JWT Config
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
