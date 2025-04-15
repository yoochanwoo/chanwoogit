from sqlalchemy import Column, Integer, VARCHAR, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from fastAPIDBTest.app.schema.choose_val_schema import ChooseValCreate
from fastapi import HTTPException

Base = declarative_base()

class choose_val_Model(Base):
    __tablename__ = "choose_val"
    chooge_id = Column(Integer, primary_key=True, index=True)
    high_loc = Column(VARCHAR(100))
    low_loc = Column(VARCHAR(100))
    theme1 = Column(VARCHAR(100))
    theme2 = Column(VARCHAR(100))
    theme3 = Column(VARCHAR(100))
    theme4 = Column(VARCHAR(100))
    days = Column(Integer)
    regdate = Column(DateTime, default=datetime.now)
    uptdate = Column(DateTime, default=datetime.now, onupdate=datetime.now)

# 생성
def create_choose_val(db: Session, choose_val: ChooseValCreate):
    db_choose_val = choose_val_Model(
        high_loc=choose_val.high_loc,
        low_loc=choose_val.low_loc,
        theme1=choose_val.theme1,
        theme2=choose_val.theme2,
        theme3=choose_val.theme3,
        theme4=choose_val.theme4,
        days=choose_val.days,
        regdate=datetime.now(),
        uptdate=datetime.now())
    db.add(db_choose_val)
    db.commit()
    db.refresh(db_choose_val)
    return db_choose_val

# 전체 조회
def get_all_choose_vals(db: Session):
    return db.query(choose_val_Model).all()

# 단일 조회
def get_choose_val_by_id(db: Session, chooge_id: int):
    choose_val = db.query(choose_val_Model).filter(choose_val_Model.chooge_id == chooge_id).first()
    if choose_val is None:
        raise HTTPException(status_code=404, detail="Choose_val not found")
    return choose_val

# 수정
def update_choose_val(db: Session, chooge_id: int, updated_data: ChooseValCreate):
    choose_val = db.query(choose_val_Model).filter(choose_val_Model.id == chooge_id).first()
    if choose_val is None:
        raise HTTPException(status_code=404, detail="Choose_val not found")

    choose_val.high_loc = updated_data.high_loc
    choose_val.low_loc = updated_data.low_loc
    choose_val.theme1 = updated_data.theme1
    choose_val.theme2 = updated_data.theme2
    choose_val.theme3 = updated_data.theme3
    choose_val.theme4 = updated_data.theme4
    choose_val.days = updated_data.days
    choose_val.uptdate = datetime.now()

    db.commit()
    db.refresh(choose_val)
    return choose_val

# 삭제
def delete_choose_val(db: Session, chooge_id: int):
    choose_val = db.query(choose_val_Model).filter(choose_val_Model.chooge_id == chooge_id).first()
    if choose_val is None:
        raise HTTPException(status_code=404, detail="Choose_val not found")

    db.delete(choose_val)
    db.commit()
    return {"message": f"Choose_val with id {chooge_id} has been deleted"}