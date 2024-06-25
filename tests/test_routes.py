from app.models import Advertise, AdvertiseStatus
from tests.test_config import client


def test_ads_list(test_db):
    response = client.get("/ads")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_ad_retrieve(test_db, test_user):
    ad = Advertise(status=AdvertiseStatus.ACTIVE, title="Test Ad",
                   owner_id=test_user.id)
    test_db.add(ad)
    test_db.commit()
    response = client.get(f"/ads/{ad.id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Ad"


def test_ad_create(test_login_user):
    ad_data = {
        "title": "New Ad",
        "description": "This is a new ad",
    }
    headers = {
        'Authorization': f"Bearer {test_login_user['access_token']}"
    }
    response = client.post("/ads", json=ad_data, headers=headers)
    assert response.status_code == 201
    assert response.json()["title"] == "New Ad"
