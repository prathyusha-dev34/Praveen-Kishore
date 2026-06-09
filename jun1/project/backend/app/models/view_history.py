from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.database import Base

class ViewHistory(Base):

    __tablename__ = "view_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    movie_id = Column(String)
    movie_title = Column(String)
    genre = Column(String)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )