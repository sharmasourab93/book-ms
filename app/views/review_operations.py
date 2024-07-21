from datetime import datetime
from typing import Dict, List, Optional, Union

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import BooksT, Reviews
from app.schemas.schemas import ReviewFullSchema, ReviewSchema

LATEST_REVIEW_LIMIT = 1


async def insert_reviews_by_id(
    book_id: int, body: ReviewSchema, db: AsyncSession
) -> Optional[ReviewFullSchema]:

    book = await db.execute(select(BooksT).where(BooksT.id == book_id))
    book = book.scalars().one_or_none()

    if book is None:
        return None

    review = Reviews(
        book_id=book_id,
        user_name=body.user_name,
        review_text=body.review_text,
        rating=body.rating,
    )
    db.add(review)
    await db.commit()
    await db.refresh(review)

    return review


async def get_reviews_by_id(book_id: int, db: AsyncSession) -> List[ReviewFullSchema]:

    result = await db.execute(select(Reviews).where(Reviews.book_id == book_id))
    return result.scalars().all()


SUMMARY_TYPE = Dict[str, Union[str, float]]


async def get_summary(book_id: int, db: AsyncSession) -> SUMMARY_TYPE:

    result = await db.execute(select(BooksT).where(BooksT.id == book_id))
    book = result.scalars().one_or_none()

    if book is None:
        return None

    result = await db.execute(
        select(func.avg(Reviews.rating)).where(Reviews.book_id == book_id)
    )
    avg_rating = result.scalar()

    result = await db.execute(
        select(Reviews)
        .where(Reviews.book_id == book_id)
        .order_by(desc(Reviews.created_at))
        .limit(LATEST_REVIEW_LIMIT)
    )
    latest_review = result.scalars().one_or_none()
    latest_review = None if latest_review is None else latest_review

    return {
        "title": book.title,
        "author": book.author,
        "genre": book.genre,
        "published_year": book.published_year,
        "average_rating": round(avg_rating, 2),
        "latest_review": latest_review,
    }
