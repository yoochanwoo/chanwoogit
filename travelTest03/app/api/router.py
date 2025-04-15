from fastapi import APIRouter, HTTPException
from app.services.travel_service import TravelService
from app.models.travel import TravelRequest, TravelResponse

travel_router = APIRouter(prefix="/chat", tags=["chat"])

# 서비스 의존성 주입
def get_travel_service():
    return TravelService()

@travel_router.post("/recommend_travel", response_model=TravelResponse)
async def recommend_travel(
    request: TravelRequest,
    service: TravelService = Depends(get_travel_service)
):
    recommendations = service.get_travel_recommendations(
        request.travel_spots,
        request.days
    )
    return TravelResponse(recommendations=recommendations)