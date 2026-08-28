import os
import sys
import tempfile
import time
import subprocess
from pathlib import Path

import pytest
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from app.model.base import Base
from test.dbutil import async_url, drop_database, recreate_database

TEST_DB_NAME = "duyi_e2e_test_db"
TEST_SERVER_PORT = "18000"
REPO_ROOT = Path(__file__).resolve().parents[4]

_server_process: subprocess.Popen | None = None
_log_file = None
_log_path = Path(tempfile.gettempdir()) / "web-service-e2e-server.log"


def _start_server():
    global _server_process, _log_file
    _log_file = open(_log_path, "w", encoding="utf-8", errors="replace")

    env = os.environ.copy()
    env["DB_NAME"] = TEST_DB_NAME
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
        f"e2e 测试服务器启动失败 (exit={_server_process.poll()})\n{log_tail}"
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


@pytest.fixture(scope="session", autouse=True)
def _e2e_server():
    recreate_database(TEST_DB_NAME)
    _start_server()
    yield
    _stop_server()
    drop_database(TEST_DB_NAME)


@pytest.fixture
def base_url():
    return f"http://127.0.0.1:{TEST_SERVER_PORT}"


@pytest.fixture
async def async_client():
    async with AsyncClient(
        base_url=f"http://127.0.0.1:{TEST_SERVER_PORT}",
        timeout=10.0,
    ) as client:
        yield client


@pytest.fixture(autouse=True)
async def cleanup_db(_e2e_server):
    yield
    engine = create_async_engine(async_url(TEST_DB_NAME), poolclass=NullPool, echo=False)
    async with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(
                text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE')
            )
    await engine.dispose()
