from pydantic import BaseModel


class UserPreferenceCreate(BaseModel):
    genre: str
    score: int = 1