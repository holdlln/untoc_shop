from fastapi import APIRouter, HTTPException, Depends, Response,Security

from sqlalchemy.orm import Session
from database import get_db

from .dateconsumption_schema import Create
from models import Dateconsumption, Consumption
from zoneinfo import ZoneInfo

from userinfo.userinfo_router import get_current_user
from sqlalchemy.sql import func

from datetime import datetime, timedelta

router = APIRouter(
    prefix="/dateconsumption"
)

def insert_data(db, table):
    db.add(table)
    db.commit()
    db.refresh(table)
    
@router.get("/dateconsumption")
def get_datewise_summary(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    datewise = (
        db.query(Dateconsumption)
        .filter(Dateconsumption.user_id == current_user.id)
        .order_by(Dateconsumption.date)
        .all()
    )
    return [
        {
            "date": d.date,
            "total_income": d.total_income,
            "total_consumption": d.total_consumption
        } for d in datewise
    ]
    
    
@router.get("/dateconsumption/{date}")
def get_consumptions_by_date(date: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        # 날짜 파싱
        parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    print(f"Fetching consumptions for user_id: {current_user.id}, date: {parsed_date}")

    # 날짜 범위 비교
    consumptions = (
        db.query(Consumption)
        .filter(
            Consumption.user_id == current_user.id,
            Consumption.created_at >= parsed_date,
            Consumption.created_at < parsed_date + timedelta(days=1)
        )
        .all()
    )

    # 결과 출력
    print(f"Found consumptions: {consumptions}")

    return [
        {
            "id": c.id,
            "amount": c.amount,
            "category": c.category,
            "description": c.description,
            "created_at": c.created_at
        } for c in consumptions
    ]