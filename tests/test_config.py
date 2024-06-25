from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import middlewares
from app.database import get_db
from app.main import app
from settings import get_settings

settings = get_settings()
TEST_SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_user}:{settings.db_pass}" \
                               f"@{settings.db_host}:{settings.db_port}/test_{settings.db_name}"

engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
app.state.db = override_get_db
client = TestClient(app)

# def override_get_current_user():
#     user = User(id=1, username="test@example.com", firstname='test', lastname='test', email="test@example.com", hashed_password="fakehashedpassword")
#     return user.model_dump()
#
#
# app.dependency_overrides[get_current_user] = override_get_current_user
