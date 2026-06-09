from pydantic import BaseModel
from datetime import datetime

class HistoryResponse(BaseModel):

    keyword: str

    searched_at: datetime