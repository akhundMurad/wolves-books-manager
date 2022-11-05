#!/bin/sh

alembic upgrade head
gunicorn -b 0.0.0.0:8000 --worker-class uvicorn.workers.UvicornWorker src.presentation.api.asgi:asgi
