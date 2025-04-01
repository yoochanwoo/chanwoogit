import uvicorn
from fastapi import FastAPI
from app.routers import ycw3_router1

app = FastAPI(title="Chatbot API", description="자상하고 비전문적인 조언 서비스")

app.include_router(ycw3_router1.router)

@app.get("/")
async def root():
    return {"message": "Chatbot API Running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)