from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import mariadb

"""
DB 설정 파이썬 파일
유찬우 만듦
"""
# MariaDB 연결 설정
SQLALCHEMY_DATABASE_URL = "mariadb+mariadbconnector://4team:4444@192.168.0.46:3306/sodam" #?charset=utf8mb4
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=5, # 데이터베이스 연결 풀의 기본 크기 (5명이 동시에 사용 가능)
    max_overflow=10, # 최대 초과 연결 수 (10명이 더 사용 가능)
    pool_timeout=30, # 연결 풀에서 대기 시간 (30초)
    pool_recycle=1800 # 연결 풀에서 재사용 가능한 최대 시간 (1800초 = 30분)
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 데이터베이스 연결 풀 생성
# autocommit=False : 자동 커밋 비활성화
# autoflush=False : 자동 플러시 비활성화
# bind=engine : 엔진에 바인딩된 세션 매이커 생성

# SQLAlchemy 모델의 기본 클래스
Base = declarative_base()

# 의존성 주입을 위한 DB 세션 생성기
def get_db():
    db = SessionLocal()
    try:
        yield db # yield : 함수를 종료하지 않고 값을 반환 (return은 종료하면서 반환)
    finally:
        db.close()