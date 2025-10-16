from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    BACKEND_PORT: int
    
    # Database configuration
    DB_TYPE: Literal["postgres", "mysql"] = "postgres"
    
    # PostgreSQL
    SQLALCHEMY_POSTGRES_DATABASE_URI: str
    
    # MySQL
    SQLALCHEMY_MYSQL_DATABASE_URI: str | None = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()