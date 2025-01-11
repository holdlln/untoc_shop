from pydantic import BaseModel

# 공통 속성
class AverageConsumptionBase(BaseModel):
    age: int
    gender: str
    classify_id: int
    content: int

# POST 요청용
class AverageConsumptionCreate(AverageConsumptionBase):
    pass

# PUT 요청용
class AverageConsumptionUpdate(AverageConsumptionBase):
    pass

# 응답용
class AverageConsumptionResponse(AverageConsumptionBase):
    id: int

    class Config:
        from_attributes = True  # SQLAlchemy 모델과 호환
