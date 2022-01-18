from service.inventory import validate_inventory_fields, inventory_crud
from sqlmodel import Session
import pytest
from fastapi import HTTPException
from model.inventory import Inventory, InventoryEditableFields


@pytest.mark.asyncio
async def test_validate_inventory_data_raises_error_for_invalid_data(session: Session):
    inventory = InventoryEditableFields(**{
        'item_id': 1,
        'warehouse_id': 22,
        'quantity': 32
    })
    with pytest.raises(HTTPException):
        await validate_inventory_fields(inventory, session)


@pytest.mark.asyncio
async def test_validate_inventory_raises_no_error_for_valid_entry(session: Session, inventory: Inventory):
    await validate_inventory_fields(InventoryEditableFields.from_orm(inventory), session)


def test_get_by_item_and_warehouse_returns_corresponding_inventory(session: Session, inventory: Inventory):
    row = inventory_crud.get_by_item_and_warehouse(
        session, inventory.item_id, inventory.warehouse_id)
    assert row == inventory


def test_get_by_item_and_warehouse_returns_none_as_no_entry_exists(session: Session):
    row = inventory_crud.get_by_item_and_warehouse(session, 11, 22)
    assert row is None
