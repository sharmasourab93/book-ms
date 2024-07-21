from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Book(BaseModel):
    title: str
    author: str
    genre: str
    published_year: int


class ModifyBook(BaseModel):
    title: Optional[str]
    author: Optional[str]
    published_year: Optional[int]
    genre: Optional[str]


class BooksReturnTypeSchema(BaseModel):
    id: int
    title: str
    author: str
    published_year: str
    genre: str
    create_at: str
    updated_at: str


class ReviewSchema(BaseModel):
    user_name: str
    review_text: str
    rating: float


class ReviewFullSchema(BaseModel):
    id: int
    book_id: int
    user_name: str
    review_text: str
    rating: float
    created_at: datetime
