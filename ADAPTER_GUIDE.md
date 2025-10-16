# Database Adapter Pattern Guide

## Overview

This application implements the **Adapter Pattern** to provide a flexible, configurable approach to database interactions. The adapter layer sits between the API and the database, allowing you to switch between different database systems without modifying your business logic.

## Architecture

```
┌─────────────────┐
│   FastAPI API   │  ← API Layer (app/)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Adapter Layer  │  ← Abstraction Layer (adapters/)
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌──────┐
│Postgres│ │MySQL │  ← Database Layer (db/)
└────────┘ └──────┘
```

## Directory Structure

```
adaptor/
├── adapters/              # Top-level adapter directory
│   ├── __init__.py
│   ├── factory.py        # Adapter factory and registry
│   └── database/         # Database-specific adapters
│       ├── __init__.py
|       ├── base.py           # Abstract base adapter interface
│       ├── postgres_adapter.py
│       └── mysql_adapter.py
├── app/                  # FastAPI application
│   ├── dependencies.py   # Dependency injection
│   ├── main.py          # Application entry point
│   └── routers/         # API routes
└── db/                   # Database models and sessions
    ├── postgres/
    └── mysql/
```

## Key Components

### 1. Base Adapter (`adapters/database/base.py`)

Defines the abstract interface that all adapters must implement:

```python
class BaseAdapter(ABC):
    async def create_book(...)
    async def get_book(...)
    async def get_books(...)
    async def update_book(...)
    async def delete_book(...)
    async def search_books(...)
    async def health_check(...)
```

### 2. Adapter Factory (`adapters/factory.py`)

Manages adapter registration and instantiation:

- **Registry Pattern**: Stores available adapter types
- **Singleton Pattern**: Ensures only one instance per adapter type
- **Dynamic Registration**: Allows adding new adapters at runtime

### 3. Concrete Adapters (`adapters/database/`)

Implement the `BaseAdapter` interface for specific databases:

- `PostgresAdapter` - PostgreSQL implementation
- `MySQLAdapter` - MySQL implementation

## Configuration

### Environment Variables

Set the database type in your `.env` file:

```bash
# Choose your database
DB_TYPE=postgres  # or 'mysql'

# PostgreSQL connection
SQLALCHEMY_POSTGRES_DATABASE_URI=postgresql+asyncpg://user:pass@host:5432/db

# MySQL connection (if using MySQL)
SQLALCHEMY_MYSQL_DATABASE_URI=mysql+aiomysql://user:pass@host:3306/db
```

### Switching Databases

To switch from PostgreSQL to MySQL:

1. Update `.env`:
   ```bash
   DB_TYPE=mysql
   ```

2. Restart the application

That's it! No code changes required.

## Adding a New Adapter

### Step 1: Create the Adapter Class

Create a new file in `adapters/database/` for DB adapters:

```python
# adapters/database/mongodb_adapter.py
from adapters.database.base import BaseAdapter

class MongoDBAdapter(BaseAdapter):
    @property
    def adapter_name(self) -> str:
        return "mongodb"
    
    async def create_book(self, title, author, year):
        # Your MongoDB implementation
        pass
    
    # Implement all other abstract methods...
```

### Step 2: Register the Adapter

Option A - Auto-registration in factory:

```python
# adapters/factory.py
def _register_default_adapters():
    from adapters.database import PostgresAdapter, MySQLAdapter, MongoDBAdapter
    
    AdapterFactory.register('postgres', PostgresAdapter)
    AdapterFactory.register('mysql', MySQLAdapter)
    AdapterFactory.register('mongodb', MongoDBAdapter)  # Add this
```

Option B - Manual registration at runtime:

```python
from adapters import AdapterFactory
from adapters.database.mongodb_adapter import MongoDBAdapter

AdapterFactory.register('mongodb', MongoDBAdapter)
```

### Step 3: Update Configuration

Add the new option to your config:

```python
# app/core/config.py
class Settings(BaseSettings):
    DB_TYPE: Literal["postgres", "mysql", "mongodb"] = "postgres"
```

## Usage in API Routes

The adapter is injected automatically via FastAPI dependency injection:

```python
from app.dependencies import DBAdapter

@router.post("/books")
async def create_book(book: BookCreate, db: DBAdapter):
    # db is automatically the correct adapter based on DB_TYPE
    result = await db.create_book(
        title=book.title,
        author=book.author,
        year=book.year
    )
    return result
```

## Benefits of This Pattern

1. **Separation of Concerns**: API logic is separate from database implementation
2. **Flexibility**: Switch databases without code changes
3. **Extensibility**: Easily add support for new databases
4. **Testability**: Mock adapters for unit testing
5. **Consistency**: All adapters follow the same interface
6. **Future-Proof**: Can add non-database adapters (APIs, caches, etc.)

## Future Adapter Examples

The adapter pattern isn't limited to databases. You could create:

- **Cache Adapters**: Redis, Memcached
- **Search Adapters**: Elasticsearch, Algolia
- **Storage Adapters**: S3, Azure Blob, Local filesystem
- **API Adapters**: External REST APIs, GraphQL
- **Message Queue Adapters**: RabbitMQ, Kafka, SQS

## Testing

Create mock adapters for testing:

```python
from adapters.base import BaseAdapter

class MockAdapter(BaseAdapter):
    def __init__(self):
        self.books = {}
    
    async def create_book(self, title, author, year):
        book_id = str(uuid4())
        self.books[book_id] = {...}
        return self.books[book_id]
    
    # Implement other methods...

# In tests
AdapterFactory.register('mock', MockAdapter)
```

## Best Practices

1. **Always implement all abstract methods** from `BaseAdapter`
2. **Include proper error handling** in your adapters
3. **Use consistent return types** (all adapters return dicts)
4. **Add logging** for debugging adapter operations
5. **Document adapter-specific behavior** in docstrings
6. **Keep adapters stateless** when possible (use singleton pattern)

## Troubleshooting

### Adapter Not Found Error

```
ValueError: Adapter 'xyz' is not registered
```

**Solution**: Make sure the adapter is registered in `adapters/factory.py`

### Import Errors

**Solution**: Check that all dependencies are installed:
```bash
uv sync
```

### Connection Errors

**Solution**: Verify environment variables are set correctly and database is running

## Example: Complete Adapter Flow

1. Request comes to API endpoint
2. FastAPI calls `get_db_adapter()` dependency
3. Dependency reads `DB_TYPE` from config
4. Factory returns appropriate adapter instance
5. Route handler calls adapter methods
6. Adapter interacts with specific database
7. Response returned through the chain

```
Client → API → Dependency → Factory → Adapter → Database → Response
```

---

For more information, see the main [README.md](README.md)

