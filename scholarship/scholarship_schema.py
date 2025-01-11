from pydantic import BaseModel

class Create(BaseModel):
    name: str
    link: str