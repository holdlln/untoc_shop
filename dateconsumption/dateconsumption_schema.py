from pydantic import BaseModel
from datetime import date

class Create(BaseModel):
    date: date
    total_income: float
    total_consumption: float

    class Config:
        from_attributes = True
