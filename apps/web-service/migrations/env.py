"""
Author: YIDA zhuhansong@merach.com
Date: 2026-08-19 18:13:57
LastEditors: YIDA zhuhansong@merach.com
LastEditTime: 2026-08-20 10:30:55
FilePath: \server-py\apps\web-service\migrations\env.py
Description: Alembic 迁移环境配置文件，用于配置数据库连接并执行迁移

Copyright (c) 2026 by ${git_name_email}, All Rights Reserved.
"""

from logging.config import fileConfig  # 用于从 alembic.ini 配置文件读取日志配置

from sqlalchemy import engine_from_config  # 根据配置创建数据库引擎
from sqlalchemy import pool  # 连接池相关类

from alembic import context  # Alembic 迁移上下文，包含迁移所需的环境信息

# 从项目配置中读取数据库连接信息（用户名、密码、主机、端口、数据库名等）
from app.core.config import db_settings

# 导入模型基类 Base（通过 app.model 包的 __init__.py 触发所有模型注册到 Base.metadata）
from app.model.base import Base

# Alembic 配置对象，用于读取 alembic.ini 中的配置项
config = context.config

# 如果存在 alembic.ini 配置文件，则根据其中的 [loggers] 等配置项配置 Python 日志
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 用项目配置覆盖 alembic.ini 中的占位 sqlalchemy.url。
# 测试里会先 set_main_option 指向独立测试库，此时不要再改回 .env 里的库名。
_current_url = config.get_main_option("sqlalchemy.url") or ""
if "://" not in _current_url or _current_url.startswith("driver://"):
    config.set_main_option(
        "sqlalchemy.url",
        f"postgresql://{db_settings.user}:{db_settings.password}@{db_settings.host}:{db_settings.port}/{db_settings.name}",
    )

# 告诉 Alembic 使用哪个模型的元数据，用于自动生成迁移脚本时对比模型与数据库差异
target_metadata = Base.metadata

# 其他配置项可通过 config.get_main_option() 获取


def run_migrations_offline() -> None:
    """
    离线模式执行迁移。
    该模式不会实际连接数据库，而是生成对应的 SQL 脚本并输出。
    适用于需要人工审查 SQL 或在无数据库连接的环境中生成迁移脚本的场景。
    """
    url = config.get_main_option("sqlalchemy.url")  # 从配置中获取数据库 URL
    context.configure(
        url=url,
        target_metadata=target_metadata,  # 指定目标元数据
        literal_binds=True,  # 将参数值直接字面量绑定到 SQL 中，便于生成可读脚本
        dialect_opts={"paramstyle": "named"},  # 使用命名参数风格
    )

    # 在事务中执行迁移
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    在线模式执行迁移。
    该模式会直接连接数据库并执行迁移操作，是实际开发中最常用的方式。
    """
    # 根据 alembic.ini 中的 [alembic] 配置节创建数据库引擎
    # poolclass=pool.NullPool 表示不使用连接池，每次连接用完即关闭，
    # 适合迁移这种一次性、短期连接的操作，避免长时间占用数据库连接
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",  # 只读取以 sqlalchemy. 开头的配置项
        poolclass=pool.NullPool,
    )

    # 获取一个数据库连接，并在该连接上执行迁移
    with connectable.connect() as connection:
        context.configure(
            connection=connection,  # 使用当前连接
            target_metadata=target_metadata,  # 指定目标元数据
        )

        # 在事务中执行迁移，确保迁移的原子性
        with context.begin_transaction():
            context.run_migrations()


# 根据 Alembic 的运行模式判断执行离线迁移还是在线迁移
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
