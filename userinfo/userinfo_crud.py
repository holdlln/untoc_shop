from sqlalchemy.orm import Session
from models import Userinfo  # User는 DB 모델이어야 합니다.
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 토큰 블랙리스트 저장소 (단순한 메모리 저장소로 시작)
token_blacklist = set()

def hash_password(hashed_password: str) -> str:
    """
    비밀번호를 해시화
    """
    return pwd_context.hash(hashed_password)

def create_user(db: Session, username: str, hashed_password: str, name: str, age: int, gender: str):
    """
    새 사용자 생성
    """
    hashed_password = hash_password(hashed_password)
    new_user = Userinfo(
        username=username,
        hashed_password=hashed_password,
        name=name,
        age=age,
        gender=gender,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_username(db: Session, username: str):
    """
    사용자 이름으로 사용자 검색
    """
    return db.query(Userinfo).filter(Userinfo.username == username).first()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    비밀번호 검증
    """
    return pwd_context.verify(plain_password, hashed_password)

def is_token_blacklisted(token: str) -> bool:
    """
    블랙리스트에서 토큰 확인
    """
    return token in token_blacklist

def blacklist_token(token: str):
    """
    토큰을 블랙리스트에 추가
    """
    token_blacklist.add(token)
