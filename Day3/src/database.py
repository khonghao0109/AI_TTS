from pathlib import Path

from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine
from sqlalchemy.engine import Engine


def get_engine() -> Engine:
    db_path = Path(__file__).resolve().parent.parent / "data" / "books.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return create_engine(f"sqlite:///{db_path}", future=True)


metadata = MetaData()


books = Table(
    "books",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255), nullable=False),
    Column("author", String(255), nullable=True),
    Column("publish_year", Integer, index=True, nullable=True),
    Column("work_key", String(255), unique=True, nullable=False),
)


def create_tables(engine: Engine) -> None:
    metadata.create_all(engine)
