import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from model.item import Item
from model.warehouse import Warehouse
from model.inventory import Inventory
from main import app
from db import get_db_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_db_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="item")
def item_fixture(session: Session):
    item_data = {
        "name": "aasif125",
        "sku": "AASI125",
        "metric": "m",
        "cost": 1100
    }
    item = Item(**item_data)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@pytest.fixture(name="warehouse")
def warehouse_fixture(session: Session):
    warehouse_data = {
        "name": "Warehouse1",
        "lat": 11.1,
        "long": 22.3,
    }
    warehouse = Warehouse(**warehouse_data)
    session.add(warehouse)
    session.commit()
    session.refresh(warehouse)
    return warehouse


@pytest.fixture(name="inventory")
def inventory_fixture(session: Session, item: Item, warehouse: Warehouse):
    inventory = Inventory()
    inventory.item = item
    inventory.warehouse = warehouse
    inventory.quantity = 20
    session.add(inventory)
    session.commit()
    session.refresh(inventory)
    return inventory
