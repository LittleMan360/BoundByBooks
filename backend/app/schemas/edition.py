from pydantic import BaseModel, Field


class EditionLookupResponse(BaseModel):
    isbn: str
    title: str
    authors: list[str] = Field(default_factory=list)
    publisher: str | None = None
    publication_date: str | None = None
    page_count: int | None = None
    cover_url: str | None = None
    source: str
