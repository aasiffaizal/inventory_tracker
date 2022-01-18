from db import BaseDBModel
from service.base_crud import BaseCRUD
from sqlmodel import Session, select


class TestTable(BaseDBModel, table=True):
    test_str: str
    test_int: int


TEST_ROW_DATA1 = {'test_str': 'str1', 'test_int': 1}
TEST_ROW_DATA2 = {'test_str': 'str2', 'test_int': 2}


class TestCRUD(BaseCRUD):
    model = TestTable


test_crud = TestCRUD()


def test_get_returns_none_for_not_existing_rows(session: Session):
    row = TestTable(**TEST_ROW_DATA1)
    result_row = test_crud.get(session, row.id)
    assert result_row is None


def test_get_returns_existing_row(session: Session):
    row = TestTable(**TEST_ROW_DATA1)
    session.add(row)
    session.commit()
    result_row: TestTable = test_crud.get(session, row.id)
    assert row == result_row


def test_get_multiple_values_returns_empty_array_for_not_existing_rows(session: Session):
    result_arr = test_crud.get_multiple_values(session)
    assert len(result_arr) == 0


def create_and_return_multiple_rows(db_session: Session):
    row1 = TestTable(**TEST_ROW_DATA1)
    row2 = TestTable(**TEST_ROW_DATA2)

    db_session.add(row1)
    db_session.add(row2)

    db_session.commit()

    return [row1, row2]


def test_get_multiple_values_returns_existing_rows(session: Session):
    rows = create_and_return_multiple_rows(session)
    result_arr = test_crud.get_multiple_values(session)
    assert result_arr == rows


def test_get_multiple_values_returns_limited_rows(session: Session):
    rows = create_and_return_multiple_rows(session)
    result_arr = test_crud.get_multiple_values(session, limit=1)
    assert result_arr == [rows[0]]


def test_get_multiple_values_returns_offset_rows(session: Session):
    rows = create_and_return_multiple_rows(session)
    result_arr = test_crud.get_multiple_values(session, offset=1)
    assert result_arr == [rows[1]]


def test_create_row_returns_inserted_row(session: Session):
    row = TestTable(**TEST_ROW_DATA1)
    inserted_row: TestTable = test_crud.create(session, row)
    assert inserted_row == row


def test_create_all_does_not_throw_errors(session: Session):
    rows = [TestTable(**TEST_ROW_DATA1), TestTable(**TEST_ROW_DATA2)]
    test_crud.create_all(session, rows)

    inserted_rows = session.exec(select(TestTable)).all()
    assert inserted_rows == rows


def test_update_returns_updated_row(session: Session):
    row = TestTable(**TEST_ROW_DATA1)
    session.add(row)
    session.commit()

    new_item = TestTable.from_orm(row)
    new_item.test_int = 10
    updated_row: TestTable = test_crud.update(session, row, new_item)
    assert new_item.test_int == updated_row.test_int


def test_delete_row_does_not_throw_error(session: Session):
    row = TestTable(**TEST_ROW_DATA1)
    session.add(row)
    session.commit()

    test_crud.delete(session, row.id)

    inserted_row = session.exec(
        select(TestTable).where(TestTable.id == row.id)).first()

    assert inserted_row is None


def test_model_attribute_returns_test_model():
    assert test_crud.model == TestTable


def test_model_in_base_crud_returns_none_when_not_implemented():
    BaseCRUD.__abstractmethods__ = set()

    class MockCRUD(BaseCRUD):
        string: str

    mock_crud = MockCRUD()
    assert mock_crud.model is None
