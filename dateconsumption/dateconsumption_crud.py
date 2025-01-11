from sqlalchemy.orm import Session
from models import Dateconsumption, Consumption
from sqlalchemy.sql import func

def update_dateconsumption_on_input(db: Session, user_id: int, category: int, amount: int, date: str):
    """
    소비/소득 입력 시 자동으로 dateconsumption 테이블 업데이트.
    """
    existing_entry = (
        db.query(Dateconsumption)
        .filter(
            Dateconsumption.user_id == user_id,
            Dateconsumption.date == date,
        )
        .first()
    )

    if not existing_entry:
        # 새로운 날짜에 대한 데이터 추가
        new_entry = Dateconsumption(
            user_id=user_id,
            date=date,
            total_income=amount if category == 0 else 0,
            total_consumption=amount if category != 0 else 0,
        )
        db.add(new_entry)
    else:
        # 기존 데이터 업데이트
        if category == 0:
            existing_entry.total_income += amount
        else:
            existing_entry.total_consumption += amount

    db.commit()


def update_dateconsumption_on_update(
    db: Session,
    user_id: int,
    date: str,
    old_category: int,
    new_category: int,
    old_amount: int,
    amount: int
):
    """
    소비/소득 내역 수정 시 Dateconsumption 데이터를 업데이트합니다.
    """
    # 날짜 데이터 가져오기
    date_entry = db.query(Dateconsumption).filter(
        Dateconsumption.user_id == user_id,
        Dateconsumption.date == date
    ).first()

    if not date_entry:
        # 날짜 데이터가 없으면 생성
        date_entry = Dateconsumption(
            user_id=user_id,
            date=date,
            total_income=0,
            total_consumption=0
        )
        db.add(date_entry)

    # 기존 카테고리 제거
    if old_category == 0:  # 기존이 소득
        date_entry.total_income -= old_amount
    else:  # 기존이 소비
        date_entry.total_consumption -= old_amount

    # 새로운 카테고리 추가
    if new_category == 0:  # 새로 변경된 것이 소득
        date_entry.total_income += amount
    else:  # 새로 변경된 것이 소비
        date_entry.total_consumption += amount

    # 값이 0 이하가 되면 강제로 0으로 처리
    date_entry.total_income = max(date_entry.total_income, 0)
    date_entry.total_consumption = max(date_entry.total_consumption, 0)

    db.commit()
