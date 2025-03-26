import numpy as np
import tensorflow as tf
import streamlit as st
from PIL import Image
from tensorflow.keras.models import load_model

# 데이터 준비
@st.cache_data # 함수의 입력 매개변수와 반환 값을 캐시에 저장하여 호출 시 재사용
def load_data():

    model_path = './model/Alzheimer_model3_2.h5'  # 저장된 모델 경로
    loaded_model = load_model(model_path)
    #print("저장된 모델이 성공적으로 로드되었습니다.")
    return loaded_model

cnn_model = load_data()
img_height = 128
img_width = 128

# 4. streamlit UI 구현
st.title("알츠하이머 여부 예측 시스템")
st.write('MRI 사진을 업로드하여 알츠하이머 여부를 예측해보세요')

# 파일 업로드 위젯
uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "png", "jpeg"])

# 저장된 모델을 활용한 이미지 예측 함수
def predict_flower_with_loaded_model(file, model, class_names):
    
    # 이미지 로드 및 전처리
    img = Image.open(file).convert("RGB")
    img = img.resize((img_height,img_width))
    
    img_array = tf.keras.preprocessing.image.img_to_array(img) # 배열형태로 변환
    
    img_array = tf.expand_dims(img_array, 0)  # 배치 차원 추가

    # 예측 수행
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    # 이미지 시각화
    st.image(img, caption="업로드 된 이미지", use_column_width=True)
    st.write(
        "이 이미지는 '{}' ({:.2f}% 확률) 입니다."
        .format(class_names[np.argmax(score)], 100 * np.max(score)))

# 예측하기 버튼
if st.button('예측하기'):
    predict_flower_with_loaded_model(uploaded_file, cnn_model, ['Mild Impairment', 'Moderate Impairment', 'No Impairment', 'Very Mild Impairment'])

