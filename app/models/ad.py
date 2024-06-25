from datetime import datetime
from functools import partial

import pytz
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint

from ..database import Base


class Advertise(Base):
    __tablename__ = "advertise"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    description = Column(String)
    timestamp = Column(DateTime(timezone=True), default=partial(datetime.now, tz=pytz.UTC))
    status = Column(Boolean, default=True)

    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE", onupdate="CASCADE"))


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    content = Column(String)
    timestamp = Column(DateTime(timezone=True), default=partial(datetime.now, tz=pytz.UTC))

    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE", onupdate="CASCADE"))
    advertise_id = Column(Integer, ForeignKey('advertise.id', ondelete="CASCADE", onupdate="CASCADE"))
    __table_args__ = (
        UniqueConstraint("user_id", "advertise_id", name="unique_user_advertise_comment"),
    )
