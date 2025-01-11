from sqlalchemy.orm import Session
from sqlalchemy.sql import func 
from models import Totalcategory, Consumption

def initialize_totalcategory(db: Session, user_id: int):
    """
    로그인 시 totalcategory를 초기화하고 기존 consumption 데이터를 반영
    """
    # 기존 사용자의 totalcategory 초기화
    db.query(Totalcategory).filter(Totalcategory.user_id == user_id).delete()
    
    # category별 소비 합계 계산
    category_totals = (
        db.query(Consumption.category, func.sum(Consumption.amount).label("total"))
        .filter(Consumption.user_id == user_id)
        .group_by(Consumption.category)
        .all()
    )

    # 계산 결과를 totalcategory에 추가
    for category, total in category_totals:
        db.add(Totalcategory(user_id=user_id, category=category, consumption=total))
    
    # category 초기화 후 누락된 카테고리를 0으로 설정
    all_categories = {0, 1, 2, 3, 4, 5, 6}  # 전체 카테고리 목록
    existing_categories = {row.category for row in category_totals}
    for category in all_categories - existing_categories:
        db.add(Totalcategory(user_id=user_id, category=category, consumption=0))
    
    db.commit()

def update_totalcategory(db: Session, user_id: int, category: int, amount: int):
    """
    소비 입력 시 해당 카테고리 소비를 업데이트
    """
    # 해당 사용자의 특정 카테고리 데이터를 가져옴
    category_data = (
        db.query(Totalcategory)
        .filter(Totalcategory.user_id == user_id, Totalcategory.category == category)
        .first()
    )
    
    if category_data:
        # 기존 값에 amount 추가
        category_data.consumption += amount
    else:
        # 없으면 새로 추가
        db.add(Totalcategory(user_id=user_id, category=category, consumption=amount))
    
    db.commit()
