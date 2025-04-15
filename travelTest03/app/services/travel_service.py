import requests

class TravelService:
    def __init__(self, model="gemma3:4b"):
        self.base_url = "http://localhost:11434/api/generate"
        self.model = model

    def _create_prompt(self, travel_spots: list, days: int) -> str:
        if days == 1:
            return f"""
            여행 전문가로서 다음 여행지 목록에서
            cat2가 겹치지 않고,
            x좌표(mapx)와 y좌표(mapy)를 보고
            서로 너무 멀지 않은 5개의 여행지를 판단하여 골라주세요:
            여행지 목록: {travel_spots}
            추천 시 중복을 피해주세요.
            대답은 받은 리스트의 형태를 유지하여 그대로 이어붙여 출력해주세요
            """
        elif days == 2:
            return f"""
            여행 전문가로서 다음 여행지 목록에서
            cat2가 겹치지 않고,
            x좌표(mapx)와 y좌표(mapy)를 보고
            서로 너무 멀지 않은 10개의 여행지와 1개의 숙소를 판단하여 골라주세요:
            여행지 목록: {travel_spots}
            추천 시 중복을 피하고,
            숙소는 여행 동선을 고려하여 선택해주세요.
            대답은 받은 리스트의 형태를 유지하여 그대로 이어붙여 출력해주세요
            """
        else:  # days == 3
            return f"""
            여행 전문가로서 다음 여행지 목록에서
            cat2가 겹치지 않고,
            x좌표(mapx)와 y좌표(mapy)를 보고
            서로 너무 멀지 않은 15개의 여행지와 1-2개의 숙소를 판단하여 골라주세요:
            여행지 목록: {travel_spots}
            추천 시 중복을 피하고,
            숙소는 여행 동선을 고려하여 선택해주세요.
            대답은 받은 리스트의 형태를 유지하여 그대로 이어붙여 출력해주세요
            """

    def get_travel_recommendations(self, travel_spots: list, days: int):
        prompt = self._create_prompt(travel_spots, days)
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.base_url, json=payload)
            response.raise_for_status()
            return response.json()['response']
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ollama API 호출 중 오류: {e}")