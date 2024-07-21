from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db_session
from app.models.models import Users
from app.schemas.schemas import UserRegistration
from app.security import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


router = APIRouter()
TAG = ["Authentication"]


@router.post("/register", tags=TAG, status_code=status.HTTP_201_CREATED)
async def register_user(
    filters: UserRegistration,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db_session),
):
    user = Users(username=filters.username, password=hash_password(filters.password))

    # result = await db.execute(user)

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {"message": "Resource created."}


@router.post("/login", tags=TAG, status_code=status.HTTP_200_OK)
async def login_user(
    filter: UserRegistration,
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db_session),
):

    user = await db.execute(select(Users).where(Users.username == filter.username))

    user = user.scalars().one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {filter.username} not found.",
        )

    if not verify_password(filter.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password."
        )

    return {
        "access_token": create_access_token(filter.username),
        "token_type": "Bearer",
    }
