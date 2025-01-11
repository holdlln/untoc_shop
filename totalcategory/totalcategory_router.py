from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Totalcategory
from userinfo.userinfo_router import get_current_user

router = APIRouter()

@router.get("/totalcategory/{category_id}") #카테고리별 소비
def get_category_total(category_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    total = db.query(Totalcategory).filter(
        Totalcategory.user_id == current_user.id, Totalcategory.category == category_id
    ).first()
    return {"category_id": category_id, "total_consumption": total.consumption if total else 0}

@router.get("/totalcategory") #원그래프
def get_all_category_totals(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    totals = db.query(Totalcategory).filter(Totalcategory.user_id == current_user.id).all()
    return [{"category_id": t.category, "total_consumption": t.consumption} for t in totals]