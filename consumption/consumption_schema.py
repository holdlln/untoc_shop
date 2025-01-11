from pydantic import BaseModel, Field
from datetime import datetime

class ConsumptionCreate(BaseModel):
    amount: int
    category: int = Field(..., ge=0, le=6)  # 0에서 5 사이의 값만 허용
    description: str


class ConsumptionResponse(BaseModel):
    id: int
    amount: int
    category: int
    description: str
    created_at: datetime
    
class ConsumptionUpdate(BaseModel):
    amount: int
    category: int = Field(..., ge=0, le=6)  # 0에서 5 사이의 값만 허용
    description: str
