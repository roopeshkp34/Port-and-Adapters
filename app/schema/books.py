from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BookBase(BaseModel):
    """Base schema for Book with common attributes."""
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    year: int = Field(..., ge=0, le=9999)


class BookCreate(BookBase):
    """Schema for creating a new book."""
    pass


class BookUpdate(BaseModel):
    """Schema for updating a book. All fields are optional."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    author: Optional[str] = Field(None, min_length=1, max_length=255)
    year: Optional[int] = Field(None, ge=0, le=9999)


class BookResponse(BookBase):
    """Schema for book response."""
    id: str
    created_on: Optional[str] = None
    
    class Config:
        from_attributes = True


class BookSearchParams(BaseModel):
    """Schema for searching books."""
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None