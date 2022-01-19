import enum
from typing import List, TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, Column, Enum, String, SQLModel

from db.base import BaseDBModel

if TYPE_CHECKING:
    from .inventory import Inventory


class Metric(str, enum.Enum):
    grams = 'g'
    meter = 'm'
    piece = 'piece'


class ItemEditableFields(SQLModel):
    name: str = Field(index=True)
    sku: str = Field(sa_column=Column("sku", String, unique=True))
    description: Optional[str] = Field(default=None)
    metric: Metric = Field(sa_column=Column(Enum(Metric)))
    cost: float


class Item(BaseDBModel, ItemEditableFields, table=True):
    item_inventories: List["Inventory"] = Relationship(back_populates='item')
    active: bool | None = Field(default=True)


