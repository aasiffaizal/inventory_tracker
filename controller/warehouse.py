from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from db import get_db_session
from model.warehouse import Warehouse, WareHouseEditableFields
from service.warehouse import warehouse_crud, validate_warehouse_id

router = APIRouter(
    prefix="/warehouse",
    tags=["warehouse"],
)


@router.get('/get_all', response_model=list[Warehouse])
async def get_warehouses(db_session: Session = Depends(get_db_session)):
    """This handler gets all the warehouses in the DB.

    Args:
        db_session: Session. The database session used to interact with the DB.

    Returns:
        list[Warehouse]. List of warehouses stored in the DB.
    """
    return warehouse_crud.get_multiple_values(db_session)


@router.post('/', response_model=Warehouse)
async def add_warehouse(
        warehouse: WareHouseEditableFields,
        db_session: Session = Depends(get_db_session)
):
    """This handler adds warehouse to the DB.

    Args:
        warehouse: WareHouseEditableFields. The data of warehouse
            to be added to the DB.
        db_session: Session. The database session used to interact with the DB.

    Returns:
          Warehouse. The warehouse object that was inserted.

    Raises:
          HTTPException. Warehouse already exists in the DB.
    """
    existing_warehouse = warehouse_crud.get_by_name(db_session, warehouse.name)
    if existing_warehouse:
        raise HTTPException(status_code=412, detail='Warehouse already exists.')
    return warehouse_crud.create(db_session, Warehouse(**warehouse.dict()))


@router.put('/{warehouse_id}', response_model=Warehouse)
async def edit_warehouse(
    new_warehouse: WareHouseEditableFields,
    db_warehouse: Warehouse = Depends(validate_warehouse_id),
    db_session: Session = Depends(get_db_session)
):
    """This handler edits warehouse in the DB.

    Args:
        new_warehouse: WareHouseEditableFields. The updated warehouse data.
        db_warehouse: Warehouse. The warehouse object to be updated in the DB.
        db_session: Session. The database session used to interact with the DB.

    Returns:
          Warehouse. The updated warehouse object.

    Raises:
          HTTPException. Warehouse does not exist in the DB.
    """
    return warehouse_crud.update(db_session, db_warehouse, new_warehouse)


@router.delete('/{warehouse_id}')
async def delete_warehouse(
    db_warehouse: Warehouse = Depends(validate_warehouse_id),
    db_session: Session = Depends(get_db_session)
):
    """This handler deletes warehouse from the DB.

    Args:
        db_warehouse: Warehouse. The warehouse object
            to be deleted from the DB.
        db_session: Session. The database session used to interact with the DB.

    Raises:
          HTTPException. Warehouse does not exist in the DB.
    """
    warehouse_crud.delete(db_session, db_warehouse.id)
    return {'message': 'Successfully deleted'}
