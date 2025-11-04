# Karkinos Oncology Intelligence

Karkinos is a monorepo housing the web experience, API, database infrastructure, and ingestion
utilities for an oncology knowledge platform.

## Repository Structure

- `web/` – Next.js 14 + TypeScript frontend styled with Tailwind CSS.
- `api/` – FastAPI service managed via Poetry with modular routers.
- `db/` – Docker Compose configuration for Postgres with pgvector and the database schema.
- `ingestion/` – Python tooling to ingest PDFs, compute embeddings, and upsert vectors.

## Prerequisites

- Docker and Docker Compose
- Node.js 18+
- Python 3.11+
- Poetry (for API dependencies)

## Running the Stack Locally

### 1. Start Postgres + pgvector

```bash
cd db
docker compose up -d
```

This seeds the database schema defined in `db/schema.sql`.

### 2. Run the API

```bash
cd api
poetry install
poetry run uvicorn app.main:app --reload
```

The API is served on `http://127.0.0.1:8000`.

### 3. Run the Web App

```bash
cd web
npm install
npm run dev
```

The Next.js application is served on `http://127.0.0.1:3000`.

### 4. (Optional) Run Ingestion Utilities

Install the ingestion requirements and execute your ingestion workflows pointing to the running
Postgres instance.

```bash
cd ingestion
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m ingestion.ingest  # implement CLI entrypoints as needed
```

## Continuous Integration

GitHub Actions workflow (`.github/workflows/ci.yml`) installs dependencies and runs tests for both
web and API packages to ensure the scaffold remains healthy.
