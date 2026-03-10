from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from typing import Generator
from app.core.config import settings
from app.db.base import Base

# Import models so SQLAlchemy metadata is populated for Alembic
from app.models import models  # noqa: F401


def _build_database_url() -> str:
    """Build DB URL from DATABASE_URL or fallback split env vars."""
    if settings.database_url:
        return settings.database_url

    required = {
        "DB_USERNAME": settings.db_username,
        "DB_PASSWORD": settings.db_password,
        "DB_HOSTNAME": settings.db_hostname,
        "DB_PORT": settings.db_port,
        "DB_NAME": settings.db_name,
    }
    missing = [key for key, value in required.items() if not value]
    if missing:
        missing_keys = ", ".join(missing)
        raise RuntimeError(
            f"Missing database configuration: {missing_keys}. "
            "Set DATABASE_URL or provide all DB_* variables."
        )

    return URL.create(
        drivername="postgresql+psycopg2",
        username=settings.db_username,
        password=settings.db_password,
        host=settings.db_hostname,
        port=int(settings.db_port),
        database=settings.db_name,
    ).render_as_string(hide_password=False)


DATABASE_URL = _build_database_url()

engine_kwargs = {
    "pool_pre_ping": True,
}

if settings.db_sslmode:
    engine_kwargs["connect_args"] = {"sslmode": settings.db_sslmode}

engine = create_engine(DATABASE_URL, **engine_kwargs)

# Tables are created via supabase_schema.sql in Supabase
# Commenting out auto-creation to avoid conflicts with existing tables
# Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
