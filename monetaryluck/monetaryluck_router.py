from fastapi import APIRouter
import random
from .monetaryluck_schema import FortuneResponse

router = APIRouter(
    prefix="/monetaryluck",
    tags=["monetaryluck"]
)

# 운세 리스트 정의
FORTUNES = [
    "오늘은 새로운 기회가 찾아올 운입니다!",
    "조심하세요. 오늘은 신중한 결정을 내려야 할 날입니다.",
    "좋은 소식이 있을 예정입니다. 기대해 보세요!",
    "노력이 결실을 맺을 운입니다. 힘내세요!",
    "운이 따르는 하루가 될 것입니다. 자신감을 가지세요!"
]

@router.get("/random", response_model=FortuneResponse)
def get_random_fortune():
    """
    랜덤 운세를 반환합니다.
    """
    random_fortune = random.choice(FORTUNES)
    return {"fortune": random_fortune}
