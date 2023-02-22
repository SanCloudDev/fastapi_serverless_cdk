from preferred_item_service.db.model import Item, Brick, MasterData, ItemStatus

from preferred_item_service.utils.logger import custom_logger
logger = custom_logger(__file__)


# Dummy Data for testing purpose

logger.info("fetching data")

items = [
    Item(
        identifier="item1",
        bricks=[
            Brick(design_id=1, color_codes=[1, 2]),
            Brick(design_id=2, color_codes=[3, 4]),
        ],
    ),
    Item(
        identifier="item2",
        bricks=[
            Brick(design_id=1, color_codes=[1, 2]),
            Brick(design_id=2, color_codes=[4, 3]),
        ],
    ),
    Item(
        identifier="item3",
        bricks=[
            Brick(design_id=1, color_codes=[1, 2]),
            Brick(design_id=3, color_codes=[5, 6]),
        ],
    ),
    Item(identifier="item4", bricks=[Brick(design_id=1, color_codes=[1, 2])]),
    Item(
        identifier="item5",
        bricks=[
            Brick(design_id=3, color_codes=[1, 2]),
            Brick(design_id=2, color_codes=[3, 4]),
        ],
    ),
    Item(
        identifier="item6",
        bricks=[
            Brick(design_id=3, color_codes=[1, 2]),
            Brick(design_id=2, color_codes=[4, 3]),
        ],
    ),
    Item(
        identifier="item7",
        bricks=[
            Brick(design_id=2, color_codes=[1, 2]),
            Brick(design_id=3, color_codes=[5, 6]),
        ],
    ),
    Item(identifier="item8", bricks=[Brick(design_id=2, color_codes=[1, 2])]),
    Item(identifier="item9", bricks=[Brick(design_id=2, color_codes=[1, 2])]),
    Item(identifier="item10", bricks=[Brick(design_id=2, color_codes=[1, 2])]),
    Item(identifier="item11", bricks=[Brick(design_id=2, color_codes=[1, 2])]),
]

master_data = [
    MasterData(identifier="item1", status=ItemStatus.Normal, price=10.0),
    MasterData(identifier="item2", status=ItemStatus.Novelty, price=5.0),
    MasterData(identifier="item3", status=ItemStatus.Outgoing, price=7.0),
    MasterData(identifier="item4", status=ItemStatus.Normal, price=3.0),
    MasterData(identifier="item5", status=ItemStatus.Normal, price=9.0),
    MasterData(identifier="item6", status=ItemStatus.Novelty, price=6.0),
    MasterData(identifier="item7", status=ItemStatus.Outgoing, price=4.0),
    MasterData(identifier="item8", status=ItemStatus.Normal, price=7.0),
    MasterData(identifier="item9", status=ItemStatus.Novelty, price=3.0),
    MasterData(identifier="item10", status=ItemStatus.Outgoing, price=3.0),
    MasterData(identifier="item11", status=ItemStatus.Discontinued, price=10.0),
]
