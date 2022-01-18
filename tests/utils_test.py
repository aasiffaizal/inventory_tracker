import csv

from utils import get_csv_from_orm
from sqlmodel import SQLModel
from fastapi.encoders import jsonable_encoder


def test_get_csv_from_orm_returns_string():
    class MockModel(SQLModel):
        head1: str
        head2: str

    mock_item = MockModel(**{
        'head1': '1',
        'head2': '2'
    })
    string = get_csv_from_orm([mock_item])
    reader = csv.DictReader(string)
    rows = [row for row in reader]
    assert jsonable_encoder(mock_item) == rows.pop()
