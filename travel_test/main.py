from fastapi import FastAPI
from fastapi.security.api_key import APIKeyHeader
import uvicorn

app = FastAPI()

# API 키를 헤더로 받기
API_KEY = "dfa91f8eb21d3d8ae4cb4b9adc06de5a"
API_KEY_NAME = "kakao_map-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# 인증이 필요 없는 엔드포인트
@app.get("/public")
async def public_route():
    return {"message": "This is a public route, no API key required."}

# FAST 실행명령어 자동 실행
if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8888, reload=True)
