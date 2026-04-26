# Kenya Locations API

This project uses FastAPI with PostgreSQL models and a seed script for `locations.json`.

## What is included

- `app/main.py`: FastAPI app setup
- `app/models.py`: SQLAlchemy model for searchable locations
- `app/routers.py`: API endpoints for listing, filtering, and reading locations
- `scripts/seed_locations.py`: imports `locations.json` into PostgreSQL
- `requirements.txt`: Python dependencies

## Local setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and set `DATABASE_URL`.
4. Make sure PostgreSQL is running and the `kenya_locations` database exists.

Example:

```bash
DATABASE_URL=postgresql+psycopg://YOUR_USER:YOUR_PASSWORD@localhost:5432/kenya_locations
```

On platforms like Render, the provided connection string is often `postgresql://...` (or sometimes `postgres://...`). This app now rewrites those to `postgresql+psycopg://...` automatically so it uses the installed Psycopg 3 driver instead of looking for `psycopg2`.

If `DATABASE_URL` is missing or empty, the app will fail at startup with a clear error instead of using a fallback value.
The committed `docker-compose.yml` is for local development only and uses local-only defaults for PostgreSQL. Do not reuse those credentials in production; keep your real deployment database URL in the environment settings of whatever platform hosts your API instead of committing it to the repository.
5. Seed the data:

```bash
python -m scripts.seed_locations
```

6. Start the API:

```bash
uvicorn main:app --reload
```

## API endpoints

- `GET /health`
- `GET /locations`
- `GET /locations/{id}`
- `GET /filters/categories`
- `GET /filters/counties`
- `GET /filters/towns`
- `GET /filters/types`

## Example filters

- `GET /locations?collection=shopping_malls`
- `GET /locations?county=Nairobi`
- `GET /locations?search=Karen`
- `GET /locations?collection=universities&type=Private%20University`
- `GET /locations?limit=10&offset=10`
