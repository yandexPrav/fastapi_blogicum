#!/usr/bin/env sh
set -e

echo "[entrypoint] Ожидание доступности БД..."
python <<'PY'
import os
import time
from urllib.parse import urlparse

import socket

url = os.environ.get("DATABASE_URL", "")
parsed = urlparse(url)
host = parsed.hostname
port = parsed.port or 5432

if not host or parsed.scheme.startswith("sqlite"):
    print("[entrypoint] SQLite или локальная БД — ожидание не требуется.")
else:
    for attempt in range(60):
        try:
            with socket.create_connection((host, port), timeout=2):
                print(f"[entrypoint] БД {host}:{port} доступна.")
                break
        except OSError:
            print(f"[entrypoint] БД недоступна, попытка {attempt + 1}/60 ...")
            time.sleep(1)
    else:
        raise SystemExit(f"БД {host}:{port} недоступна после 60 попыток")
PY

echo "[entrypoint] Запуск миграций Alembic..."
alembic upgrade head

echo "[entrypoint] Запуск команды: $*"
exec "$@"
