from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from .scholarship1_crawler import fetch_scholarships
from .scholarship2_crawler import fetch_scholarships2
from .scholarship_crud import insert_scholarship, delete_scholarships_by_page_id, get_scholarships_by_page_id

router = APIRouter(
    prefix="/scholarship"
)


@router.post("/crawl/1")
def crawl_and_save_scholarships1(
    limit: int = 15,
    db: Session = Depends(get_db)
):
    # page_id=0 데이터 삭제
    delete_scholarships_by_page_id(db, page_id=0)

    # 크롤링 실행
    scholarships = fetch_scholarships(limit=limit)

    # 데이터 저장
    for data in scholarships:
        insert_scholarship(db, data)

    return {"message": f"Successfully crawled and saved {len(scholarships)} scholarships"}


@router.post("/crawl/2")
def crawl_and_save_scholarships2(
    limit: int = 15,  # 최대 크롤링할 항목 수
    db: Session = Depends(get_db)
):
    # 1. page_id가 2인 데이터 삭제
    delete_scholarships_by_page_id(db, page_id=2)

    # 2. scholarship2 크롤링
    scholarships = fetch_scholarships2(limit=limit)

    # 3. 데이터베이스에 저장
    for data in scholarships:
        insert_scholarship(db, data)

    return {"message": f"Successfully crawled and saved {len(scholarships)} scholarships"}

@router.get("/1")
def get_scholarships1(limit: int = 15, db: Session = Depends(get_db)):
    """
    장학금 1 (page_id=0) 데이터를 반환하는 엔드포인트.
    """
    # POST 요청 먼저 실행
    crawl_and_save_scholarships1(limit=limit, db=db)

    scholarships = get_scholarships_by_page_id(db, page_id=0)
    return {"scholarships": scholarships}

@router.get("/2")
def get_scholarships2(limit: int = 15, db: Session = Depends(get_db)):
    """
    장학금 2 (page_id=2) 데이터를 반환하는 엔드포인트.
    """

    crawl_and_save_scholarships2(limit=limit, db=db)

    scholarships = get_scholarships_by_page_id(db, page_id=2)
    return {"scholarships": scholarships}