from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from settings import get_settings

settings = get_settings()
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_user}:{settings.db_pass}" \
                          f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
