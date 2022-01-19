from fastapi import APIRouter, Depends
from sqlmodel import Session

from db import get_db_session
from model.inventory import InventoryEditableFields, Inventory, InventoryRead
from service.inventory import validate_inventory_fields, inventory_crud

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
)


@router.get('/get_all', response_model=list[InventoryRead])
async def get_inventories(db_session: Session = Depends(get_db_session)):
    """This handler gets all the inventory present in the DB.

    Args:
        db_session: Session. The database session used to interact with the DB.

    Returns:
        list[InventoryRead]. List of inventories stored in the DB.
    """
    return inventory_crud.get_multiple_values(db_session)


@router.post('/', dependencies=[Depends(
    validate_inventory_fields)], response_model=Inventory)
async def update_inventory(
        inventory: InventoryEditableFields,
        db_session: Session = Depends(get_db_session)
):
    """This handler updates the quantity of the item in a warehouse.

    Args:
        inventory: InventoryEditableFields. The inventory object
            that needs to be updated.
        db_session: Session. The database session used to interact with the DB.

    Returns:
        Inventory. The inventory object that was updated.

    Raises:
        HTTPException. The item or warehouse does not exist.
    """
    existing_inventory = inventory_crud.get_by_item_and_warehouse(
        db_session, inventory.item_id, inventory.warehouse_id)
    if existing_inventory:
        result_row = inventory_crud.update(db_session, existing_inventory, inventory)
    else:
        result_row = inventory_crud.create(db_session, Inventory.from_orm(inventory))
    return result_row
