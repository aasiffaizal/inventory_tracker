from fastapi import Path, Depends, HTTPException
from sqlmodel import Session, select

from db import get_db_session
from model.item import Item
from service.base_crud import BaseCRUD


async def validate_item_id(
        item_id: int = Path(...),
        db_session: Session = Depends(get_db_session)
) -> Item:
    """Validates the if an item is present with the given id.

    Args:
        item_id: int. The id of the item.
        db_session: Session. The database session used to interact with the DB.

    Returns:
        Item. The item corresponding to the item_id.

    Raises:
          HTTPException. Item does not exist in the DB.
    """
    item: Item = item_crud.get(db_session, item_id)
    if not item or not item.active:
        raise HTTPException(status_code=404, detail='Item does not exist')
    return item


class ItemCRUD(BaseCRUD):
    model = Item

    def get_by_sku(self, db_session: Session, sku: str) -> Item:
        """Fetches item using sku

        Args:
            db_session: Session. The database session used to interact
                with the DB.
            sku: str. The product sku of the item.

        Returns:
            Item. The item having the given product sku.
        """
        statement = select(self.model).where(self.model.sku == sku)
        return db_session.exec(statement).first()


item_crud = ItemCRUD()
