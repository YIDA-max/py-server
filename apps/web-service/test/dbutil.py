from contextlib import contextmanager
from pathlib import Path

import psycopg2
from alembic import command
from alembic.config import Config

from app.core.config import db_settings

WEB_SERVICE_DIR = Path(__file__).resolve().parent.parent


@contextmanager
def postgres_admin():
    conn = psycopg2.connect(  # pyright: ignore[reportCallIssue, reportArgumentType]
        host=db_settings.host,
        port=db_settings.port,
        user=db_settings.user,
        password=db_settings.password,
        dbname="postgres",
        connect_timeout=5,
    )
    conn.autocommit = True
    cur = conn.cursor()
    try:
        yield cur
    finally:
        cur.close()
        conn.close()


def recreate_database(name: str) -> None:
    with postgres_admin() as cur:
        cur.execute(
            "SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
            "WHERE datname = %s AND pid <> pg_backend_pid()",
            (name,),
        )
        cur.execute(f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)')
        cur.execute(f'CREATE DATABASE "{name}"')

    alembic_cfg = Config(str(WEB_SERVICE_DIR / "alembic.ini"))
    alembic_cfg.set_main_option("sqlalchemy.url", sync_url(name))
    command.upgrade(alembic_cfg, "head")


def drop_database(name: str) -> None:
    with postgres_admin() as cur:
        cur.execute(
            "SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
            "WHERE datname = %s AND pid <> pg_backend_pid()",
            (name,),
        )
        cur.execute(f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)')


def sync_url(name: str) -> str:
    return (
        f"postgresql://{db_settings.user}:{db_settings.password}"
        f"@{db_settings.host}:{db_settings.port}/{name}"
    )


def async_url(name: str) -> str:
    return (
        f"postgresql+asyncpg://{db_settings.user}:{db_settings.password}"
        f"@{db_settings.host}:{db_settings.port}/{name}"
    )
