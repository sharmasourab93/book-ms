# tests/test_schemas.py

import pytest
from app.schemas.schemas import Book, ModifyBook


def test_valid_book_schema():
    data = {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "genre": "Fiction",
        "published_year": 1925,
    }
    book = Book(**data)
    assert book.title == "The Great Gatsby"
    assert book.author == "F. Scott Fitzgerald"
    assert book.genre == "Fiction"
    assert book.published_year == 1925


def test_invalid_book_schema():
    with pytest.raises(ValueError):
        Book(title="Invalid Book", author="Author", genre="Genre", published_year="not_a_year")  # Should raise an error


def test_modify_book_schema():
    modify_data = {
        "title": "New Title",
        "author": None,
        "published_year": None,
        "genre": "New Genre",
    }
    modify_book = ModifyBook(**modify_data)
    assert modify_book.title == "New Title"
    assert modify_book.genre == "New Genre"
    assert modify_book.author is None
    assert modify_book.published_year is None