import pytest
from fastapi import HTTPException
from sqlmodel import Session

from model.item import Item
from service.item import validate_item_id, item_crud


@pytest.mark.asyncio
async def test_validate_item_id_raises_error_for_invalid_id(session: Session):
    with pytest.raises(HTTPException):
        await validate_item_id(1, session)


@pytest.mark.asyncio
async def test_validate_item_id_raises_no_error_for_valid_id(session: Session, item: Item):
    validated_item = await validate_item_id(item.id, session)
    assert validated_item == item


def test_get_by_sku_returns_corresponding_item(session: Session, item: Item):
    row = item_crud.get_by_sku(session, item.sku)
    assert row == item


def test_get_by_sky_returns_none_no_entry_with_given_sku(session: Session):
    row = item_crud.get_by_sku(session, 'TEST')
    assert row is None
