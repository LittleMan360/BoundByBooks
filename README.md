# Bound By Books

A digital home for your physical book collection.

Bound By Books is an edition-aware collection manager for book lovers and collectors. The MVP focuses on identifying a specific physical edition by ISBN, saving a user's copy, organizing copies on virtual shelves, and eventually estimating collection value.

## MVP roadmap

1. ISBN lookup and edition identification
2. Personal library management
3. Virtual shelves and ordering
4. Barcode scanning
5. Market-value estimates and price history
6. Collection statistics and wishlists
7. Mobile application using the same API

## Architecture

- `web/` — Next.js + TypeScript frontend
- `backend/` — FastAPI + Python API
- PostgreSQL — persistent application data
- `docs/` — architecture and product documentation

The domain model deliberately separates a `Book` (the work), an `Edition` (a published version), and a `UserCopy` (the user's physical item).

## Local development

### Web

```bash
cd web
npm install
npm run dev
```

The web app runs at `http://localhost:3000`.

### API

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`; interactive API documentation is available at `/docs`.

### Database

```bash
docker compose up -d db
```

Copy `.env.example` to `.env` before adding secrets. Never commit `.env`.

## First product slice

`ISBN -> exact edition -> copy details -> add to library`
