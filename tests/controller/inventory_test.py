from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from model.inventory import Inventory
from model.item import Item
from model.warehouse import Warehouse

TEST_INVENTORY_1 = {
    "name": "",
    "lat": 11.1,
    "long": 22.3,
}


def test_get_all_inventory_return_existing_inventory(client: TestClient, inventory: Inventory):
    response = client.get("/inventory/get_all/")
    assert response.status_code == 200
    assert len(response.json()) == 1

    response_inventory = response.json()[0]
    assert response_inventory['item']['id'] == inventory.item_id
    assert response_inventory['warehouse']['id'] == inventory.warehouse_id


def test_get_all_inventory_return_empty_array_when_no_inventory_exists(client: TestClient):
    response = client.get("/inventory/get_all/")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_update_inventory_returns_new_inserted_row(
        client: TestClient,
        item: Item,
        warehouse: Warehouse):
    data = {
        'item_id': item.id,
        'warehouse_id': warehouse.id,
        'quantity': 200
    }
    response = client.post("/inventory/", json=data)
    assert response.status_code == 200
    assert response.json()['item_id'] == item.id
    assert response.json()['warehouse_id'] == warehouse.id


def test_update_inventory_returns_updated_row(
        client: TestClient,
        inventory: Inventory
):
    data = {
        'item_id': inventory.item_id,
        'warehouse_id': inventory.warehouse_id,
        'quantity': 300
    }
    response = client.post("/inventory/", json=data)
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(inventory)
