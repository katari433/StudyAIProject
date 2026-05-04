#!/usr/bin/env bash
set -euo pipefail

# Wait for Postgres to be available (if DATABASE_URL points to postgres)
echo "Starting entrypoint: waiting for DB (if applicable) and running migrations..."

if [[ -n "${DATABASE_URL:-}" ]] && [[ "$DATABASE_URL" == postgresql* ]]; then
  # extract host and port
  python - <<'PY'
import os, time
from urllib.parse import urlparse
u = urlparse(os.environ['DATABASE_URL'])
host = u.hostname or 'postgres'
port = u.port or 5432
user = u.username or 'postgres'
print(f'Waiting for Postgres at {host}:{port}...')
import socket
for _ in range(30):
    try:
        with socket.create_connection((host, port), timeout=2):
            print('Postgres is accepting connections')
            break
    except Exception:
        time.sleep(1)
else:
    print('Timed out waiting for Postgres')
    raise SystemExit(1)
PY
fi

# Run Alembic migrations
alembic upgrade head || true

# Start the app with uvicorn
echo "Starting uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
