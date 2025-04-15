from fastapi import FastAPI
from travelTest03.app.api.router import router

app = FastAPI(title="Travel Recommendation API")

# 라우터 등록
app.include_router(router, prefix="/api/v1", tags=["travel"])