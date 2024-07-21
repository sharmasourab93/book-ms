from datetime import datetime
from typing import List, Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import BooksT
from app.schemas.schemas import Book as BookSchema
from app.schemas.schemas import BooksReturnTypeSchema, ModifyBook


async def insert_book_operation(data: BookSchema, db: AsyncSession) -> bool:

    book = BooksT(**data.dict())

    try:
        db.add(book)
        await db.commit()
        await db.refresh(book)
        return True

    except Exception as e:
        return False


async def get_all_books(db: AsyncSession) -> List[BooksReturnTypeSchema]:

    books = await db.execute(select(BooksT))
    data = books.scalars().all()
    return data


async def get_book_id(book_id: int, db: AsyncSession) -> BooksReturnTypeSchema:

    book = await db.execute(select(BooksT).where(BooksT.id == book_id))
    book = book.scalars().one_or_none()

    return book


async def update_book_by_id(
    book_id: int, book: BookSchema, db: AsyncSession
) -> Optional[BooksReturnTypeSchema]:

    result = await db.execute(select(BooksT).where(BooksT.id == book_id))

    exisiting_book = result.scalars().one_or_none()

    if exisiting_book is None:
        return None

    exisiting_book.title = (
        book.title if book.title is not None else (exisiting_book.title)
    )
    exisiting_book.author = (
        book.author if book.author is not None else (exisiting_book.author)
    )
    exisiting_book.genre = (
        book.genre if book.genre is not None else exisiting_book.genre
    )
    exisiting_book.published_year = (
        book.published_year
        if book.published_year is not None
        else (exisiting_book.published_year)
    )
    exisiting_book.updated_at = datetime.utcnow()

    db.add(exisiting_book)
    await db.commit()
    await db.refresh(exisiting_book)

    return exisiting_book


async def delete_book_by_id(book_id: int, db: AsyncSession) -> bool:

    book = get_book_id(book_id, db)

    if book is None:
        return False

    await db.execute(delete(BooksT).where(BooksT.id == book_id))
    await db.commit()

    return True
