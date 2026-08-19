"""
Author: YIDA zhuhansong@merach.com
Date: 2026-08-17 16:47:31
LastEditors: YIDA zhuhansong@merach.com
LastEditTime: 2026-08-17 18:27:20
FilePath: \server-py\apps\web-service\app\core\database.py
Description: 数据库连接核心模块，提供异步 PostgreSQL 引擎和会话工厂。
             使用全局单例模式管理引擎和会话工厂，避免重复创建。
Copyright (c) 2026 by ${git_name_email}, All Rights Reserved.
"""

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from app.core.config import db_settings

# ---------- 异步数据库引擎（全局单例）----------
_engine: AsyncEngine | None = None


def get_engine() -> AsyncEngine:
    """
    获取或创建全局异步数据库引擎。

    使用连接池配置：
        - pool_size: 连接池常驻连接数
        - max_overflow: 最大临时溢出连接数（超出 pool_size 部分）
        - pool_pre_ping: 每次获取连接时检查连接可用性，避免使用已断开连接
        - echo: 是否打印 SQL 日志（生产环境建议 False）

    Returns:
        AsyncEngine: SQLAlchemy 异步引擎实例
    """
    global _engine

    if _engine is None:
        # 构建 PostgreSQL 异步连接 URL（使用 asyncpg 驱动）
        url = f"postgresql+asyncpg://{db_settings.user}:{db_settings.password}@{db_settings.host}:{db_settings.port}/{db_settings.name}"
        _engine = create_async_engine(
            url,
            pool_size=10,  # 核心连接池大小
            max_overflow=20,  # 最大溢出连接数
            pool_pre_ping=True,  # 自动重连检测
            echo=False,  # 生产环境关闭 SQL 日志
        )

    return _engine


# ---------- 异步会话工厂（全局单例）----------
_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """
    获取或创建全局异步会话工厂。

    会话工厂用于生成 AsyncSession 实例，每个会话代表一个数据库事务。
    配置：
        - class_: 指定使用异步 Session 类
        - expire_on_commit: 提交后是否使对象过期（False 保持对象可用）

    Returns:
        async_sessionmaker[AsyncSession]: 用于创建异步会话的工厂对象
    """
    global _session_factory

    if _session_factory is None:
        _session_factory = async_sessionmaker(
            get_engine(),  # 绑定到全局引擎
            class_=AsyncSession,  # 使用异步会话类
            expire_on_commit=False,  # 提交后不自动过期对象
        )

    return _session_factory
