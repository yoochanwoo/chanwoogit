from pydantic import BaseModel
from typing import List

class TravelRequest(BaseModel):
    travel_spots: List[str]
    days: int

class TravelResponse(BaseModel):
    recommendations: str