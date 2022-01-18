from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from service.item import item_crud, validate_item_id
from db import get_db_session
from model.item import Item, ItemEditableFields
from sqlmodel import Session
from utils import get_csv_from_orm


router = APIRouter(
    prefix="/item",
    tags=["item"],
)


@router.get('/get_all', response_model=list[Item])
async def get_items(db_session: Session = Depends(get_db_session)):
    return item_crud.get_multiple_values(db_session)


@router.get('/get_all.csv')
async def get_items_csv(db_session: Session = Depends(get_db_session)):
    items = item_crud.get_multiple_values(db_session)
    if not items:
        raise HTTPException(status_code=404, detail='No Items present')
    csv_string = get_csv_from_orm(items)
    return PlainTextResponse(csv_string.read(), media_type="text/csv")


@router.post('/', response_model=Item)
async def add_item(item: ItemEditableFields, db_session: Session = Depends(get_db_session)):
    existing_item = item_crud.get_by_sku(db_session, item.sku)
    if existing_item:
        raise HTTPException(status_code=412, detail='Item already exists.')
    return item_crud.create(db_session, Item(**item.dict()))


@router.put('/{item_id}', response_model=Item)
async def edit_item(
    new_item: ItemEditableFields,
    db_item: Item = Depends(validate_item_id),
    db_session: Session = Depends(get_db_session)
):
    return item_crud.update(db_session, db_item, new_item)


@router.delete('/{item_id}')
async def delete_item(
    db_item: Item = Depends(validate_item_id),
    db_session: Session = Depends(get_db_session)
):
    item_crud.delete(db_session, db_item.id)
    return {'message': 'Successfully deleted'}
