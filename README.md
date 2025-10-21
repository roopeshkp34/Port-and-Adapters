# FastAPI Database Adapter Application

A FastAPI application implementing the **Adapter Pattern** for flexible, configurable database interactions. Switch between PostgreSQL and MySQL (or add new databases) without changing your code.

## 🌟 Features

- **Adapter Pattern**: Clean separation between API and database layers
- **Configurable Databases**: Switch between PostgreSQL/MySQL via configuration
- **Extensible Architecture**: Easily add new database adapters or other data sources
- **FastAPI Framework**: Modern, fast Python web framework
- **Async Operations**: Full async/await support for database operations
- **Docker Ready**: Complete containerization with Docker Compose
- **Auto-generated API Docs**: Interactive Swagger UI and ReDoc

## 🏗️ Architecture

```
┌─────────────────┐
│   FastAPI API   │  ← API endpoints and business logic
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Adapter Layer  │  ← Database abstraction (adapters/)
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌──────┐
│Postgres│ │MySQL │  ← Actual database implementations
└────────┘ └──────┘
```

## 📁 Project Structure

```
adaptor/
├── adapters/              # Adapter layer (top-level)  
│   ├── factory.py        # Adapter factory & registry
│   └── database/         # Database-specific adapters
|       ├── base.py       # Abstract adapter interface
│       ├── postgres_adapter.py
│       └── mysql_adapter.py
├── app/                   # FastAPI application
│   ├── main.py           # Application entry point
│   ├── dependencies.py   # Dependency injection
│   ├── core/
│   │   └── config.py     # Configuration management
│   ├── routers/          # API route handlers
│   │   └── books.py
│   └── schema/           # Pydantic schemas
│       └── books.py
├── db/                    # Database layer
│   ├── postgres/         # PostgreSQL models & session
│   └── mysql/            # MySQL models & session
├── docker-compose.yml     # Docker orchestration
├── Dockerfile            # Container configuration
├── pyproject.toml        # Python dependencies
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker
- Docker Compose

### 1. Clone and Configure

```bash
# Clone the repository (if applicable)
git clone git@github.com:roopeshkp34/Port-and-Adapters.git
cd adaptor

# Create environment file
cp .env.example .env

# Edit .env to configure your database preference
# DB_TYPE=postgres  # or 'mysql'
```

### 2. Start with Docker Compose

```bash
# Build and start all services
docker-compose up --build
```

This starts three services:
- **server**: FastAPI application on port 8000 (published to host)
- **postgres_db**: PostgreSQL database on port 5432
- **mysql**: MySQL database on port 3306

### 3. Access the Application

- **API**: http://localhost:8000
- **Interactive Docs (Swagger)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔧 Configuration

### Database Selection

The application uses the `DB_TYPE` environment variable to determine which database to use:

**Option 1: PostgreSQL (default)**
```bash
# .env
DB_TYPE=postgres
SQLALCHEMY_POSTGRES_DATABASE_URI=postgresql+asyncpg://postgres:postgres@postgres_db:5432/fastapi_db
```

**Option 2: MySQL**
```bash
# .env
DB_TYPE=mysql
SQLALCHEMY_MYSQL_DATABASE_URI=mysql+aiomysql://root:mysql@mysql:3306/fastapi_db
```

**Switching databases**: Simply change `DB_TYPE` in `.env` and restart the container. No code changes needed!

Note: When running via Docker Compose, the app is published on host port 8000. Ensure your `.env` sets `BACKEND_PORT=8000` to match the compose mapping.

## 📚 API Endpoints

### General Endpoints

#### Index
```http
GET /
```
Returns welcome message and configured database type.

#### Health Check
```http
GET /health
```
Returns application health status and database connectivity.

### Book Management (CRUD)

#### Create a Book
```http
POST /books
Content-Type: application/json

{
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "year": 1925
}
```

#### Get All Books
```http
GET /books?skip=0&limit=100
```

#### Search Books
```http
GET /books/search?title=gatsby&author=fitzgerald&year=1925
```

#### Get Book by ID
```http
GET /books/{book_id}
```

#### Update a Book
```http
PUT /books/{book_id}
Content-Type: application/json

{
  "title": "Updated Title",
  "author": "Updated Author",
  "year": 2024
}
```

#### Delete a Book
```http
DELETE /books/{book_id}
```

For complete API documentation with examples, visit `/docs` after starting the application.

## 💡 How the Adapter Pattern Works

1. **Configuration**: Set `DB_TYPE` environment variable
2. **Dependency Injection**: FastAPI injects the correct adapter based on config
3. **Unified Interface**: All adapters implement the same methods
4. **Transparent Operations**: API code doesn't know which database it's using

```python
# Your route handler - works with any database!
@router.post("/books")
async def create_book(book: BookCreate, db: DBAdapter):
    # db is automatically the correct adapter (Postgres/MySQL)
    return await db.create_book(book.title, book.author, book.year)
```

## 🛠️ Development

### Running Locally (without Docker)

1. **Install dependencies**:
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -e .
   ```

2. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your local database credentials
   ```

3. **Run the application**:
   ```bash
   uvicorn app.main:app --reload --port ${BACKEND_PORT:-9020}
   ```

### Database Migrations (PostgreSQL)

```bash
# Create a new migration
cd db/postgres
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

### Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f server

# Stop services
docker-compose down

# Remove all data (including database volumes)
docker-compose down -v

# Rebuild after code changes
docker-compose up --build
```

### Access Database Directly

```bash
# PostgreSQL
docker-compose exec postgres_db psql -U postgres -d fastapi_db

# MySQL
docker-compose exec mysql mysql -u root -p fastapi_db
```

## 🔌 Adding New Adapters

Want to add MongoDB, Redis, or another data source? See [ADAPTER_GUIDE.md](ADAPTER_GUIDE.md) for detailed instructions.

**Quick example**:

1. Create `adapters/database/mongodb_adapter.py`
2. Implement `BaseAdapter` interface (in `adapters/database/base.py`)
3. Register in `adapters/factory.py`
4. Add `DB_TYPE="mongodb"` option to config
5. Done! 🎉

## 📋 Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `BACKEND_PORT` | Application port | `8000` (Docker), `9020` (local default) | Yes |
| `DB_TYPE` | Database type (`postgres`/`mysql`) | `postgres` | Yes |
| `SQLALCHEMY_POSTGRES_DATABASE_URI` | PostgreSQL connection string | - | If using postgres |
| `SQLALCHEMY_MYSQL_DATABASE_URI` | MySQL connection string | - | If using mysql |

## 🧪 Testing

```bash
# Run tests (when implemented)
pytest

# With coverage
pytest --cov=app --cov=adapters
```

## 🐛 Troubleshooting

### "Adapter 'xyz' is not registered"
- Check that the adapter is registered in `adapters/factory.py`
- Ensure imports are correct

### Connection refused errors
- Verify database container is running: `docker-compose ps`
- Check connection strings in `.env`
- Ensure database has started (may take a few seconds)

### Import errors
- Run `uv sync` to install all dependencies
- Check Python version is >= 3.12

## 📖 Additional Documentation

- [ADAPTER_GUIDE.md](ADAPTER_GUIDE.md) - Complete guide to the adapter pattern
- [Interactive API Docs](http://localhost:9020/docs) - After starting the app

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

