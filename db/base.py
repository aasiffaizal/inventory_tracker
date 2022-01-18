import datetime
from typing import Generator, Optional

import inflection
from sqlalchemy.orm import declared_attr
from sqlmodel import Field, Session, SQLModel, create_engine, func, TIMESTAMP, Column
import os

CONFIG = {
    'engine': os.environ.get('ENGINE'),
    'user': os.environ.get('USER'),
    'password': os.environ.get('PASSWORD'),
    'host': os.environ.get('HOST'),
    'db': os.environ.get('DB')
}


engine = create_engine(
    "{engine}://{user}:{password}@{host}/{db}".format(**CONFIG),
    echo=True
)


def get_table_name(name: str) -> str:
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
    """Provide a transactional scope around a series of operations."""
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
