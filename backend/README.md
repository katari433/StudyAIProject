## Development

Instructions to run locally using the virtualenv and uvicorn.

Docker development
------------------
You can run the backend and Postgres via Docker Compose. The backend image will run Alembic migrations on startup.

1. Build and start services:

```bash
docker-compose up --build
```

2. The backend will be available at `http://localhost:8000` and Postgres on `localhost:5432`.

Notes:
- The `DATABASE_URL` used inside the compose file is `postgresql://studyai_user:studyai_password_change_me@postgres:5432/studyai_db`.
- If you need to re-run migrations manually inside the container:

```bash
docker-compose exec backend alembic upgrade head
```

