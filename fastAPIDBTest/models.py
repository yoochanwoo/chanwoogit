from sqlalchemy import Column, Integer, String, DateTime
#from sqlalchemy.orm import relationship # 테이블간 관계 정의시 사용
from db import Base
from datetime import datetime

"""유찬우"""
# 선택값 테이블 모델
class Choose_val_Model(Base):
    __tablename__ = "choose_val"
    choose_id = Column(Integer, primary_key=True, index=True)
    high_loc = Column(String(100))
    low_loc = Column(String(100))
    theme1 = Column(String(100))
    theme2 = Column(String(100))
    theme3 = Column(String(100))
    theme4 = Column(String(100))
    days = Column(Integer)
    regdate = Column(DateTime, default=datetime.now)
    uptdate = Column(DateTime, default=datetime.now, onupdate=datetime.now)
"""유찬우 끝"""