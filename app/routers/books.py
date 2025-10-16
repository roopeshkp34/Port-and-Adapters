from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from app.dependencies import DBAdapter
from app.schema.books import (
    BookCreate,
    BookResponse,
    BookUpdate,
)

router = APIRouter(prefix="/books", tags=["books"])


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: DBAdapter):
    """
    Create a new book.
    
    - **title**: Book title (required)
    - **author**: Book author (required)
    - **year**: Publication year (required)
    """
    try:
        result = await db.create_book(
            title=book.title,
            author=book.author,
            year=book.year
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create book: {str(e)}"
        )


@router.get("/", response_model=List[BookResponse])
async def get_books(
    db: DBAdapter,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return")
):
    """
    Get all books with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100, max: 1000)
    """
    try:
        books = await db.get_books(skip=skip, limit=limit)
        return books
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve books: {str(e)}"
        )


@router.get("/search", response_model=List[BookResponse])
async def search_books(
    db: DBAdapter,
    title: str | None = Query(None, description="Search by title (partial match)"),
    author: str | None = Query(None, description="Search by author (partial match)"),
    year: int | None = Query(None, description="Search by year (exact match)")
):
    """
    Search books by title, author, or year.
    
    - **title**: Search by title (partial match, case-insensitive)
    - **author**: Search by author (partial match, case-insensitive)
    - **year**: Search by publication year (exact match)
    """
    try:
        books = await db.search_books(title=title, author=author, year=year)
        return books
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search books: {str(e)}"
        )


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: UUID, db: DBAdapter):
    """
    Get a specific book by ID.
    
    - **book_id**: UUID of the book
    """
    try:
        book = await db.get_book(book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found"
            )
        return book
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve book: {str(e)}"
        )


@router.put("/{book_id}", response_model=BookResponse)
async def update_book(book_id: UUID, book_update: BookUpdate, db: DBAdapter):
    """
    Update a book by ID.
    
    - **book_id**: UUID of the book
    - **title**: New title (optional)
    - **author**: New author (optional)
    - **year**: New publication year (optional)
    """
    try:
        updated_book = await db.update_book(
            book_id=book_id,
            title=book_update.title,
            author=book_update.author,
            year=book_update.year
        )
        if not updated_book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found"
            )
        return updated_book
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update book: {str(e)}"
        )


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID, db: DBAdapter):
    """
    Delete a book by ID.
    
    - **book_id**: UUID of the book
    """
    try:
        deleted = await db.delete_book(book_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with id {book_id} not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete book: {str(e)}"
        )

