import requests
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.auth_service import get_current_user
from app.models.favorite import Favorite

router = APIRouter(tags=["Recommendations"])


# =========================
# CHECK POSTER URL
# =========================
def is_valid_poster(url: str) -> bool:
    if not url or url == "N/A":
        return False

    try:
        response = requests.get(url, timeout=3, stream=True)
        return response.status_code == 200
    except Exception:
        return False


# =========================
# RECOMMENDATIONS
# =========================
@router.get("/recommendations")
def get_recommendations(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    favorites = db.query(Favorite).filter(
        Favorite.user_id == user.id
    ).all()

    recommendations = []

    for fav in favorites:
        if is_valid_poster(fav.poster):
            recommendations.append({
                "title": fav.title,
                "poster": fav.poster,
                "reason": "From Favorites"
            })

    return {
        "recommended_movies": recommendations
    }