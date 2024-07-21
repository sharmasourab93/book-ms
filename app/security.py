import secrets
from datetime import datetime, timedelta
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt
from fastapi import HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = secrets.token_hex(64)
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"
CREDENTIAL_EXCEPTION = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                     detail="Could not validate credentials",
                                     headers={"Authorization": "Bearer "})


def create_access_token(username: str, expires_delta: timedelta = None):

    if expires_delta:
        expire = datetime.utcnow() + expires_delta

    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"sub": username, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub", None)

        if username is None:
            return False
        return True

    except JWTError:
        return False


def token_required(func):
    async def wrapper(*args, **kwargs):
        token = kwargs.get("token") or (await oauth2_scheme())
        if verify_token(token):
            return await func(*args, **kwargs)
        else:
            raise CREDENTIAL_EXCEPTION
    return wrapper
