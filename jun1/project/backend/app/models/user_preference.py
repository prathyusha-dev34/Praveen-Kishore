from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from app.database.database import Base


class UserPreference(Base):

    __tablename__ = "user_preferences"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    genre = Column(String)

    score = Column(
        Integer,
        default=1
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )