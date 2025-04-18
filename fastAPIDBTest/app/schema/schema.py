from pydantic import BaseModel
from datetime import datetime

"""
스키마 클래스 정의
"""


""" 유찬우 """
# 선택값 리퀘스트
class ChooseValCreate(BaseModel):
    high_loc: str
    low_loc: str
    theme1: str
    theme2: str
    theme3: str
    theme4: str
    days: int

# 선택값 리스폰스
class ChooseValResponse(ChooseValCreate):
    choose_id: int
    regdate: datetime
    uptdate: datetime

    class Config:
        orm_mode = True
""" 유찬우 끝 """