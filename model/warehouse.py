from db.base import BaseDBModel
from sqlmodel import Relationship, Field, SQLModel
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .inventory import Inventory


class WareHouseEditableFields(SQLModel):
    name: str
    lat: Optional[float] = Field(default=None)
    long: Optional[float] = Field(default=None)


class Warehouse(BaseDBModel, table=True):
    name: str
    lat: Optional[float] = Field(default=None)
    long: Optional[float] = Field(default=None)
    warehouse_inventories: List["Inventory"] = Relationship(back_populates='warehouse')
    active: Optional[bool] = Field(default=True)
