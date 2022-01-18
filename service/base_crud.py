from abc import ABCMeta, abstractmethod
from sqlmodel import Session, select
from typing import Type, TypeVar
from db import BaseDBModel

DBModel = TypeVar("DBModel", bound=BaseDBModel)


class BaseCRUD(metaclass=ABCMeta):
    EXCLUDE_LIST = ['id', 'created_at', 'updated_at']

    @property
    @abstractmethod
    def model(self) -> Type[BaseDBModel]:
        pass

    def get(self, db_session: Session, identifier: int) -> DBModel:
        statement = select(self.model).where(self.model.id == identifier)
        return db_session.exec(statement).first()

    def get_multiple_values(
            self, db_session: Session, offset: int = 0, limit: int = 100) -> list[DBModel]:
        statement = select(self.model).offset(offset).limit(limit)
        return db_session.exec(statement).all()

    @staticmethod
    def create(db_session: Session, item: BaseDBModel) -> DBModel:
        db_session.add(item)
        db_session.commit()
        db_session.refresh(item)
        return item

    @staticmethod
    def create_all(db_session: Session, items: list[BaseDBModel]) -> None:
        for item in items:
            db_session.add(item)
        db_session.commit()

    def update(
            self,
            db_session: Session,
            db_item: BaseDBModel,
            new_item: BaseDBModel
    ) -> DBModel:
        update_data = new_item.dict(exclude_unset=True)
        for key, value in update_data.items():
            if key in self.EXCLUDE_LIST:
                continue
            setattr(db_item, key, value)
        db_session.add(db_item)
        db_session.commit()
        db_session.refresh(db_item)
        return db_item

    def delete(self, db_session: Session, identifier: int) -> None:
        item = self.get(db_session, identifier)
        db_session.delete(item)
        db_session.commit()
