from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from userinfo.userinfo_crud import is_token_blacklisted
from averageconsumption.averageconsumption_router import router as averageconsumption_router
from consumption.consumption_router import router as consumption_router
from scholarship.scholarship_router import router as scholarship_router
from totalcategory.totalcategory_router import router as totalcategory_router
from dateconsumption.dateconsumption_router import router as dateconsumption_router
from monetaryluck.monetaryluck_router import router as monetaryluck_router
from userinfo.userinfo_router import router as userinfo_router
import sys
import os
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware



# 환경 변수 설정
SECRET_KEY = os.environ.get("SECRET_KEY", "your_secret_key")
ALGORITHM = "HS256"

app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_token(token: str = Depends(oauth2_scheme)):
    """
    토큰 검증 및 블랙리스트 확인
    """
    if is_token_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is no longer valid",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# 라우터 등록
app.include_router(userinfo_router, prefix="/auth", tags=["userinfo"])
app.include_router(averageconsumption_router, tags=["averageconsumption"])
app.include_router(consumption_router, prefix="/consumption", tags=["consumption"])
app.include_router(scholarship_router, tags=["scholarship"])
app.include_router(totalcategory_router, tags=["totalcategory"])
app.include_router(dateconsumption_router, tags=["dateconsumption"])
app.include_router(monetaryluck_router, tags=["monetaryluck"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
