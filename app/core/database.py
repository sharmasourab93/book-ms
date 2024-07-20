import asyncio
import os

import asyncpg
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_USER = os.environ.get("DB_USER")
DB_PWD = os.environ.get("DB_PWD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB = os.environ.get("DB")


# For a local PostgreSQL database
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB}"
engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
