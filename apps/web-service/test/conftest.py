import os
import sys
import time
import subprocess
from pathlib import Path
from contextlib import contextmanager

# ─── 必须在任何 app 导入之前设置环境变量 ───

os.environ.setdefault("DB_NAME", "duyi_test_db")
from app.core.config import db_settings

import pytest
import psycopg2

TEST_SERVER_PORT = "18000"
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
WEB_SERVICE_DIR = Path(__file__).resolve().parent.parent

_server_process: subprocess.Popen | None = None
_log_file = None
_log_path = REPO_ROOT / "tmp" / "test_server.log"


@contextmanager
def _create_cur():
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


def _drop_database(cur):
    cur.execute(
        f"SELECT pg_terminate_backend(pg_stat_activity.pid) "
        f"FROM pg_stat_activity "
        f"WHERE pg_stat_activity.datname = '{db_settings.name}' "
        f"AND pid <> pg_backend_pid()"
    )
    cur.execute(f"DROP DATABASE IF EXISTS {db_settings.name} WITH (FORCE)")


def _start_server():
    global _server_process, _log_file
    _log_path.parent.mkdir(exist_ok=True)
    _log_file = open(_log_path, "w", encoding="utf-8", errors="replace")

    env = os.environ.copy()
    env["DB_NAME"] = db_settings.name
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"

    _server_process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            TEST_SERVER_PORT,
            "--log-level",
            "warning",
        ],
        cwd=REPO_ROOT,
        stdout=_log_file,
        stderr=subprocess.STDOUT,
        env=env,
    )
    import httpx

    for _ in range(60):
        if _server_process.poll() is not None:
            break
        try:
            resp = httpx.get(
                f"http://127.0.0.1:{TEST_SERVER_PORT}/docs",
                timeout=1.0,
            )
            if resp.status_code == 200:
                return
        except Exception:
            pass
        time.sleep(0.25)

    log_tail = _log_path.read_text(encoding="utf-8", errors="replace")[-2000:]
    raise RuntimeError(
        f"测试服务器启动失败 (exit={_server_process.poll()})\n{log_tail}"
    )


def _stop_server():
    global _server_process, _log_file
    if _server_process is not None:
        _server_process.terminate()
        try:
            _server_process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            _server_process.kill()
            _server_process.wait(timeout=5)
        _server_process = None
    if _log_file is not None:
        _log_file.close()
        _log_file = None


def pytest_sessionstart(session):
    with _create_cur() as cur:
        _drop_database(cur)
        cur.execute(f"CREATE DATABASE {db_settings.name}")

    from alembic.config import Config
    from alembic import command

    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", str(WEB_SERVICE_DIR / "migrations"))
    alembic_cfg.set_main_option(
        "sqlalchemy.url",
        f"postgresql://{db_settings.user}:{db_settings.password}@{db_settings.host}:{db_settings.port}/{db_settings.name}",
    )
    command.upgrade(alembic_cfg, "head")

    _start_server()


def pytest_sessionfinish(session, exitstatus):
    _stop_server()

    with _create_cur() as cur:
        _drop_database(cur)


@pytest.fixture
def base_url():
    return f"http://127.0.0.1:{TEST_SERVER_PORT}"


@pytest.fixture
async def async_client():
    from httpx import AsyncClient

    async with AsyncClient(
        base_url=f"http://127.0.0.1:{TEST_SERVER_PORT}",
        timeout=10.0,
    ) as client:
        yield client


@pytest.fixture(autouse=True)
async def cleanup_db(async_client):
    yield
    from sqlalchemy import text
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.pool import NullPool
    from app.model.base import Base

    url = (
        f"postgresql+asyncpg://{db_settings.user}:{db_settings.password}"
        f"@{db_settings.host}:{db_settings.port}/{db_settings.name}"
    )
    engine = create_async_engine(url, poolclass=NullPool, echo=False)

    async with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(
                text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE')
            )
    await engine.dispose()
