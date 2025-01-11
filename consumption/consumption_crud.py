from sqlalchemy.orm import Session
from models import Consumption
from datetime import datetime, timedelta
from totalcategory.totalcategory_crud import update_totalcategory
from zoneinfo import ZoneInfo

from totalcategory.totalcategory_crud import update_totalcategory
from dateconsumption.dateconsumption_crud import update_dateconsumption_on_update

def create_consumption(db: Session, user_id: int, amount: float, category: int, description: str):
    """
    소비 내역을 추가하고 totalcategory를 업데이트합니다.
    """
    current_time_kst = datetime.now(ZoneInfo("Asia/Seoul"))
    
    new_consumption = Consumption(
        user_id=user_id,
        amount=amount,
        category=category,
        description=description,
        created_at=current_time_kst
    )
    db.add(new_consumption)
    db.commit()
    db.refresh(new_consumption)



    return new_consumption


def update_consumption(db: Session, consumption_id: int, user_id: int, amount: int, category: int, description: str):
    """
    특정 소비/소득 내역을 업데이트하고 Totalcategory 및 Dateconsumption을 수정합니다.
    """
    # 기존 소비/소득 데이터 가져오기
    consumption = db.query(Consumption).filter(
        Consumption.id == consumption_id,
        Consumption.user_id == user_id
    ).first()

    if not consumption:
        raise ValueError("해당 소비/소득 내역이 존재하지 않습니다.")

    # 기존 데이터와 변경될 데이터의 차이 계산
    old_amount = consumption.amount
    old_category = consumption.category
    category_changed = category != old_category  # 카테고리 변경 여부 확인

    # 기존 데이터 업데이트
    consumption.amount = amount
    consumption.category = category
    consumption.description = description

    db.commit()
    db.refresh(consumption)

    # Totalcategory 업데이트
    update_totalcategory(db=db, user_id=user_id, category=old_category, amount=-old_amount)
    update_totalcategory(db=db, user_id=user_id, category=category, amount=amount)

    # Dateconsumption 업데이트
    update_dateconsumption_on_update(
        db=db,
        user_id=user_id,
        date=consumption.created_at.date(),
        old_category=old_category,
        new_category=category,
        old_amount = old_amount,
        amount = amount
    )


    return consumption