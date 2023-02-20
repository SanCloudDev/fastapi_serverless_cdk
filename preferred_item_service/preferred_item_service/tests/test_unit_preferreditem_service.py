from fastapi.testclient import TestClient
from preferred_item_service.api.main import app
from preferred_item_service.db.model import Item, Brick, MasterData, ItemStatus
from preferred_item_service.db.data import items, master_data


client = TestClient(app)


def test_get_preferred_item():
    # Test case where a preferred item is found
    bricks = [
        Brick(design_id=1, color_codes=[1, 2]),
        Brick(design_id=2, color_codes=[3, 4]),
    ]
    response = client.post("/preferred-item", json={"bricks": bricks})
    assert response.status_code == 200
    assert response.json()["preferred_item"]["identifier"] == "item1"
    assert response.json()["item_info"]["identifier"] == "item1"
    assert response.json()["item_info"]["status"] == ItemStatus.Normal.value
    assert response.json()["item_info"]["price"] == 10.0

    # Test case where multiple preferred items are found, but the first one is returned
    bricks = [        
        Brick(design_id=1, color_codes=[1, 2]),
        Brick(design_id=2, color_codes=[4, 3]),
    ]
    response = client.post("/preferred-item", json={"bricks": bricks})
    assert response.status_code == 200
    assert response.json()["preferred_item"]["identifier"] == "item2"
    assert response.json()["item_info"]["identifier"] == "item2"
    assert response.json()["item_info"]["status"] == ItemStatus.Novelty.value
    assert response.json()["item_info"]["price"] == 5.0

    # Test case where no preferred item is found
    bricks = [        
        Brick(design_id=1, color_codes=[1, 2]),
        Brick(design_id=2, color_codes=[5, 6]),
    ]
    response = client.post("/preferred-item", json={"bricks": bricks})
    assert response.status_code == 404
    assert response.json()["detail"] == "No preferred item found for the provided bricks"
