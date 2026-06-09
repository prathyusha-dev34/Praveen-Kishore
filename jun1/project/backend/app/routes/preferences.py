from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.auth_service import get_current_user
from app.services.preference_service import save_user_preferences
from app.schemas.user_preference_schema import UserPreferenceCreate


router = APIRouter(prefix="/preferences", tags=["Preferences"])


@router.post("/")
def add_preferences(
    data: UserPreferenceCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    return save_user_preferences(
        db=db,
        user_id=user.id,
        genre=data.genre,
        score=data.score
    )