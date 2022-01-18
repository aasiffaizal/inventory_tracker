from fastapi import Path, Depends, HTTPException

from db import get_db_session
from service.base_crud import BaseCRUD
from model.warehouse import Warehouse
from sqlmodel import Session, select


async def validate_warehouse_id(
        warehouse_id: int = Path(...),
        db_session: Session = Depends(get_db_session)
) -> Warehouse:
    warehouse: Warehouse = warehouse_crud.get(db_session, warehouse_id)
    if not warehouse or not warehouse.active:
        raise HTTPException(status_code=404, detail='Warehouse does not exist')
    return warehouse


class WarehouseCRUD(BaseCRUD):
    model = Warehouse

    def get_by_name(self, db_session: Session, name: str) -> Warehouse:
        statement = select(self.model).where(self.model.name == name)
        return db_session.exec(statement).first()


warehouse_crud = WarehouseCRUD()
