from service.warehouse import validate_warehouse_id, warehouse_crud
from sqlmodel import Session
import pytest
from fastapi import HTTPException
from model.warehouse import Warehouse


@pytest.mark.asyncio
async def test_validate_warehouse_id_raises_error_for_invalid_id(session: Session):
    with pytest.raises(HTTPException):
        await validate_warehouse_id(1, session)


@pytest.mark.asyncio
async def test_validate_warehouse_id_raises_no_error_for_valid_id(session: Session, warehouse: Warehouse):
    validated_warehouse = await validate_warehouse_id(warehouse.id, session)
    assert validated_warehouse == warehouse


def test_get_by_name_returns_corresponding_item(session: Session, warehouse: Warehouse):
    row = warehouse_crud.get_by_name(session, warehouse.name)
    assert row == warehouse


def test_get_by_name_returns_none_no_entry_with_given_name(session: Session):
    row = warehouse_crud.get_by_name(session, 'TEST')
    assert row is None
