from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db_session
from app.schemas.schemas import Book, BooksReturnTypeSchema, ModifyBook
from app.views.operations import (delete_book_by_id, get_all_books,
                                  get_book_id, insert_book_operation,
                                  update_book_by_id)

router = APIRouter(prefix="/books")


@router.post("/", tags=["Books"], status_code=status.HTTP_201_CREATED)
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


@router.get("/", tags=["Books"], status_code=status.HTTP_200_OK)
async def get_books(
    request: Request, response: Response, db: AsyncSession = Depends(get_db_session)
):

    response = await get_all_books(db)

    return response


@router.get("/{book_id}", tags=["Books"], status_code=status.HTTP_200_OK)
async def get_books_by_id(
    book_id: int,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db_session),
):
    response = await get_book_id(book_id, db)

    if response is not None:
        return response

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Book Not " "Found."
    )


@router.put("/{book_id}", tags=["Books"], status_code=status.HTTP_200_OK)
async def update_books(
    book_id: int,
    filters: ModifyBook,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db_session),
):

    response = await update_book_by_id(book_id, filters, db)

    if response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book Not found."
        )

    return response


@router.delete("/{book_id}", tags=["Books"], status_code=status.HTTP_200_OK)
async def delete_books(
    book_id: int,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db_session),
):

    response = await delete_book_by_id(book_id, db)

    if response is False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Record not found."
        )

    return {"message": "Successfully deleted record."}
