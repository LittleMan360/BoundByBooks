from fastapi import APIRouter, HTTPException

from app.schemas.edition import EditionLookupResponse
from app.services.metadata_service import lookup_isbn

router = APIRouter()


@router.get("/isbn/{isbn}", response_model=EditionLookupResponse)
async def get_book_by_isbn(isbn: str) -> EditionLookupResponse:
    normalized = "".join(character for character in isbn if character.isdigit() or character.upper() == "X")
    if len(normalized) not in (10, 13):
        raise HTTPException(status_code=400, detail="ISBN must contain 10 or 13 characters.")

    edition = await lookup_isbn(normalized)
    if edition is None:
        raise HTTPException(status_code=404, detail="No edition found for that ISBN.")

    return edition
