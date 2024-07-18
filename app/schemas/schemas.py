from pydantic import BaseModel


class Book(BaseModel):
    title: str
    author: str
    genre: str
    published_year: int


class BooksReturnTypeSchema(BaseModel):
    id: int
    title: str
    author: str
    published_year: str
    genre: str
    create_at: str
    updated_at: str
