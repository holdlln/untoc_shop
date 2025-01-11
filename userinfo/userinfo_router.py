from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta
from database import get_db  # 데이터베이스 세션 가져오기
from .userinfo_schema import TokenResponse, UserCreate, UserInfoResponse
from models import Userinfo
from .userinfo_crud import get_user_by_username, verify_password, create_user
from totalcategory.totalcategory_crud import initialize_totalcategory
from typing import Set
from dotenv import load_dotenv
import os

load_dotenv()
router = APIRouter()

# JWT 설정
SECRET_KEY = os.environ.get("SECRET_KEY")  # .env에서 로드된 값
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))

# OAuth2 설정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# 블랙리스트
token_blacklist: Set[str] = set()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def is_token_valid(token: str):
    """
    토큰 검증 및 블랙리스트 확인
    """
    if token in token_blacklist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is no longer valid",
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token",
        )
        
def get_current_user(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = db.query(Userinfo).filter(Userinfo.username == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    
    initialize_totalcategory(db, user.id)
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # 사용자 이름 중복 확인
    existing_user = db.query(Userinfo).filter(Userinfo.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # 사용자 생성
    new_user = create_user(db, user.username, user.hashed_password, user.name, user.age, user.gender)
    return {"message": "User created successfully", "user_id": new_user.id}

@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    """
    로그아웃 엔드포인트. 토큰을 블랙리스트에 추가합니다.
    """
    # 블랙리스트에 추가
    token_blacklist.add(token)
    return {"message": "Logged out successfully"}

@router.get("/userinfo", response_model=UserInfoResponse)
def get_user_info(db: Session = Depends(get_db), current_user: Userinfo = Depends(get_current_user)):
    """
    현재 사용자 정보를 반환합니다.
    """
    return {
        "name": current_user.name,
        "age": current_user.age,
        "gender": current_user.gender,
    }
