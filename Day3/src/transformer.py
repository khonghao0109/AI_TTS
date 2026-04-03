from typing import Any


def _normalize_author(author_name: Any) -> str | None:
    if author_name is None:
        return None
    if isinstance(author_name, list):
        parts = [str(item).strip() for item in author_name if item is not None and str(item).strip()]
        return ", ".join(parts) if parts else None
    if isinstance(author_name, str):
        value = author_name.strip()
        return value or None
    return None


def _normalize_publish_year(raw_year: Any) -> int | None:
    if raw_year is None:
        return None
    if isinstance(raw_year, int):
        return raw_year
    if isinstance(raw_year, list):
        for item in raw_year:
            if isinstance(item, int):
                return item
        return None
    return None


def transform_book(raw: dict[str, Any]) -> dict[str, object] | None:
    title = raw.get("title")
    if not isinstance(title, str) or not title.strip():
        return None

    work_key = raw.get("key")
    if not isinstance(work_key, str) or not work_key.strip():
        return None

    author = _normalize_author(raw.get("author_name"))
    publish_year = _normalize_publish_year(raw.get("first_publish_year"))

    return {
        "title": title.strip(),
        "author": author,
        "publish_year": publish_year,
        "work_key": work_key.strip(),
    }


def transform_books(raw_books: list[dict[str, Any]]) -> list[dict[str, object]]:
    transformed: list[dict[str, object]] = []

    for raw_book in raw_books:
        book = transform_book(raw_book)
        if book is not None:
            transformed.append(book)

    return transformed
