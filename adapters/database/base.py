"""
Base Adapter Interface

This module defines the abstract base class for all adapters.
All adapters must implement these methods to ensure consistent behavior.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Optional
from uuid import UUID


class BaseAdapter(ABC):
    """
    Abstract base class for all data source adapters.
    
    This interface defines the contract that all adapters must follow,
    ensuring consistent CRUD operations regardless of the underlying data source.
    """
    
    @abstractmethod
    async def create_book(self, title: str, author: str, year: int) -> dict[str, Any]:
        """
        Create a new book record.
        
        Args:
            title: Book title
            author: Book author
            year: Publication year
            
        Returns:
            Dictionary containing the created book data
            
        Raises:
            Exception: If the operation fails
        """
        pass
    
    @abstractmethod
    async def get_book(self, book_id: UUID) -> Optional[dict[str, Any]]:
        """
        Retrieve a book by its ID.
        
        Args:
            book_id: Unique identifier of the book
            
        Returns:
            Dictionary containing book data if found, None otherwise
            
        Raises:
            Exception: If the operation fails
        """
        pass
    
    @abstractmethod
    async def get_books(self, skip: int = 0, limit: int = 100) -> List[dict[str, Any]]:
        """
        Retrieve all books with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of dictionaries containing book data
            
        Raises:
            Exception: If the operation fails
        """
        pass
    
    @abstractmethod
    async def update_book(
        self, 
        book_id: UUID, 
        title: Optional[str] = None,
        author: Optional[str] = None,
        year: Optional[int] = None
    ) -> Optional[dict[str, Any]]:
        """
        Update a book record.
        
        Args:
            book_id: Unique identifier of the book
            title: New title (optional)
            author: New author (optional)
            year: New publication year (optional)
            
        Returns:
            Dictionary containing updated book data if found, None otherwise
            
        Raises:
            Exception: If the operation fails
        """
        pass
    
    @abstractmethod
    async def delete_book(self, book_id: UUID) -> bool:
        """
        Delete a book record.
        
        Args:
            book_id: Unique identifier of the book
            
        Returns:
            True if deleted successfully, False if not found
            
        Raises:
            Exception: If the operation fails
        """
        pass
    
    @abstractmethod
    async def search_books(
        self,
        title: Optional[str] = None,
        author: Optional[str] = None,
        year: Optional[int] = None
    ) -> List[dict[str, Any]]:
        """
        Search books by criteria.
        
        Args:
            title: Search by title (partial match)
            author: Search by author (partial match)
            year: Search by year (exact match)
            
        Returns:
            List of dictionaries containing matching book data
            
        Raises:
            Exception: If the operation fails
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> dict[str, Any]:
        """
        Check the health/connectivity of the data source.
        
        Returns:
            Dictionary containing health status information
        """
        pass
    
    @property
    @abstractmethod
    def adapter_name(self) -> str:
        """
        Return the name of this adapter.
        
        Returns:
            String identifier for this adapter
        """
        pass

