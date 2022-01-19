from fastapi import Path, Depends, HTTPException
from sqlmodel import Session, select

from db import get_db_session
from model.warehouse import Warehouse
from service.base_crud import BaseCRUD


async def validate_warehouse_id(
        warehouse_id: int = Path(...),
        db_session: Session = Depends(get_db_session)
) -> Warehouse:
    """Validates the if a warehouse is present with the given id.

    Args:
        warehouse_id: int. The id of the warehouse.
        db_session: Session. The database session used to interact with the DB.

    Returns:
        Warehouse. The warehouse corresponding to the warehouse_id.

    Raises:
          HTTPException. Warehouse does not exist in the DB.
    """
    warehouse: Warehouse = warehouse_crud.get(db_session, warehouse_id)
    if not warehouse or not warehouse.active:
        raise HTTPException(status_code=404, detail='Warehouse does not exist')
    return warehouse


class WarehouseCRUD(BaseCRUD):
    model = Warehouse

    def get_by_name(self, db_session: Session, name: str) -> Warehouse:
        """Fetches warehouse by name.

        Args:
            db_session: Session. The database session used to interact
                with the DB.
            name: str. The name of the warehouse.

        Returns:
            Warehouse. The warehouse having the given name.
        """
        statement = select(self.model).where(self.model.name == name)
        return db_session.exec(statement).first()


warehouse_crud = WarehouseCRUD()
