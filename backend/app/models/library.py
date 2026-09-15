from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(500), index=True)
    primary_author: Mapped[str | None] = mapped_column(String(300), nullable=True)

    editions: Mapped[list["Edition"]] = relationship(back_populates="book")


class Edition(Base):
    __tablename__ = "editions"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), index=True)
    isbn: Mapped[str] = mapped_column(String(13), unique=True, index=True)
    publisher: Mapped[str | None] = mapped_column(String(300), nullable=True)
    publication_date: Mapped[str | None] = mapped_column(String(100), nullable=True)
    format: Mapped[str | None] = mapped_column(String(100), nullable=True)
    cover_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    book: Mapped[Book] = relationship(back_populates="editions")
    copies: Mapped[list["UserCopy"]] = relationship(back_populates="edition")


class Shelf(Base):
    __tablename__ = "shelves"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(String(100), index=True)
    name: Mapped[str] = mapped_column(String(150))

    copies: Mapped[list["UserCopy"]] = relationship(back_populates="shelf")


class UserCopy(Base):
    __tablename__ = "user_copies"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(String(100), index=True)
    edition_id: Mapped[int] = mapped_column(ForeignKey("editions.id"), index=True)
    shelf_id: Mapped[int | None] = mapped_column(ForeignKey("shelves.id"), nullable=True)
    position: Mapped[int | None] = mapped_column(nullable=True)
    condition: Mapped[str | None] = mapped_column(String(50), nullable=True)
    purchase_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    purchase_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    estimated_value: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    edition: Mapped[Edition] = relationship(back_populates="copies")
    shelf: Mapped[Shelf | None] = relationship(back_populates="copies")
