from fastapi import Body, Depends

from db import get_db_session
from service.base_crud import BaseCRUD
from service.warehouse import validate_warehouse_id
from service.item import validate_item_id
from model.inventory import InventoryEditableFields, Inventory
from sqlmodel import Session, select


async def validate_inventory_fields(
        inventory: InventoryEditableFields = Body(...),
        db_session: Session = Depends(get_db_session)
) -> None:
    await validate_warehouse_id(inventory.warehouse_id, db_session)
    await validate_item_id(inventory.item_id, db_session)


class InventoryCRUD(BaseCRUD):
    model = Inventory

    def get_by_item_and_warehouse(
            self,
            db_session: Session,
            item_id, warehouse_id
    ) -> Inventory:
        statement = (select(self.model)
                     .where(self.model.item_id == item_id)
                     .where(self.model.warehouse_id == warehouse_id))
        return db_session.exec(statement).first()


inventory_crud = InventoryCRUD()
