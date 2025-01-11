from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from consumption.consumption_crud import create_consumption, update_consumption
from consumption.consumption_schema import ConsumptionCreate
from totalcategory.totalcategory_crud import update_totalcategory
from dateconsumption.dateconsumption_crud import update_dateconsumption_on_input
from userinfo.userinfo_router import get_current_user
from models import Userinfo, Consumption
from datetime import datetime
from zoneinfo import ZoneInfo

router = APIRouter()

@router.post("/consumption")
def save_consumption(
    amount: int,
    category: int,
    description: str,
    db: Session = Depends(get_db),
    current_user: Userinfo = Depends(get_current_user)
):
    consumption = create_consumption(
        db=db,
        user_id=current_user.id,
        amount=amount,
        category=category,
        description=description,
    )
    
    update_totalcategory(
        db=db,
        user_id=current_user.id,
        category=category,
        amount=amount
    )
    
    today_date = datetime.now().date()
    update_dateconsumption_on_input(
        db=db,
        user_id=current_user.id,
        category=category,
        amount=amount,
        date=today_date,
    )
    
    
    return {"message": "Consumption saved successfully", "data": consumption}


@router.get("/consumption/recent")
def get_recent_consumptions(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    consumptions = (
        db.query(Consumption)
        .filter(Consumption.user_id == current_user.id)
        .order_by(Consumption.created_at.desc())
        .limit(5)
        .all()
    )
    return [
        {
            "id": c.id,
            "amount": c.amount,
            "category": c.category,
            "description": c.description,
            "created_at": c.created_at.astimezone(ZoneInfo("Asia/Seoul"))
        } for c in consumptions
    ]


@router.put("/consumption/{consumption_id}")
def update_consumption_entry(
    consumption_id: int,
    amount: int,
    category: int,
    description: str,
    db: Session = Depends(get_db),
    current_user: Userinfo = Depends(get_current_user)
):
    """
    소비/소득 내역을 업데이트합니다.
    """
    try:
        updated_consumption = update_consumption(
            db=db,
            consumption_id=consumption_id,
            user_id=current_user.id,
            amount=amount,
            category=category,
            description=description
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return {
        "message": "Consumption updated successfully",
        "data": {
            "id": updated_consumption.id,
            "amount": updated_consumption.amount,
            "category": updated_consumption.category,
            "description": updated_consumption.description,
            "created_at": updated_consumption.created_at.astimezone(ZoneInfo("Asia/Seoul")),
        }
    }
