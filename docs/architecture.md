# Architecture

## Product boundary

Bound By Books treats three concepts separately:

- **Book** — the abstract work/title, such as a novel by an author.
- **Edition** — a specific published product identified where possible by ISBN, publisher, publication date, format and cover.
- **UserCopy** — the physical item a user owns, including condition, purchase information, shelf position and eventually estimated value.

This separation is foundational for collecting and valuation because two copies of the same title can be different editions with very different attributes and values.

## MVP request flow

```text
Web / Mobile
    |
    v
FastAPI
    |
    +--> PostgreSQL (normalized books, editions, user copies, shelves)
    |
    +--> MetadataService
              |
              +--> metadata provider(s)
    |
    +--> ValuationService (later)
              |
              +--> legitimate market data source(s)
```

## ISBN lookup

The first implementation uses Open Library behind `MetadataService`. Provider responses are normalized into Bound By Books schemas before reaching the rest of the application. This makes it possible to add or replace providers without coupling the UI or domain models to one external API.

The intended lookup path is:

1. Normalize and validate ISBN.
2. Search our `Edition` table.
3. If known, return the stored edition.
4. Otherwise ask metadata provider(s).
5. Normalize and persist the edition.
6. Ask the user to confirm the match.
7. Create a `UserCopy` when the user adds it to their library.

The current v0.1 route implements the provider lookup portion; persistence is the next slice.

## Valuation principle

Valuation is intentionally separate from metadata. A later valuation service should return an estimate/range, source context, and calculation timestamp. It should not present an unsupported price as an exact market value.
