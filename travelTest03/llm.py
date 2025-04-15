from fastapi import FastAPI
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = FastAPI()

class TravelService:
    def __init__(self):
        self.model_name = "google/gemma-3b-it"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)

    def _create_prompt(self, travel_spots: list, days: int) -> str:
        if days == 1:
            return f"""여행 전문가로서 다음 여행지 목록에서 성격이 겹치지 않고 서로 너무 멀지 않은 5개의 여행지를 추천해주세요:
            여행지 목록: {travel_spots}
            추천 시 중복을 피하고 각 장소의 특징을 간단히 설명해주세요."""
        elif days == 2:
            return f"""여행 전문가로서 다음 여행지 목록에서 성격이 겹치지 않고 서로 너무 멀지 않은 10개의 여행지와 1개의 숙소를 추천해주세요:
            여행지 목록: {travel_spots}
            추천 시 중복을 피하고 각 장소의 특징을 간단히 설명하며, 숙소는 여행 동선을 고려하여 선택해주세요."""
        else:  # days == 3
            return f"""여행 전문가로서 다음 여행지 목록에서 성격이 겹치지 않고 서로 너무 멀지 않은 15개의 여행지와 1-2개의 숙소를 추천해주세요:
            여행지 목록: {travel_spots}
            추천 시 중복을 피하고 각 장소의 특징을 간단히 설명하며, 숙소는 여행 동선을 고려하여 선택해주세요."""

    def get_travel_recommendations(self, travel_spots: list, days: int) -> str:
        prompt = self._create_prompt(travel_spots, days)
        
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(
            **inputs,
            max_length=1000,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

# 서비스 인스턴스 생성
travel_service = TravelService()

@app.post("/recommend_travel")
async def recommend_travel(travel_spots: list, days: int):
    recommendations = travel_service.get_travel_recommendations(travel_spots, days)
    return {"recommendations": recommendations}
