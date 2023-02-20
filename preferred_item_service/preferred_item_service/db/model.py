from typing import List
from pydantic import BaseModel
from enum import Enum


class Brick(BaseModel):
    design_id: int
    color_codes: List[int]


class Item(BaseModel):
    identifier: str
    bricks: List[Brick]


class ItemStatus(str, Enum):
    Normal = "Normal"
    Novelty = "Novelty"
    Outgoing = "Outgoing"
    Discontinued = "Discontinued"


class MasterData(BaseModel):
    identifier: str
    status: ItemStatus
    price: float


class PreferredItemRequest(BaseModel):
    bricks: List[Brick]


class PreferredItemResponse(BaseModel):
    preferred_item: Item
    item_info:  MasterData
