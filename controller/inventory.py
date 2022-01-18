from fastapi import APIRouter, Depends
from service.inventory import validate_inventory_fields, inventory_crud
from db import get_db_session
from model.inventory import InventoryEditableFields, Inventory, InventoryRead
from sqlmodel import Session


router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
)


@router.get('/get_all', response_model=list[InventoryRead])
async def get_inventory(db_session: Session = Depends(get_db_session)):
    return inventory_crud.get_multiple_values(db_session)


@router.post('/', dependencies=[Depends(validate_inventory_fields)])
async def update_inventory(
        inventory: InventoryEditableFields,
        db_session: Session = Depends(get_db_session)
):
    existing_inventory = inventory_crud.get_by_item_and_warehouse(
        db_session, inventory.item_id, inventory.warehouse_id)
    if existing_inventory:
        result_row = inventory_crud.update(db_session, existing_inventory, inventory)
    else:
        result_row = inventory_crud.create(db_session, Inventory.from_orm(inventory))
    return result_row
