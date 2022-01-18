from db.base import BaseDBModel
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from model.item import Item
from model.warehouse import Warehouse


class InventoryEditableFields(SQLModel):
    item_id: int = Field(foreign_key="item.id")
    warehouse_id: int = Field(foreign_key="warehouse.id")
    quantity: int


class Inventory(BaseDBModel, InventoryEditableFields, table=True):
    item: Optional[Item] = Relationship(back_populates="item_inventories")
    warehouse: Optional[Warehouse] = Relationship(back_populates="warehouse_inventories")


class InventoryRead(SQLModel):
    quantity: int
    item: Optional[Item] = None
    warehouse: Optional[Warehouse] = None
