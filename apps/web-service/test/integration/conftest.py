from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

import pytest
from httpx import ASGITransport, AsyncClient

from app.model.base import Base
from test.dbutil import async_url, drop_database, recreate_database

TEST_DB_NAME = "duyi_integration_test_db"


@pytest.fixture(scope="session", autouse=True)
def _integration_db():
    recreate_database(TEST_DB_NAME)
    yield
    drop_database(TEST_DB_NAME)


@pytest.fixture
async def db_session(_integration_db):
    engine = create_async_engine(async_url(TEST_DB_NAME), poolclass=NullPool)

    async with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(
                text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE')
            )

    session_factory = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with session_factory() as session:
        yield session

    await engine.dispose()


@pytest.fixture
async def async_client(db_session):
    from app.core.database import get_db
    from app.main import app

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://test", timeout=10.0
    ) as client:
        yield client
    app.dependency_overrides.clear()
