from src.database import create_tables, get_engine
from src.fetcher import fetch_books
from src.loader import load_books
from src.transformer import transform_books


def main() -> None:
    engine = get_engine()
    create_tables(engine)

    raw_books = fetch_books()
    if not raw_books:
        print("No data fetched. Exiting pipeline.")
        return
    transformed_books = transform_books(raw_books)
    inserted_count = load_books(transformed_books, engine)

    print(f"Fetched {len(raw_books)} -> Transformed {len(transformed_books)} -> Inserted {inserted_count}")


if __name__ == "__main__":
    main()
