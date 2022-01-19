from typing import List, Optional, TYPE_CHECKING

from sqlmodel import Relationship, Field, SQLModel, String, Column

from db.base import BaseDBModel

if TYPE_CHECKING:
    from .inventory import Inventory


class WareHouseEditableFields(SQLModel):
    name: str = Field(sa_column=Column("name", String, unique=True))
    lat: Optional[float] = Field(default=None)
    long: Optional[float] = Field(default=None)


class Warehouse(BaseDBModel, WareHouseEditableFields, table=True):
    warehouse_inventories: List["Inventory"] = Relationship(back_populates='warehouse')
    active: Optional[bool] = Field(default=True)
