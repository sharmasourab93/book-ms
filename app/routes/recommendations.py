from fastapi import APIRouter, status, Request, Response, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_db_session


router = APIRouter(prefix="/recommendation")


@router.get("/", status_code=status.HTTP_200_OK, tags=["Recommendations"])
async def get_recommendations(request: Request, response: Response,
                              db: AsyncSession = Depends(get_db_session)):

    return {"message": "API in works."}
