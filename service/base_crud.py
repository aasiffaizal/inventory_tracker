from abc import ABCMeta, abstractmethod
from typing import Type, TypeVar

from sqlmodel import Session, select

from db import BaseDBModel

DBModel = TypeVar("DBModel", bound=BaseDBModel)


class BaseCRUD(metaclass=ABCMeta):
    EXCLUDE_LIST = ['id', 'created_at', 'updated_at']

    @property
    @abstractmethod
    def model(self) -> Type[BaseDBModel]:
        pass

    def get(self, db_session: Session, identifier: int) -> DBModel:
        """Gets the row from DB by id field.

        Args:
            db_session: Session. The database session used to interact
                with the DB.
            identifier: int. The id of the row.

        Returns:
            DBModel. The DB row object.
        """
        statement = select(self.model).where(self.model.id == identifier)
        return db_session.exec(statement).first()

    def get_multiple_values(
            self,
            db_session: Session,
            offset: int = 0,
            limit: int = 100
    ) -> list[DBModel]:
        """Gets the multiple rows from the DB.

        Args:
            db_session: Session. The database session used to interact
                with the DB.
            offset: int. The offset from which the rows should be read.
            limit: int. The limit of number of rows during fetch.

        Returns:
            list[DBModel]. The DB rows.
        """
        statement = select(self.model).offset(offset).limit(limit)
        return db_session.exec(statement).all()

    @staticmethod
    def create(db_session: Session, item: BaseDBModel) -> DBModel:
        """Inserts a row in the DB.

        Args:
            db_session: Session. The database session used to interact
                with the DB.
            item: BaseDBModel. The row object that needs to be
                inserted into the DB.

        Returns:
            DBModel. The DB row object that was created.
        """
        db_session.add(item)
        db_session.commit()
        db_session.refresh(item)
        return item

    @staticmethod
    def create_all(db_session: Session, items: list[BaseDBModel]) -> None:
        """Inserts rows into the DB.

        Args:
            db_session: Session. The database session used to interact
                with the DB.
            items: list[BaseDBModel]. The row objects that needs to be
                inserted into the DB.
        """
        for item in items:
            db_session.add(item)
        db_session.commit()

    def update(
            self,
            db_session: Session,
            db_item: BaseDBModel,
            new_item: BaseDBModel
    ) -> DBModel:
        """Updates a row in the DB.

        Args:
            db_session: Session. The database session used to interact
                with the DB.
            db_item: BaseDBModel. The row objects that needs to be
                updated in the DB.
            new_item: BaseDBModel. The object with the updated fields.

        Returns:
            DBModel. The updated row object.
        """
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
        """Deletes a row from the DB.

        Args:
            db_session: Session. The database session used to interact
                with the DB.
            identifier: int. The id of the row
        """
        item = self.get(db_session, identifier)
        db_session.delete(item)
        db_session.commit()
