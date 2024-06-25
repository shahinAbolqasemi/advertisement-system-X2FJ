import pytest
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, drop_database

from app import models
from app.database import Base
from app.models import User, Advertise, AdvertiseStatus
from app.security.password import get_password_hash
from tests.test_config import TEST_SQLALCHEMY_DATABASE_URL, engine, TestingSessionLocal, client


@pytest.fixture(scope='module')
def test_db():
    try:
        create_database(TEST_SQLALCHEMY_DATABASE_URL)
    except:
        drop_database(TEST_SQLALCHEMY_DATABASE_URL)
        create_database(TEST_SQLALCHEMY_DATABASE_URL)
    try:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        db = TestingSessionLocal()
        yield db
        db.close()
        Base.metadata.drop_all(bind=engine)
    finally:
        drop_database(TEST_SQLALCHEMY_DATABASE_URL)


@pytest.fixture(scope='module')
def test_user(test_db: Session):
    user = User(
        username="testuser@example.com",
        email="testuser@example.com",
        firstname="test",
        lastname="test",
        hashed_password=get_password_hash("password")
    )  # Replace with appropriate user attributes
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture(scope='module')
def test_login_user(test_user: models.User):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': '',
        'username': 'testuser@example.com',
        'password': 'password',
        'scope': '',
        'client_id': '',
        'client_secret': '',
    }
    response = client.post('/auth/login', data=data, headers=headers)
    return response.json()


@pytest.fixture(scope='module')
def test_ad(test_db: Session, test_user: User):
    ad = Advertise(status=AdvertiseStatus.ACTIVE, title="Test Ad",
                   owner_id=test_user.id)  # Ensure this matches your Advertise model's requirements
    test_db.add(ad)
    test_db.commit()
    test_db.refresh(ad)
    return ad
