from pydantic import BaseModel
from typing import Optional

class TotalCategoryResponse(BaseModel):
    category: int
    consumption: float

    class Config:
        orm_mode = True


