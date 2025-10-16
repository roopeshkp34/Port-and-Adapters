import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_MYSQL_DATABASE_URI = os.getenv("SQLALCHEMY_MYSQL_DATABASE_URI")

if not SQLALCHEMY_MYSQL_DATABASE_URI:
    # Provide a default or raise an error
    SQLALCHEMY_MYSQL_DATABASE_URI = None

if SQLALCHEMY_MYSQL_DATABASE_URI:
    engine = create_async_engine(
        SQLALCHEMY_MYSQL_DATABASE_URI,
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
else:
    engine = None
    AsyncSessionLocal = None

