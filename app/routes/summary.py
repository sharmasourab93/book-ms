from app.core.deps import get_db_session
from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/summaries")


@router.get("/", status_code=status.HTTP_200_OK, tags=["Summary"])
async def get_lama_summaries(
    request: Request, response: Response, db: AsyncSession = Depends(get_db_session)
):

    return {"message": "API in works."}
