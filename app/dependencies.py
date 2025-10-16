from typing import Annotated

from fastapi import Depends

from app.core.config import settings
from adapters.database import BaseAdapter
from adapters import get_adapter


def get_db_adapter() -> BaseAdapter:
    """
    Dependency to get the configured database adapter.
    
    This will return the appropriate adapter (PostgreSQL, MySQL, etc.)
    based on the DB_TYPE configuration setting.
    
    The adapter is responsible for all database operations and abstracts
    the underlying database implementation from the API layer.
    """
    return get_adapter(settings.DB_TYPE)


# Type alias for cleaner dependency injection in route handlers
DBAdapter = Annotated[BaseAdapter, Depends(get_db_adapter)]

