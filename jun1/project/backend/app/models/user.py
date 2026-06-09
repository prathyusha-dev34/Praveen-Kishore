from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship

from app.database.database import Base

from app.models.view_history import ViewHistory
from app.models.user_preference import UserPreference

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    password = Column(String, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    favorites = relationship(
        "Favorite",
        backref="user",
        cascade="all, delete"
    )

    reviews = relationship(
        "Review",
        backref="user",
        cascade="all, delete"
    )

    search_history = relationship(
        "SearchHistory",
        backref="user",
        cascade="all, delete"
    )

    view_history = relationship(
    "ViewHistory",
    backref="user"
    )

    preferences = relationship(
    "UserPreference",
    backref="user"
    )