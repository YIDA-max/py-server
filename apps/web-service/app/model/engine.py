"""
Author: YIDA zhuhansong@merach.com
Date: 2026-08-13 15:58:44
LastEditors: YIDA zhuhansong@merach.com
LastEditTime: 2026-08-14 16:39:33
FilePath: \server-py\apps\web-service\app\model\engine.py
Description:

Copyright (c) 2026 by ${git_name_email}, All Rights Reserved.
"""

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import db_settings

_engine: AsyncEngine | None = None


def get_engine() -> AsyncEngine:
    """获取数据库引擎"""
    # 全局变量
    global _engine

    if _engine is None:
        # 如果数据库引擎为空，则创建数据库引擎
        # 创建数据库连接URL
        url = f"postgresql+asyncpg://{db_settings.user}:{db_settings.password}@{db_settings.host}:{db_settings.port}/{db_settings.name}"
        # 创建数据库引擎
        _engine = create_async_engine(
            # 数据库连接URL
            url,
            # 连接池大小
            pool_size=10,
            # 连接池最大超额连接数
            max_overflow=20,
            # 连接池前检查是否存活
            pool_pre_ping=True,
            # 是否打印SQL日志
            echo=False,
        )

    return _engine
