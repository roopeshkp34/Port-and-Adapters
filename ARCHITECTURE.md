# Architecture Overview

## 🎯 Adapter Pattern Implementation

This application implements a clean **Adapter Pattern** architecture that separates concerns and provides flexibility for multiple database backends.

## 📐 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      CLIENT REQUEST                          │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   FASTAPI APPLICATION                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  app/routers/books.py                                 │  │
│  │  - POST   /books         (create_book)                │  │
│  │  - GET    /books         (get_books)                  │  │
│  │  - GET    /books/search  (search_books)               │  │
│  │  - GET    /books/{id}    (get_book)                   │  │
│  │  - PUT    /books/{id}    (update_book)                │  │
│  │  - DELETE /books/{id}    (delete_book)                │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  DEPENDENCY INJECTION                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  app/dependencies.py                                  │  │
│  │  - get_db_adapter() → BaseAdapter                     │  │
│  │  - Reads DB_TYPE from config                          │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    ADAPTER FACTORY                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  adapters/factory.py                                  │  │
│  │  - AdapterFactory.create(db_type)                     │  │
│  │  - Registry: {'postgres': PostgresAdapter, ...}      │  │
│  │  - Singleton pattern for adapter instances            │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│   POSTGRES ADAPTER       │  │     MYSQL ADAPTER        │
│  ┌────────────────────┐  │  │  ┌────────────────────┐  │
│  │ PostgresAdapter    │  │  │  │   MySQLAdapter     │  │
│  │ implements         │  │  │  │   implements       │  │
│  │ BaseAdapter        │  │  │  │   BaseAdapter      │  │
│  └────────────────────┘  │  │  └────────────────────┘  │
└────────────┬─────────────┘  └────────────┬─────────────┘
             │                             │
             ▼                             ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│   POSTGRES DATABASE      │  │     MYSQL DATABASE       │
│  ┌────────────────────┐  │  │  ┌────────────────────┐  │
│  │ SQLAlchemy Models  │  │  │  │ SQLAlchemy Models  │  │
│  │ Async Session      │  │  │  │ Async Session      │  │
│  │ PostgreSQL Driver  │  │  │  │ MySQL Driver       │  │
│  └────────────────────┘  │  │  └────────────────────┘  │
└──────────────────────────┘  └──────────────────────────┘
```

## 🔄 Request Flow

### Example: Creating a Book

```
1. Client sends POST /books
   └─> {"title": "1984", "author": "George Orwell", "year": 1949}

2. FastAPI routes to create_book(book: BookCreate, db: DBAdapter)
   └─> DBAdapter is injected via dependency

3. Dependency calls get_db_adapter()
   └─> Reads DB_TYPE from settings (e.g., "postgres")

4. Factory returns PostgresAdapter instance
   └─> AdapterFactory.create("postgres")

5. Route calls db.create_book(title, author, year)
   └─> PostgresAdapter.create_book() is executed

6. Adapter interacts with PostgreSQL database
   └─> Uses SQLAlchemy async session
   └─> Creates Book model instance
   └─> Commits to database

7. Response flows back through the chain
   └─> Returns book data as JSON
```

## 📦 Component Responsibilities

### 1. API Layer (`app/`)
**Responsibility**: Handle HTTP requests/responses, validation, routing

- Receives client requests
- Validates input using Pydantic schemas
- Delegates business logic to adapters
- Returns formatted responses
- **Does NOT** know about specific databases

### 2. Adapter Layer (`adapters/`)
**Responsibility**: Abstract data operations, provide unified interface

- **BaseAdapter**: Defines contract (abstract interface) in `adapters/database/base.py`
- **Factory**: Creates and manages adapter instances
- **Concrete Adapters**: Implement database-specific logic
- Converts database results to standard format (dicts)
- Handles database-specific errors

### 3. Database Layer (`db/`)
**Responsibility**: Database connections, models, sessions

- SQLAlchemy models (table definitions)
- Database sessions (connection pooling)
- Database-specific configurations
- Alembic migrations (PostgreSQL)

## 🔑 Key Design Patterns

### 1. Adapter Pattern
**Purpose**: Convert one interface to another

```python
# All adapters provide same interface (see adapters/database/base.py)
class BaseAdapter(ABC):
    async def create_book(...)
    async def get_book(...)
    # ... etc

# Different implementations, same interface
PostgresAdapter implements BaseAdapter
MySQLAdapter implements BaseAdapter
```

### 2. Factory Pattern
**Purpose**: Create objects without specifying exact class

```python
# Don't call constructors directly
adapter = PostgresAdapter()  ❌

# Use factory instead
adapter = AdapterFactory.create("postgres")  ✅
```

### 3. Singleton Pattern
**Purpose**: Ensure only one instance exists

```python
# Multiple calls return same instance
adapter1 = AdapterFactory.create("postgres")
adapter2 = AdapterFactory.create("postgres")
assert adapter1 is adapter2  # True
```

### 4. Dependency Injection
**Purpose**: Provide dependencies from outside

```python
# FastAPI automatically injects the adapter
@router.post("/books")
async def create_book(book: BookCreate, db: DBAdapter):
    # db is injected, not created here
    return await db.create_book(...)
```

## 🎛️ Configuration Flow

```
1. Environment Variables (.env)
   └─> DB_TYPE=postgres
   └─> SQLALCHEMY_POSTGRES_DATABASE_URI=...

2. Settings (app/core/config.py)
   └─> settings = Settings()
   └─> Reads from .env using pydantic-settings

3. Dependency (app/dependencies.py)
   └─> get_db_adapter() reads settings.DB_TYPE

4. Factory (adapters/factory.py)
   └─> Returns appropriate adapter

5. Application uses adapter
   └─> All DB operations go through adapter
```

## 🔧 Extension Points

### Adding a New Database Adapter

1. **Create adapter class** (`adapters/database/mongodb_adapter.py`)
2. **Inherit from BaseAdapter** (in `adapters/database/base.py`)
3. **Implement all abstract methods**
4. **Register in factory** (`adapters/factory.py`)
5. **Add configuration** (`app/core/config.py`)
6. **Done!** No changes to API code needed

### Adding a Non-Database Adapter

The pattern supports ANY data source:

```python
# Cache adapter
adapters/cache/redis_adapter.py

# Search adapter
adapters/search/elasticsearch_adapter.py

# External API adapter
adapters/external/google_books_adapter.py
```

## 📊 Benefits Summary

| Benefit | Description |
|---------|-------------|
| **Flexibility** | Switch databases via configuration |
| **Maintainability** | Clear separation of concerns |
| **Extensibility** | Easy to add new adapters |
| **Testability** | Mock adapters for testing |
| **Scalability** | Independent scaling of components |
| **Consistency** | Unified interface across data sources |

## 🎯 SOLID Principles Applied

- **Single Responsibility**: Each adapter handles one database
- **Open/Closed**: Open for extension (new adapters), closed for modification
- **Liskov Substitution**: Any adapter can replace another
- **Interface Segregation**: Clean, focused BaseAdapter interface
- **Dependency Inversion**: Depend on abstractions (BaseAdapter), not concretions

---

For implementation details, see [ADAPTER_GUIDE.md](ADAPTER_GUIDE.md)

