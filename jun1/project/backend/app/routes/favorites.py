from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.favorite import Favorite
from app.models.user import User
from app.schemas.favorite_schema import FavoriteCreate
from app.services.auth_service import get_current_user

router = APIRouter()


# =========================
# ADD FAVORITE
# =========================
@router.post("/favorites")
def add_favorite(
    favorite: FavoriteCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    existing = db.query(Favorite).filter(
        Favorite.movie_id == favorite.movie_id,
        Favorite.user_id == user.id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already exists")

    new_fav = Favorite(
        movie_id=favorite.movie_id,
        title=favorite.title,
        poster=favorite.poster,
        user_id=user.id
    )

    db.add(new_fav)
    db.commit()
    db.refresh(new_fav)

    return new_fav


# =========================
# GET FAVORITES
# =========================
@router.get("/favorites")
def get_favorites(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    return db.query(Favorite).filter(
        Favorite.user_id == user.id
    ).all()


# =========================
# DELETE FAVORITE
# =========================
@router.delete("/favorites/{movie_id}")
def delete_favorite(
    movie_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    fav = db.query(Favorite).filter(
        Favorite.movie_id == movie_id,
        Favorite.user_id == user.id
    ).first()

    if not fav:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(fav)
    db.commit()

    return {"message": "Deleted successfully"}