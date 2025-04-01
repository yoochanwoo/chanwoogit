from transformers import pipeline

pipe = pipeline("text-generation", model="keelezibel/korea-travelguide-vicuna-13b")

pipe("강원도 여행지 추천")