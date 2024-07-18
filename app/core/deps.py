from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app.core.database import async_session, engine
from app.models.models import Base


async def create_all_tables(engine: AsyncEngine = engine):

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session
