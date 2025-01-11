from sqlalchemy.orm import Session
from models import Averageconsumption, Totalcategory
from fastapi import HTTPException
from averageconsumption.averageconsumption_schema import AverageConsumptionCreate, AverageConsumptionUpdate
from datetime import datetime, timedelta

# POST - 새 데이터 생성
def create_record(db: Session, data: AverageConsumptionCreate):
    new_record = Averageconsumption(
        age=data.age,
        gender=data.gender,
        classify_id=data.classify_id,
        content=data.content
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

# PUT - 기존 데이터 수정
def update_record(db: Session, record_id: int, data: AverageConsumptionUpdate):
    record = db.query(Averageconsumption).filter(Averageconsumption.id == record_id).first()
    if not record:
        raise ValueError("Record not found")
    record.age = data.age
    record.gender = data.gender
    record.classify_id = data.classify_id
    record.content = data.content

    db.commit()
    db.refresh(record)
    return record

# GET - classify_id, gender, 나이대별 Averageconsumption - Totalcategory
def get_average_vs_totalcategory(
    db: Session,
    current_user,
    classify_id: int,
):
    # 나이대 계산 (20, 30, 40 등)
    age_group = (current_user.age // 10) * 10

    # Averageconsumption에서 조건에 맞는 데이터 조회
    avg_consumption = db.query(Averageconsumption).filter(
        Averageconsumption.gender == current_user.gender,
        Averageconsumption.age == age_group,
        Averageconsumption.classify_id == classify_id,
    ).first()

    if not avg_consumption:
        raise HTTPException(status_code=404, detail="No average consumption data found")

    # Totalcategory에서 조건에 맞는 데이터 조회
    total_category = db.query(Totalcategory).filter(
        Totalcategory.user_id == current_user.id,
        Totalcategory.category == classify_id,
    ).first()

    if not total_category:
        raise HTTPException(status_code=404, detail="No total category data found")

    # 차이 계산: Averageconsumption.content - Totalcategory.consumption
    result = avg_consumption.content - total_category.consumption

    # 결과 반환
    return {
        "gender": current_user.gender,
        "age_group": age_group,
        "classify_id": classify_id,
        "difference": result,
    }