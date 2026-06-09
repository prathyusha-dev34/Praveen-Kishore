from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.search_history import SearchHistory
from app.models.user import User

from app.services.auth_service import (
    get_current_user
)

router = APIRouter(
    prefix="/history",
    tags=["History"]
)

@router.get("/history")
def get_history(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    history = (
        db.query(SearchHistory)
        .filter(
            SearchHistory.user_id == user.id
        )
        .order_by(
            SearchHistory.searched_at.desc()
        )
        .limit(10)
        .all()
    )

    return {
        "success": True,
        "data": [
            {
                "keyword": item.keyword,
                "searched_at": item.searched_at
            }
            for item in history
        ]
    }