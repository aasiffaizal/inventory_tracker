from fastapi import Body, Depends
from sqlmodel import Session, select

from db import get_db_session
from model.inventory import InventoryEditableFields, Inventory
from service.base_crud import BaseCRUD
from service.item import validate_item_id
from service.warehouse import validate_warehouse_id


async def validate_inventory_fields(
        inventory: InventoryEditableFields = Body(...),
        db_session: Session = Depends(get_db_session)
) -> None:
    """Validates the inventory fields in the inventory object.

    Args:
        inventory: InventoryEditableFields. The inventory object
            with editable fields.
        db_session: Session. The database session used to interact with the DB.

    Raises:
          HTTPException. Item or warehouse does not exist in the DB.
    """
    await validate_warehouse_id(inventory.warehouse_id, db_session)
    await validate_item_id(inventory.item_id, db_session)


class InventoryCRUD(BaseCRUD):
    model = Inventory

    def get_by_item_and_warehouse(
            self,
            db_session: Session,
            item_id: int,
            warehouse_id: int
    ) -> Inventory:
        """Fetches inventory using item_id and warehouse_id

        Args:
            db_session: Session. The database session used to interact
                with the DB.
            item_id: int. The id of the item.
            warehouse_id: int. The id of the warehouse.

        Returns:
            Inventory. The inventory mapped to the item and the warehouse.
        """
        statement = (select(self.model)
                     .where(self.model.item_id == item_id)
                     .where(self.model.warehouse_id == warehouse_id))
        return db_session.exec(statement).first()


inventory_crud = InventoryCRUD()
