from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db_session
from app.schemas.schemas import Book
from app.views.operations import get_all_books, insert_book_operation

router = APIRouter(prefix="/books")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_books(
    body: Book,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db_session),
):

    response = await insert_book_operation(body, db)

    if response:
        return {"status": "Resource Created."}

    else:
        return {"status": "Resource couldn't be created."}


@router.get("/", status_code=status.HTTP_200_OK)
async def get_books(
    request: Request, response: Response, db: AsyncSession = Depends(get_db_session)
):

    response = await get_all_books(db)

    return response
