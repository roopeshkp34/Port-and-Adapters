import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_POSTGRES_DATABASE_URI = os.getenv("SQLALCHEMY_POSTGRES_DATABASE_URI")

if not SQLALCHEMY_POSTGRES_DATABASE_URI:
    raise ValueError("SQLALCHEMY_POSTGRES_DATABASE_URI environment variable is not set")

engine = create_async_engine(
    SQLALCHEMY_POSTGRES_DATABASE_URI,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=10,
    echo=False,
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)
