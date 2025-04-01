import requests

class OllamaService:
    def __init__(self, model="gemma3:4b"):
        self.base_url = "http://localhost:11434/api/generate"
        self.model = model
        self.chatbot_role = "너는 항상 민간요법에 기반된 비과학적인 대답을 해. 질문에 대한 답은 한글만을 사용하여 3줄 이내로 짧게해줘."

    def generate_response(self, prompt):
        payload = {
            "model": self.model,
            "prompt": self.chatbot_role + prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.base_url, json=payload)
            response.raise_for_status()
            return response.json()['response']
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ollama API 호출 중 오류: {e}")