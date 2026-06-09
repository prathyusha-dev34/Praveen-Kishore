from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.review import Review
from app.models.user import User
from app.routes.favorites import get_current_user
from app.schemas.review_schema import ReviewCreate

from app.schemas.review_schema import ReviewCreate, ReviewUpdate

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)

# CREATE REVIEW
@router.post("/reviews")
def create_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    if review.rating < 1 or review.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be 1-5")

    new_review = Review(
        movie_id=review.movie_id,
        review_text=review.review_text,
        rating=review.rating,
        user_id=user.id
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return new_review


# GET REVIEWS BY MOVIE
@router.get("/reviews/{movie_id}")
def get_reviews(movie_id: str, db: Session = Depends(get_db)):

    reviews = db.query(Review)\
        .filter(Review.movie_id == movie_id)\
        .all()

    return {
        "success": True,
        "data": reviews
    }


# UPDATE REVIEW
@router.put("/reviews/{review_id}")
def update_review(
    review_id: int,
    review: ReviewUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    db_review = db.query(Review).filter(
        Review.id == review_id,
        Review.user_id == user.id
    ).first()

    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    db_review.review_text = review.review_text
    db_review.rating = review.rating

    db.commit()
    return {"message": "Updated successfully"}


# DELETE REVIEW
@router.delete("/reviews/{review_id}")
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    review = db.query(Review).filter(
        Review.id == review_id,
        Review.user_id == user.id
    ).first()

    if not review:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(review)
    db.commit()

    return {"message": "Deleted successfully"}