from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlmodel import Session

from constants import ITEM_CSV_HEADERS
from db import get_db_session
from model.item import Item, ItemEditableFields
from service.item import item_crud, validate_item_id
from utils import get_csv_from_orm

router = APIRouter(
    prefix="/item",
    tags=["item"],
)


@router.get('/get_all', response_model=list[Item])
async def get_items(db_session: Session = Depends(get_db_session)):
    """This handler gets all the items in the DB.

    Args:
        db_session: Session. The database session used to interact with the DB.

    Returns:
        list[Item]. List of items stored in the DB.
    """
    return item_crud.get_multiple_values(db_session)


@router.get('/get_all.csv')
async def get_items_csv(db_session: Session = Depends(get_db_session)):
    """This handler fetches the csv containing all the items in the DB.

    Args:
        db_session: Session. The database session used to interact with the DB.

    Returns:
        StreamingResponse. CSV containing all the items.

    Raises:
         HTTPException. There are no items in the DB.
    """
    items = item_crud.get_multiple_values(db_session)
    if not items:
        raise HTTPException(status_code=404, detail='No Items present')
    csv_string = get_csv_from_orm(items, headers=ITEM_CSV_HEADERS)
    response = StreamingResponse(csv_string, media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=items.csv"
    return response


@router.post('/', response_model=Item)
async def add_item(
        item: ItemEditableFields,
        db_session: Session = Depends(get_db_session)
):
    """This handler adds item to the DB.

    Args:
        item: ItemEditableFields. The data of item to be added to the DB.
        db_session: Session. The database session used to interact with the DB.

    Returns:
          Item. The item object that was inserted.

    Raises:
          HTTPException. Item already exists in the DB.
    """
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
    """This handler edits item in the DB.

    Args:
        new_item: ItemEditableFields. The updated item data.
        db_item: Item. The item object to be updated in the DB.
        db_session: Session. The database session used to interact with the DB.

    Returns:
          Item. The updated item object.

    Raises:
          HTTPException. Item does not exist in the DB.
    """
    return item_crud.update(db_session, db_item, new_item)


@router.delete('/{item_id}')
async def delete_item(
    db_item: Item = Depends(validate_item_id),
    db_session: Session = Depends(get_db_session)
):
    """This handler deletes item from the DB.

    Args:
        db_item: Item. The item object to be deleted from the DB.
        db_session: Session. The database session used to interact with the DB.

    Raises:
          HTTPException. Item does not exist in the DB.
    """
    item_crud.delete(db_session, db_item.id)
    return {'message': 'Successfully deleted'}
