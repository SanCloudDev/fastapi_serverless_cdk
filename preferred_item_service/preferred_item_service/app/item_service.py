from fastapi import FastAPI, HTTPException, APIRouter
from preferred_item_service.db.data import items

from preferred_item_service.utils.logger import custom_logger
logger = custom_logger(__file__)

router = APIRouter()

 

@router.get("/item/{item_id}")
async def get_item(item_id: str):
    """
    Get item by ID
    """
    for item in items:
        if item.identifier == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@router.get("/")
def get_all():
    """
    Get all items
    """

    # logger.info(f"All items : {items}")
    return items
