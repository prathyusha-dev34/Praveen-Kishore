from sqlalchemy.orm import Session
from app.models.user_preference import UserPreference


def save_user_preferences(db: Session, user_id: int, genre: str, score: int):

    pref = UserPreference(
        user_id=user_id,
        genre=genre,
        score=score
    )

    db.add(pref)
    db.commit()
    db.refresh(pref)

    return pref