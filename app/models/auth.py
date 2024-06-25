from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Uuid

from ..database import Base


class Session(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE", onupdate="CASCADE"))
    expire_datetime = Column(DateTime(timezone=True))
    session_key = Column(Uuid)
    revoked = Column(Boolean, server_default='f')
