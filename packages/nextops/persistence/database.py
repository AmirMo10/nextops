"""PostgreSQL engine and transaction factory construction."""

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


def create_database_engine(database_url: str) -> Engine:
    """Create a pooled PostgreSQL engine and reject compatibility substitutions."""

    if not database_url.startswith("postgresql+psycopg://"):
        raise ValueError("NextOps authoritative state requires postgresql+psycopg")
    return create_engine(database_url, pool_pre_ping=True)


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Create sessions whose objects remain usable after a successful commit."""

    return sessionmaker(bind=engine, expire_on_commit=False)
