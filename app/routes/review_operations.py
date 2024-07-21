from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db_session
from app.schemas.schemas import ReviewSchema
from app.security import token_required
from app.views.review_operations import (get_reviews_by_id, get_summary,
                                         insert_reviews_by_id)

router = APIRouter(prefix="/books/{book_id}")


@token_required
@router.post("/reviews", tags=["Reviews"], status_code=status.HTTP_201_CREATED)
async def post_reviews(
    book_id: int,
    body: ReviewSchema,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db_session),
):

    response = await insert_reviews_by_id(book_id, body, db)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"BookId: {book_id} not found"
        )

    return response


@token_required
@router.get("/reviews", tags=["Reviews"], status_code=status.HTTP_200_OK)
async def get_reviews(
    book_id: int,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db_session),
):
    return await get_reviews_by_id(book_id, db)


@token_required
@router.get("/summary", tags=["Reviews"], status_code=status.HTTP_200_OK)
async def get_summaries(
    book_id: int,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db_session),
):
    return await get_summary(book_id, db)
