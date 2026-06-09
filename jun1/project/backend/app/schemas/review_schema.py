from pydantic import BaseModel

class ReviewCreate(BaseModel):
    movie_id: str
    review_text: str
    rating: int


class ReviewUpdate(BaseModel):
    review_text: str
    rating: int