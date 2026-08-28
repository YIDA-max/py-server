# Makefile

.PHONY: dev debug test test-unit test-integration test-e2e test-smoke db-migrate db-upgrade db-downgrade

dev:
	uv run --package web-service fastapi dev apps/web-service/app/main.py --port 8080

debug:
	uv run --package web-service python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m fastapi dev apps/web-service/app/main.py --port 8000

test:
	uv run --package web-service pytest apps/web-service/test/unit apps/web-service/test/integration --cov=app --cov-report=term-missing --cov-fail-under=80

test-unit:
	uv run --package web-service pytest apps/web-service/test/unit

test-integration:
	uv run --package web-service pytest apps/web-service/test/integration

test-e2e:
	uv run --package web-service pytest apps/web-service/test/e2e

test-smoke:
	uv run --package web-service pytest apps/web-service/test -m smoke

db-migrate:
	uv run --package web-service alembic -c apps/web-service/alembic.ini revision --autogenerate -m "$(message)"

db-upgrade:
	uv run --package web-service alembic -c apps/web-service/alembic.ini upgrade head

db-downgrade:
	uv run --package web-service alembic -c apps/web-service/alembic.ini downgrade $(version)