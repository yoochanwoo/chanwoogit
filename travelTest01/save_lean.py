import pandas as pd
import numpy as np
from ncf import TravelRecommender # 훈련모델을 정리한 클래스
from tensorflow.keras.preprocessing.sequence import pad_sequences # 리스트 데이터(여행목적) 패딩시에 사용
from tensorflow.keras.callbacks import EarlyStopping # callback함수
from sklearn.preprocessing import LabelEncoder # 위치아이디 인코딩에 사용
from sklearn.metrics import mean_absolute_error, root_mean_squared_error # 예측결과 평가에 사용
import matplotlib.pyplot as plt

# ------ 데이터 호출 -------- 
df = pd.read_csv('train_dataset/train_travel_A.csv')  # 훈련에 사용할 데이터 호출
df_val = pd.read_csv('test_dataset/test_travel_A.csv')  # 평가에 사용할 데이터 호출

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
model.compile(optimizer='adam', loss='mse', metrics=['mae'])

early_stop = EarlyStopping(
    monitor='val_loss',         # 검증 손실 기준
    patience=8,                 # 7번 연속 좋아지지 않으면 종료
    restore_best_weights=True,  #  가장 좋은 성능을 보였던 모델의 가중치(weights)를 복원
    verbose=1                   # 중단 시 메시지 출력
)

# --------- 모델 학습 ---------
history = model.fit(
    x=[place_ids, purpose_seqs, days],
    y=ratings,
    batch_size=128,
    epochs=100,
    callbacks=[early_stop],
    validation_split=0.1
)
model.save_model('./model/travel_model_A.h5')

# 예측 수행
y_pred = model.predict([X_val_place, X_val_purpose, X_val_days]).flatten()

mae = mean_absolute_error(y_true, y_pred)
rmse = root_mean_squared_error(y_true, y_pred)

print(f"MAE:  {mae:.4f}")
print(f"RMSE: {rmse:.4f}")

for i in range(5):
    print(f"실제 평점: {y_true[i]}, 예측 평점: {y_pred[i]:.2f}")

# 그래프 그리기
plt.figure(figsize=(10, 4))
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.title('Training & Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid()
plt.savefig("training_loss_curve_A.png")