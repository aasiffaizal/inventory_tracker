from fastapi import Path, Depends, HTTPException

from db import get_db_session
from service.base_crud import BaseCRUD
from model.item import Item
from sqlmodel import Session, select


async def validate_item_id(
        item_id: int = Path(...),
        db_session: Session = Depends(get_db_session)
) -> Item:
    item: Item = item_crud.get(db_session, item_id)
    if not item or not item.active:
        raise HTTPException(status_code=404, detail='Item does not exist')
    return item


class ItemCRUD(BaseCRUD):
    model = Item

    def get_by_sku(self, db_session: Session, sku: str) -> Item:
        statement = select(self.model).where(self.model.sku == sku)
        return db_session.exec(statement).first()


item_crud = ItemCRUD()
