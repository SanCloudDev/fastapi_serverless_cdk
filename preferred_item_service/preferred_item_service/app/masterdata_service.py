
from fastapi import  HTTPException, APIRouter
from preferred_item_service.db.model import MasterData
from preferred_item_service.db.data import master_data
from typing  import List

from preferred_item_service.utils.logger import custom_logger
logger = custom_logger(__file__)

router = APIRouter()

 
@router.get("/")
def get_all_masterdata(skip: int = 0, limit: int = 100) -> List[MasterData]:

    # logger.info(f"All items in master data : {master_data}")
    return master_data

 
@router.get("/item/{item_id}")
def get_masterdata_id(item_id: str) -> MasterData:
    for item_data in master_data:
        if item_data.identifier == item_id:
            return item_data
        else:
         raise HTTPException(status_code=404, detail="MasterData not found") 

    return master_data