import httpx

from app.schemas.edition import EditionLookupResponse

OPEN_LIBRARY_BOOKS_URL = "https://openlibrary.org/api/books"


async def lookup_isbn(isbn: str) -> EditionLookupResponse | None:
    """Look up an ISBN through Open Library for the MVP.

    Provider-specific data is normalized here so API routes and future database
    code do not depend on Open Library's response format.
    """
    params = {
        "bibkeys": f"ISBN:{isbn}",
        "format": "json",
        "jscmd": "data",
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(OPEN_LIBRARY_BOOKS_URL, params=params)
        response.raise_for_status()

    data = response.json().get(f"ISBN:{isbn}")
    if not data:
        return None

    cover = data.get("cover", {})
    publishers = data.get("publishers", [])

    return EditionLookupResponse(
        isbn=isbn,
        title=data.get("title", "Unknown title"),
        authors=[author.get("name", "Unknown") for author in data.get("authors", [])],
        publisher=publishers[0].get("name") if publishers else None,
        publication_date=data.get("publish_date"),
        page_count=data.get("number_of_pages"),
        cover_url=cover.get("large") or cover.get("medium") or cover.get("small"),
        source="open_library",
    )
