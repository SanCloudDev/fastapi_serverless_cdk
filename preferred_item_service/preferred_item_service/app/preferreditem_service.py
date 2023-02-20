from fastapi import FastAPI, APIRouter, HTTPException
from operator import attrgetter
from functools import reduce
from collections import defaultdict
from preferred_item_service.db.data import items, master_data
from preferred_item_service.db.model import PreferredItemRequest, PreferredItemResponse, ItemStatus

from preferred_item_service.utils.logger import custom_logger
logger = custom_logger(__file__)

router = APIRouter()
logger.info("Preferre Item serivce")

@router.post("/", response_model=PreferredItemResponse)
def get_preferred_item(request: PreferredItemRequest):
    logger.info(f"Items Reguest: {request.json}")
    brick_set = set(
        [(brick.design_id, tuple(brick.color_codes)) for brick in request.bricks]
    )
    brick_dict = defaultdict(list)
    for brick in request.bricks:
        brick_dict[brick.design_id].append(tuple(brick.color_codes))
    possible_items = []
    for item in items:
        item_brick_set = set(
            [(brick.design_id, tuple(brick.color_codes)) for brick in item.bricks]
        )
        if item_brick_set == brick_set:
            possible_items.append(item)

    if len(possible_items) == 0:
        raise HTTPException(
            status_code=404, detail="No preferred item found for the provided bricks"
        )

    sorted_items = sorted(
        possible_items,
        key=lambda item: (
            attrgetter("status")(
                next(md for md in master_data if md.identifier == item.identifier)
            ),
            attrgetter("price")(
                next(md for md in master_data if md.identifier == item.identifier)
            ),
        ),
    )

    # get master data of  the items
    item_info = []
    for item in sorted_items:
        item_info.append(
            {
                "identifier": item.identifier,
                "status": next(
                    md.status for md in master_data if md.identifier == item.identifier
                ).value,
                "price": next(
                    md.price for md in master_data if md.identifier == item.identifier
                ),
            }
        )
    logger.info(f"preferred item: {sorted_items[0].identifier}")
    return {"preferred_item": sorted_items[0], "item_info": item_info[0]}


@router.post("/", response_model=PreferredItemResponse)
def get_preferred_item_score(request: PreferredItemRequest): 
    scores = {}
    for item in items:
        item_id = item["id"] 
        item_bricks = item["bricks"]

        # Check if the item's bricks match the given bricks
        if all(brick in item_bricks for brick in request.bricks):
            # If the item's bricks match the given bricks, calculate the score for the item
            item_status = None
            item_price = None
            for data in master_data:
                if data["item_id"] == item_id:
                    item_status = data["status"]
                    item_price = data["price"]
                    break
            if item_status and item_price: 
                if item_status == ItemStatus.Normal:
                    status_weight = 3
                elif item_status == ItemStatus.Novelty:
                    status_weight = 2
                elif item_status == ItemStatus.Outgoing:
                    status_weight = 1
                else:
                    status_weight = 0
     # Calculate the score for the item by multiplying the status weight and the inverse of the price
                score = status_weight * (1 / item_price)
                scores[item_id] = score 

    sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=True) 
    if not sorted_items:
        return None
    # Get the preferred item, which is the item with the highest score
    preferred_item_id = sorted_items[0][0]
    preferred_item = next(item for item in items if item["id"] == preferred_item_id)
    return preferred_item