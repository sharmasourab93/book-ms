from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import BooksT
from app.schemas.schemas import Book as BookSchema
from app.schemas.schemas import  BooksReturnTypeSchema


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
