from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.search_history import SearchHistory

from app.services.omdb_service import search_movies, get_movie

from app.services.auth_service import get_current_user
from app.models.user import User

router = APIRouter(
    tags=["Movies"]
)

# =========================
# HOME MOVIES (NO AUTH)
# =========================
@router.get("/movies")
def home_movies():
    return search_movies("batman")


# =========================
# SEARCH MOVIES
# =========================
@router.get("/movies/search")
def search(
    title: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    if not title.strip():
        raise HTTPException(
            status_code=400,
            detail="Invalid request"
        )

    data = search_movies(title)

    if not data or data.get("Response") == "False":
        return []

    movies = data.get("Search", [])

    history = SearchHistory(
        keyword=title,
        user_id=user.id
    )

    db.add(history)
    db.commit()

    return movies


# =========================
# GET MOVIE BY TITLE (optional)
# =========================
@router.get("/movies/{title}")
def search_by_title(title: str):

    data = search_movies(title)

    if not data or data.get("Response") == "False":
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return data


# =========================
# GET MOVIE DETAILS BY IMDB ID (NEW FIX)
# =========================
@router.get("/movies/id/{imdb_id}")
def get_movie_details(imdb_id: str):

    data = get_movie(imdb_id)

    if not data or data.get("Response") == "False":
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return data