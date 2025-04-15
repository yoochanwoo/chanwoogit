from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastAPIDBTest.app.schema.choose_val_schema import ChoogeValCreate, ChoogeValResponse
from fastAPIDBTest.app.service import choose_val_service
from fastAPIDBTest.choose_val_main import SessionLocal
from typing import List

router = APIRouter(
    prefix="/choose_val",
    tags=["choose_val"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db # yield : 함수를 종료하지 않고 값을 반환 (return은 종료하면서 반환)
    finally:
        db.close()

@router.post("")
def add_choose_val(choose_val: ChoogeValCreate, db: Session = Depends(get_db)):
    return choose_val_service.create_choose_val(db=db, choose_val=choose_val)

# 전체 조회
@router.get("s", response_model=List[ChoogeValResponse])
def read_students(db: Session = Depends(get_db)):
    return choose_val_service.get_all_choose_vals(db)

# 단일 조회
@router.get("/{choose_val_id}", response_model=ChoogeValResponse)
def read_student(student_id: int, db: Session = Depends(get_db)):
    return choose_val_service.get_choose_val_by_id(db, student_id)

# 수정
@router.put("/{choose_val_id}", response_model=ChoogeValResponse)
def update_student(student_id: int, student: ChoogeValCreate, db: Session = Depends(get_db)):
    return choose_val_service.update_choose_val(db, student_id, student)

# 삭제
@router.delete("/{choose_val_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    return choose_val_service.delete_choose_val(db, student_id)