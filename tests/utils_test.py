import csv

from fastapi.encoders import jsonable_encoder
from sqlmodel import SQLModel

from utils import get_csv_from_orm


class MockModel(SQLModel):
    head1: str
    head2: str


mock_item = MockModel(**{
    'head1': '1',
    'head2': '2'
})


def test_get_csv_from_orm_returns_string():
    string = get_csv_from_orm([mock_item])
    reader = csv.DictReader(string)
    rows = [row for row in reader]
    assert jsonable_encoder(mock_item) == rows.pop()


def test_get_csv_from_orm_with_headers_returns_string():
    string = get_csv_from_orm([mock_item], headers=mock_item.dict().keys())
    reader = csv.DictReader(string)
    rows = [row for row in reader]
    assert jsonable_encoder(mock_item) == rows.pop()
