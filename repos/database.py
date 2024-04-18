from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from settings import settings


async_engine = create_async_engine(
    url=settings.get_pg_connection,
    echo=False,
    max_overflow=10,
    pool_size=5
)

async_session = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession
)



