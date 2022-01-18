from fastapi import APIRouter, Depends, HTTPException
from service.warehouse import warehouse_crud, validate_warehouse_id
from db import get_db_session
from model.warehouse import Warehouse, WareHouseEditableFields
from sqlmodel import Session


router = APIRouter(
    prefix="/warehouse",
    tags=["warehouse"],
)


@router.get('/get_all', response_model=list[Warehouse])
async def get_warehouses(db_session: Session = Depends(get_db_session)):
    return warehouse_crud.get_multiple_values(db_session)


@router.post('/', response_model=Warehouse)
async def add_warehouse(warehouse: WareHouseEditableFields, db_session: Session = Depends(get_db_session)):
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
    return warehouse_crud.update(db_session, db_warehouse, new_warehouse)


@router.delete('/{warehouse_id}')
async def delete_warehouse(
    db_warehouse: Warehouse = Depends(validate_warehouse_id),
    db_session: Session = Depends(get_db_session)
):
    warehouse_crud.delete(db_session, db_warehouse.id)
    return {'message': 'Successfully deleted'}
