"""
Author: YIDA zhuhansong@merach.com
Date: 2026-08-25 16:12:20
LastEditors: YIDA zhuhansong@merach.com
LastEditTime: 2026-08-25 16:13:11
FilePath: \server-py\apps\web-service\app\core\database.py
Description:

Copyright (c) 2026 by ${git_name_email}, All Rights Reserved.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from app.core.config import db_settings

_engine: AsyncEngine | None = None


def get_engine() -> AsyncEngine:
    global _engine

    if _engine is None:
        url = f"postgresql+asyncpg://{db_settings.user}:{db_settings.password}@{db_settings.host}:{db_settings.port}/{db_settings.name}"
        _engine = create_async_engine(
            url, pool_size=10, max_overflow=20, pool_pre_ping=True, echo=False
        )

    return _engine


_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    global _session_factory

    if _session_factory is None:
        _session_factory = async_sessionmaker(
            get_engine(),
            class_=AsyncSession,  # 明确指定使用异步 Session
            expire_on_commit=False,
            autoflush=True,
        )

    return _session_factory


async def get_db():
    async with get_session_factory().begin() as session:
        yield session
