from sqlalchemy import insert
from sqlalchemy.engine import Engine

from src.database import books as books_table


def load_books(books: list[dict[str, object]], engine: Engine) -> int:
    if not books:
        return 0

    stmt = insert(books_table).prefix_with("OR IGNORE")

    try:
        with engine.begin() as conn:
            result = conn.execute(stmt, books)
            return int(result.rowcount or 0)

    except Exception as e:
        print(f"DB insert failed: {e}")
        return 0

    return int(result.rowcount or 0)
