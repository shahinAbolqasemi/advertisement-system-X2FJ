from app.models import Advertise, AdvertiseStatus, Comment
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


def test_ad_update(test_db, test_user, test_login_user):
    ad = Advertise(status=AdvertiseStatus.ACTIVE, title="Update Ad", owner_id=test_user.id)
    test_db.add(ad)
    test_db.commit()
    ad_data = {"title": "Updated Ad"}
    headers = {
        'Authorization': f"Bearer {test_login_user['access_token']}"
    }
    response = client.put(f"/ads/{ad.id}", json=ad_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Ad"


def test_ad_partial_update(test_db, test_user, test_login_user):
    ad = Advertise(status=AdvertiseStatus.ACTIVE, title="Update Ad 1", owner_id=test_user.id)
    test_db.add(ad)
    test_db.commit()
    headers = {
        'Authorization': f"Bearer {test_login_user['access_token']}"
    }
    ad_data = {"description": "Updated Description"}
    response = client.patch(f"/ads/{ad.id}", json=ad_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["description"] == "Updated Description"


def test_ad_delete(test_db, test_user, test_login_user):
    ad = Advertise(status=AdvertiseStatus.ACTIVE, title="Update Ad 2", owner_id=test_user.id)
    test_db.add(ad)
    test_db.commit()
    headers = {
        'Authorization': f"Bearer {test_login_user['access_token']}"
    }
    response = client.delete(f"/ads/{ad.id}", headers=headers)
    assert response.status_code == 200


def test_ad_comments_list(test_db, test_user, test_login_user):
    ad = Advertise(status=AdvertiseStatus.ACTIVE, title="Ad with Comments", owner_id=test_user.id)
    comment = Comment(advertise_id=ad.id, owner_id=test_user.id, content="Comment for ad")
    test_db.add(ad)
    test_db.add(comment)
    test_db.commit()
    response = client.get(f"/ads/{ad.id}/comments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_ad_comment_create(test_db, test_user, test_login_user):
    ad = Advertise(status=AdvertiseStatus.ACTIVE, title="Ad with Comments 123", owner_id=test_user.id)
    test_db.add(ad)
    test_db.commit()
    comment_data = {
        "content": "N" * 100
    }
    headers = {
        'Authorization': f"Bearer {test_login_user['access_token']}"
    }
    response = client.post(f"/ads/{ad.id}/comments", json=comment_data, headers=headers)
    assert response.status_code == 201
    assert response.json()["content"] == "N" * 100
