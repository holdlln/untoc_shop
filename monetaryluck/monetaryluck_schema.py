from pydantic import BaseModel

class FortuneResponse(BaseModel):
    fortune: str
