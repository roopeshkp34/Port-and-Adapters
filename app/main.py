from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.routers import books_router
from app.dependencies import get_db_adapter

app = FastAPI(
    title="FastAPI Database Adapter Application",
    description="A FastAPI application with configurable database adapters",
    version="0.1.0"
)

# Include routers
app.include_router(books_router)


@app.get("/")
async def index():
    """Index endpoint with API information"""
    return JSONResponse(
        content={
            "message": "Welcome to FastAPI Database Adapter Application",
            "status": "running",
            "configured_database": settings.DB_TYPE,
            "endpoints": {
                "docs": "/docs",
                "health": "/health",
                "books": "/books"
            }
        }
    )


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Checks the application status and database connectivity.
    """
    try:
        adapter = get_db_adapter()
        db_health = await adapter.health_check()
        
        return JSONResponse(
            content={
                "status": "healthy",
                "configured_adapter": settings.DB_TYPE,
                "database": db_health
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "configured_adapter": settings.DB_TYPE,
                "error": str(e)
            }
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.BACKEND_PORT)

