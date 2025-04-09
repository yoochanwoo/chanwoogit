import pandas as pd
import numpy as np
from ncf import TravelRecommender # 훈련모델을 정리한 클래스
from tensorflow.keras.preprocessing.sequence import pad_sequences # 리스트 데이터(여행목적) 패딩시에 사용
from sklearn.preprocessing import LabelEncoder # 위치아이디 인코딩에 사용
from sklearn.metrics import mean_absolute_error, root_mean_squared_error # 예측결과 평가에 사용

# ------ 데이터 호출 -------- 
df = pd.read_csv('train_dataset/train_travel_F.csv')  # 훈련에 사용할 데이터 호출
df_val = pd.read_csv('test_dataset/test_travel_F.csv')  # 평가에 사용할 데이터 호출

# 필드:
# df['위치ID']          → 여행지 ID (int)
# df['여행목적']        → 목적 ID의 리스트 (list[int])
# df['여행일수']        → 여행일자 (int)
# df['만족도']          → 평점 (1~5 float or int)

# --------- 전처리 ---------

# 여행목적을 리스트로 처리
df['여행목적리스트'] = df['여행목적'].str.split(';').apply(lambda lst: [int(x) for x in lst])
df_val['여행목적리스트'] = df_val['여행목적'].str.split(';').apply(lambda lst: [int(x) for x in lst])

# 여행목적은 리스트니까 padding 필요
purpose_seqs = pad_sequences(df['여행목적리스트'], padding='post')  # 2D numpy array
purpose_seqs_val = pad_sequences(df_val['여행목적리스트'], padding='post')  # 2D numpy array

# 위치아이디값은 매우 크기에 겹치지 않는 값으로 인코딩
le = LabelEncoder()
df['위치ID_encoded'] = le.fit_transform(df['위치ID'])
df_val['위치ID_encoded'] = le.fit_transform(df_val['위치ID'])
# 예측시에 다시 디코딩
# original_id = le.inverse_transform(['''결과로 나온 여행지 인코딩값'''])[0]

# 훈련용 데이터
place_ids = df['위치ID_encoded'].values.astype(np.int32)
days = df['여행일수'].values.astype(np.float32)
ratings = df['만족도'].values.astype(np.float32)

# 평가용 데이터
X_val_place = df_val['위치ID_encoded'].values.astype(np.int32)
X_val_purpose = purpose_seqs_val
X_val_days = df_val['여행일수'].values.astype(np.float32)
y_true = df_val['만족도'].values.astype(np.float32)

# --------- 모델 생성 ---------
NUM_PLACES = df['위치ID_encoded'].max() + 1
NUM_PURPOSES = max([max(p) for p in df['여행목적리스트']]) + 1  # 모든 목적 태그 중 최댓값

model = TravelRecommender(num_places=NUM_PLACES, num_purpose_tags=NUM_PURPOSES, embedding_dim=32)
model.load_model("model/travel_model_F.h5") # 모델 호출

# 예측 수행
y_pred = model.predict([X_val_place, X_val_purpose, X_val_days]).flatten()

mae = mean_absolute_error(y_true, y_pred)
rmse = root_mean_squared_error(y_true, y_pred)

print(f"MAE:  {mae:.4f}")
print(f"RMSE: {rmse:.4f}")

for i in range(5):
    print(f"실제 평점: {y_true[i]}, 예측 평점: {y_pred[i]:.2f}")

def recommend_places_by_region(model, df, region_code_prefix, selected_purposes, selected_days, top_n=5):
    # 1. 지역 필터링
    """
    region_code_prefix: int 또는 str, 예: 11 → 11로 시작하는 모든 지역 포함
    """
    region_code_prefix = str(region_code_prefix)
    region_df = df[df['지역코드'].astype(str).str.startswith(region_code_prefix)].copy()
    # .startswith : 해당 글자로 시작하는 데이터
    """
    리스트로 한다면,
    region_code_list: List[int] 또는 List[str] - 예: [23050, 23052] → 청주시, 제천시

    region_code_list = [str(code) for code in region_code_list]
    region_df = df[df['region_code'].astype(str).isin(region_code_list)].copy()
    """

    if region_df.empty:
        return [], []

    # 목적 리스트를 동일하게 넣음
    purpose_input = pad_sequences([selected_purposes] * len(region_df), maxlen=3)
    days_input = np.full(len(region_df), selected_days, dtype=np.float32)
    place_input = region_df['위치ID_encoded'].values

    # 3. 예측
    preds = model.predict([place_input, purpose_input, days_input])

    # 4. 상위 추천
    top_indices = preds.flatten().argsort()[::-1][:top_n]
    recommended = region_df.iloc[top_indices]

    return recommended[['위치명', '지역코드', '만족도']], preds[top_indices]

sgg = 42
purposes = [8]
day = 2

reco = recommend_places_by_region(model, df, sgg, purposes, day, top_n=5)
print(reco)