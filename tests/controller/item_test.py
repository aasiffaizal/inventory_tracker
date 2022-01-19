from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from model.item import Item

TEST_ITEM = {
    "name": "aasif126",
    "sku": "AASI126",
    "metric": "m",
    "cost": 2200
}


def test_get_items_returns_no_item_when_table_is_empty(client: TestClient):
    response = client.get("/item/get_all/")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_get_items_returns_existing_items(client: TestClient, session: Session, item: Item):
    item_2 = Item(**TEST_ITEM)
    session.add(item_2)
    session.commit()
    session.refresh(item_2)

    item_ids = [item.id, item_2.id]
    response = client.get("/item/get_all/")
    response_ids = list(map(lambda _item: _item['id'], response.json()))
    assert response.status_code == 200
    assert item_ids == response_ids


def test_get_items_csv_returns_csv(client: TestClient, session: Session, item: Item):
    response = client.get("/item/get_all.csv")
    assert response.status_code == 200


def test_get_items_csv_raises_error_for_when_no_items_present(
        client: TestClient, session: Session):
    response = client.get("/item/get_all.csv")
    assert response.status_code == 404


def test_add_item_returns_inserted_row(client: TestClient, session: Session):
    response = client.post("/item/", json=TEST_ITEM)
    assert response.status_code == 200

    item = Item(**response.json())
    row = session.exec(
        select(Item).where(Item.id == item.id)).one()

    assert row == item


def test_add_item_returns_error_for_invalid_body(
        client: TestClient, session: Session
):
    data = {
        "name": "aasif125",
        "sku": "AASI125",
    }
    response = client.post("/item/", json=data)
    assert response.status_code == 422


def test_add_item_returns_error_existing_item(
        client: TestClient,
        session: Session,
        item: Item
):

    response = client.post("/item/", json=jsonable_encoder(item))
    assert response.status_code == 412


def test_edit_item_returns_error_for_invalid_item_id(
        client: TestClient, session: Session
):
    response = client.put("/item/1", json=TEST_ITEM)
    assert response.status_code == 404


def test_edit_item_returns_updated_item(
        client: TestClient, session: Session,
        item: Item
):
    item.cost = 2200
    response = client.put("/item/1", data=item.json())
    assert response.status_code == 200
    assert response.json()['cost'] == item.cost


def test_delete_item_returns_error_for_invalid_item_id(
        client: TestClient, session: Session
):
    response = client.delete("/item/1")
    assert response.status_code == 404


def test_delete_item_returns_success(
        client: TestClient, session: Session,
        item: Item
):
    response = client.delete("/item/1")
    assert response.status_code == 200
