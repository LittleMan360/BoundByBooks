from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class UserCopyCreate(BaseModel):
    isbn: str
    condition: str | None = None
    purchase_price: Decimal | None = Field(default=None, ge=0)
    purchase_date: date | None = None
    notes: str | None = None


class UserCopyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    isbn: str
    title: str
    authors: list[str]
    publisher: str | None = None
    publication_date: str | None = None
    cover_url: str | None = None
    condition: str | None = None
    purchase_price: Decimal | None = None
    purchase_date: date | None = None
    estimated_value: Decimal | None = None
    notes: str | None = None
