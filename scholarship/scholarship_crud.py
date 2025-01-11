from sqlalchemy.orm import Session
from models import Scholarship  # models.py에서 가져오기

def insert_scholarship(db: Session, data: dict):
    """
    데이터베이스에 장학금 데이터를 추가하는 함수.
    """
    # 데이터베이스에 이미 존재하는지 확인
    existing = db.query(Scholarship).filter(Scholarship.link == data["link"]).first()
    if existing:
        return existing  # 이미 존재하면 추가하지 않음

    # 데이터 삽입
    scholarship = Scholarship(
        name=data["name"],
        link=data["link"],
        page_id=data["page_id"]
    )
    db.add(scholarship)
    db.commit()
    db.refresh(scholarship)
    return scholarship

def delete_scholarships_by_page_id(db: Session, page_id: int):
    db.query(Scholarship).filter(Scholarship.page_id == page_id).delete()
    db.commit()

def get_scholarships_by_page_id(db: Session, page_id: int):
    """
    특정 page_id를 가진 장학금 데이터를 가져오는 함수.

    Returns:
    - List[dict]: 장학금 데이터를 딕셔너리 리스트로 반환.
    """
    scholarships = db.query(Scholarship).filter(Scholarship.page_id == page_id).all()
    return [
        {
            "id": scholarship.id,
            "page_id": scholarship.page_id,
            "name": scholarship.name,
            "link": scholarship.link,
        }
        for scholarship in scholarships
    ]