"""
PostgreSQL Database Adapter

This adapter implements the BaseAdapter interface for PostgreSQL databases.
"""

from typing import Any, List, Optional
from uuid import UUID, uuid4
from datetime import datetime

from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError

from adapters.database.base import BaseAdapter
from db.postgres.session import AsyncSessionLocal
from db.postgres.models import Book


class PostgresAdapter(BaseAdapter):
    """PostgreSQL database adapter implementation."""
    
    @property
    def adapter_name(self) -> str:
        return "postgresql"
    
    async def create_book(self, title: str, author: str, year: int) -> dict[str, Any]:
        """Create a new book record in PostgreSQL."""
        async with AsyncSessionLocal() as session:
            try:
                book = Book(
                    id=uuid4(),
                    title=title,
                    author=author,
                    year=year,
                )
                session.add(book)
                await session.commit()
                await session.refresh(book)
                
                return self._book_to_dict(book)
            except SQLAlchemyError as e:
                await session.rollback()
                raise Exception(f"PostgreSQL: Failed to create book: {str(e)}")
    
    async def get_book(self, book_id: UUID) -> Optional[dict[str, Any]]:
        """Get a book by ID from PostgreSQL."""
        async with AsyncSessionLocal() as session:
            try:
                stmt = select(Book).where(Book.id == book_id)
                result = await session.execute(stmt)
                book = result.scalar_one_or_none()
                
                return self._book_to_dict(book) if book else None
            except SQLAlchemyError as e:
                raise Exception(f"PostgreSQL: Failed to get book: {str(e)}")
    
    async def get_books(self, skip: int = 0, limit: int = 100) -> List[dict[str, Any]]:
        """Get all books with pagination from PostgreSQL."""
        async with AsyncSessionLocal() as session:
            try:
                stmt = select(Book).offset(skip).limit(limit).order_by(Book.created_on.desc())
                result = await session.execute(stmt)
                books = result.scalars().all()
                
                return [self._book_to_dict(book) for book in books]
            except SQLAlchemyError as e:
                raise Exception(f"PostgreSQL: Failed to get books: {str(e)}")
    
    async def update_book(
        self,
        book_id: UUID,
        title: Optional[str] = None,
        author: Optional[str] = None,
        year: Optional[int] = None
    ) -> Optional[dict[str, Any]]:
        """Update a book record in PostgreSQL."""
        async with AsyncSessionLocal() as session:
            try:
                # Build update values
                update_values = {}
                if title is not None:
                    update_values["title"] = title
                if author is not None:
                    update_values["author"] = author
                if year is not None:
                    update_values["year"] = year
                
                if not update_values:
                    # No updates provided, just return existing book
                    return await self.get_book(book_id)
                
                # Update the book
                stmt = (
                    update(Book)
                    .where(Book.id == book_id)
                    .values(**update_values)
                    .returning(Book)
                )
                result = await session.execute(stmt)
                await session.commit()
                book = result.scalar_one_or_none()
                
                return self._book_to_dict(book) if book else None
            except SQLAlchemyError as e:
                await session.rollback()
                raise Exception(f"PostgreSQL: Failed to update book: {str(e)}")
    
    async def delete_book(self, book_id: UUID) -> bool:
        """Delete a book record from PostgreSQL."""
        async with AsyncSessionLocal() as session:
            try:
                stmt = delete(Book).where(Book.id == book_id)
                result = await session.execute(stmt)
                await session.commit()
                
                return result.rowcount > 0
            except SQLAlchemyError as e:
                await session.rollback()
                raise Exception(f"PostgreSQL: Failed to delete book: {str(e)}")
    
    async def search_books(
        self,
        title: Optional[str] = None,
        author: Optional[str] = None,
        year: Optional[int] = None
    ) -> List[dict[str, Any]]:
        """Search books by title, author, or year in PostgreSQL."""
        async with AsyncSessionLocal() as session:
            try:
                stmt = select(Book)
                
                # Add filters
                if title:
                    stmt = stmt.where(Book.title.ilike(f"%{title}%"))
                if author:
                    stmt = stmt.where(Book.author.ilike(f"%{author}%"))
                if year:
                    stmt = stmt.where(Book.year == year)
                
                stmt = stmt.order_by(Book.created_on.desc())
                result = await session.execute(stmt)
                books = result.scalars().all()
                
                return [self._book_to_dict(book) for book in books]
            except SQLAlchemyError as e:
                raise Exception(f"PostgreSQL: Failed to search books: {str(e)}")
    
    async def health_check(self) -> dict[str, Any]:
        """Check PostgreSQL database connection health."""
        async with AsyncSessionLocal() as session:
            try:
                # Simple query to test connection
                await session.execute(select(1))
                return {
                    "adapter": self.adapter_name,
                    "status": "healthy",
                    "timestamp": datetime.utcnow().isoformat()
                }
            except SQLAlchemyError as e:
                return {
                    "adapter": self.adapter_name,
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                }
    
    @staticmethod
    def _book_to_dict(book: Book) -> dict[str, Any]:
        """Convert Book model to dictionary."""
        return {
            "id": str(book.id),
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "created_on": book.created_on.isoformat() if book.created_on else None
        }

