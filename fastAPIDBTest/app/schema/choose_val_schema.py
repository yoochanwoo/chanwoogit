from pydantic import BaseModel
from datetime import datetime

class ChooseValCreate(BaseModel):
    high_loc: str
    low_loc: str
    theme1: str
    theme2: str
    theme3: str
    theme4: str
    days: int

class ChooseValResponse(ChooseValCreate):
    choose_id: int
    regdate: datetime
    uptdate: datetime

    class Config:
        orm_mode = True