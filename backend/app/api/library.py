from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.database.session import get_db
from app.models.library import Book, Edition, UserCopy
from app.schemas.library import UserCopyCreate, UserCopyResponse
from app.services.metadata_service import lookup_isbn

router = APIRouter()

# Authentication comes in a later milestone. Keeping this value in one place
# lets the MVP exercise the complete library flow without pretending auth exists.
MVP_USER_ID = "local-demo-user"


def to_response(copy: UserCopy) -> UserCopyResponse:
    edition = copy.edition
    book = edition.book
    return UserCopyResponse(
        id=copy.id,
        isbn=edition.isbn,
        title=book.title,
        authors=[book.primary_author] if book.primary_author else [],
        publisher=edition.publisher,
        publication_date=edition.publication_date,
        cover_url=edition.cover_url,
        condition=copy.condition,
        purchase_price=copy.purchase_price,
        purchase_date=copy.purchase_date,
        estimated_value=copy.estimated_value,
        notes=copy.notes,
    )


@router.get("", response_model=list[UserCopyResponse])
def list_library(db: Session = Depends(get_db)) -> list[UserCopyResponse]:
    statement = (
        select(UserCopy)
        .where(UserCopy.user_id == MVP_USER_ID)
        .options(joinedload(UserCopy.edition).joinedload(Edition.book))
        .order_by(UserCopy.id.desc())
    )
    return [to_response(copy) for copy in db.scalars(statement).all()]


@router.post("", response_model=UserCopyResponse, status_code=201)
async def add_to_library(payload: UserCopyCreate, db: Session = Depends(get_db)) -> UserCopyResponse:
    isbn = "".join(character for character in payload.isbn if character.isdigit() or character.upper() == "X")
    if len(isbn) not in (10, 13):
        raise HTTPException(status_code=400, detail="ISBN must contain 10 or 13 characters.")

    edition = db.scalar(
        select(Edition).where(Edition.isbn == isbn).options(joinedload(Edition.book))
    )

    if edition is None:
        metadata = await lookup_isbn(isbn)
        if metadata is None:
            raise HTTPException(status_code=404, detail="No edition found for that ISBN.")

        primary_author = metadata.authors[0] if metadata.authors else None
        book = Book(title=metadata.title, primary_author=primary_author)
        edition = Edition(
            book=book,
            isbn=metadata.isbn,
            publisher=metadata.publisher,
            publication_date=metadata.publication_date,
            cover_url=metadata.cover_url,
        )
        db.add(edition)
        db.flush()

    copy = UserCopy(
        user_id=MVP_USER_ID,
        edition=edition,
        condition=payload.condition,
        purchase_price=payload.purchase_price,
        purchase_date=payload.purchase_date,
        notes=payload.notes,
    )
    db.add(copy)
    db.commit()
    db.refresh(copy)

    return to_response(copy)
