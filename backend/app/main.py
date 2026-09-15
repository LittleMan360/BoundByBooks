from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.books import router as books_router
from app.api.library import router as library_router
from app.config import settings
from app.database.base import Base
from app.database.session import engine
# Import models so SQLAlchemy registers tables before create_all runs.
from app.models import library as library_models  # noqa: F401

app = FastAPI(
    title="Bound By Books API",
    version="0.2.0",
    description="API for edition-aware physical book collection management.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books_router, prefix="/api/books", tags=["books"])
app.include_router(library_router, prefix="/api/library", tags=["library"])


@app.on_event("startup")
def create_database_tables() -> None:
    # Convenient for the early MVP. Replace with Alembic migrations before production.
    Base.metadata.create_all(bind=engine)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "bound-by-books-api"}
