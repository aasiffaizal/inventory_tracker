from fastapi.testclient import TestClient
from sqlmodel import Session, select
from model.warehouse import Warehouse
from fastapi.encoders import jsonable_encoder

TEST_WAREHOUSE = {
    "name": "Warehouse2",
    "lat": 11.1,
    "long": 22.3,
}


def test_get_warehouses_returns_no_warehouse_when_table_is_empty(client: TestClient):
    response = client.get("/warehouse/get_all/")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_get_warehouses_returns_existing_warehouses(
        client: TestClient,
        session: Session,
        warehouse: Warehouse
):
    warehouse_2 = Warehouse(**TEST_WAREHOUSE)
    session.add(warehouse_2)
    session.commit()
    session.refresh(warehouse_2)

    warehouse_ids = [warehouse.id, warehouse_2.id]
    response = client.get("/warehouse/get_all/")
    response_ids = list(map(lambda _item: _item['id'], response.json()))
    assert response.status_code == 200
    assert response_ids == warehouse_ids


def test_add_warehouse_returns_inserted_row(client: TestClient, session: Session):
    response = client.post("/warehouse/", json=TEST_WAREHOUSE)
    assert response.status_code == 200

    warehouse = Warehouse(**response.json())
    row = session.exec(
        select(Warehouse).where(Warehouse.id == warehouse.id)).one()

    assert row == warehouse


def test_add_warehouse_returns_error_for_invalid_body(
        client: TestClient, session: Session
):
    data = {
        "a": "b"
    }
    response = client.post("/warehouse/", json=data)
    assert response.status_code == 422


def test_add_warehouse_returns_error_existing_warehouse(
        client: TestClient,
        session: Session,
        warehouse: Warehouse
):

    response = client.post("/warehouse/", json=jsonable_encoder(warehouse))
    assert response.status_code == 412


def test_edit_warehouse_returns_error_for_invalid_warehouse_id(
        client: TestClient, session: Session
):
    response = client.put("/warehouse/1", json=TEST_WAREHOUSE)
    assert response.status_code == 404


def test_edit_warehouse_returns_updated_warehouse(
        client: TestClient,
        session: Session,
        warehouse: Warehouse
):
    warehouse.lat = 22.2
    response = client.put("/warehouse/1", data=warehouse.json())
    assert response.status_code == 200
    assert response.json()['lat'] == warehouse.lat


def test_delete_warehouse_returns_error_for_invalid_warehouse_id(
        client: TestClient, session: Session
):
    response = client.delete("/warehouse/1")
    assert response.status_code == 404


def test_delete_item_returns_success(
        client: TestClient,
        session: Session,
        warehouse: Warehouse
):
    response = client.delete("/warehouse/1")
    assert response.status_code == 200
