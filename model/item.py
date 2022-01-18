import enum
from typing import List, TYPE_CHECKING
from db.base import BaseDBModel
from sqlmodel import Field, Relationship, Column, Enum, String, SQLModel

if TYPE_CHECKING:
    from .inventory import Inventory


class Metric(enum.Enum):
    grams = 'g'
    meter = 'm'
    piece = 'piece'


class ItemEditableFields(SQLModel):
    name: str = Field(index=True)
    sku: str = Field(sa_column=Column("sku", String, unique=True))
    description: str | None = Field(default=None)
    metric: Metric = Field(sa_column=Column(Enum(Metric)))
    cost: int


class Item(BaseDBModel, table=True):
    name: str = Field(index=True)
    sku: str = Field(sa_column=Column("sku", String, unique=True))
    description: str | None = Field(default=None)
    metric: Metric = Field(sa_column=Column(Enum(Metric)))
    cost: int
    item_inventories: List["Inventory"] = Relationship(back_populates='item')
    active: bool | None = Field(default=True)


