import datetime
import os
from typing import Generator, Optional

import inflection
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, Session, SQLModel, create_engine, func, TIMESTAMP, Column

CONFIG = {
    'engine': os.environ.get('ENGINE'),
    'user': os.environ.get('USER'),
    'password': os.environ.get('PASSWORD'),
    'host': os.environ.get('HOST'),
    'db': os.environ.get('DB')
}


def get_table_name(name: str) -> str:
    """Transforms camel cased table names to snake case.

    Args:
        name: str. The camel cased table name.

    Returns:
        str. The snake cased table name.
    """
    return inflection.underscore(name)


class BaseDBModel(SQLModel):
    @declared_attr
    def __tablename__(cls) -> str:
        return get_table_name(cls.__name__)

    id: Optional[int] = Field(primary_key=True)
    created_at: Optional[datetime.datetime] = Field(
        sa_column=Column(TIMESTAMP, default=func.now()))
    updated_at: Optional[datetime.datetime] = Field(
        sa_column=Column(TIMESTAMP, default=func.now(), onupdate=func.now())
    )


def get_db_session() -> Generator:
    """Transactional scope for DB session around a series of operations."""
    engine = create_engine(
        "{engine}://{user}:{password}@{host}/{db}".format(**CONFIG))
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
