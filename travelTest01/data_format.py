import pandas as pd

## 데이터 셋 호출
travel_df = pd.read_csv('./dataset/tn_travel_B.csv')
loc_df = pd.read_csv('./dataset/tn_visit_area_info_B.csv')

# 필요 데이터 추출
travel_df = travel_df[['TRAVEL_ID', 'TRAVEL_START_YMD', 'TRAVEL_END_YMD', 'TRAVEL_MISSION_CHECK']]
loc_df = loc_df[['TRAVEL_ID', 'POI_ID', 'POI_NM', 'X_COORD', 'Y_COORD', 'DGSTFN', 'REVISIT_INTENTION', 'RCMDTN_INTENTION', 'SGG_CD']]

# ID 기준으로 병합
travelDF_f1 = pd.merge(loc_df,travel_df, on="TRAVEL_ID", how="left")

# ID 값 제거
travelDF_f1.drop(columns=['TRAVEL_ID'], inplace=True)

# 위치정보와 평점 기준으로 결측치 제거
travelDF_f1.dropna(subset=['SGG_CD', 'DGSTFN', 'REVISIT_INTENTION', 'RCMDTN_INTENTION'], inplace=True)

# 날짜 형식으로 변환
travelDF_f1['TRAVEL_END_YMD'] = pd.to_datetime(travelDF_f1['TRAVEL_END_YMD'])
travelDF_f1['TRAVEL_START_YMD'] = pd.to_datetime(travelDF_f1['TRAVEL_START_YMD'])

# 날짜 차이 남기고 날짜 데이터 날리기
travelDF_f1['여행일수'] = (travelDF_f1['TRAVEL_END_YMD'] - travelDF_f1['TRAVEL_START_YMD']).dt.days
travelDF_f1.drop(columns=['TRAVEL_START_YMD','TRAVEL_END_YMD'], inplace=True)

# 위치정보 필요부분만 남기기
travelDF_f1['SGG_CD'] = travelDF_f1['SGG_CD'].astype(str).str[:5].astype(float).astype(int)

# 평점 평균내기
travelDF_f1['평점'] = (travelDF_f1['DGSTFN'] + travelDF_f1['REVISIT_INTENTION'] + travelDF_f1['RCMDTN_INTENTION'])/3

# 평점 데이터만 남기기
travelDF_f1.drop(columns=['DGSTFN', 'REVISIT_INTENTION', 'RCMDTN_INTENTION'], inplace=True)

# 평점 데이터를 방문지 별로 통합하기
df_avg = travelDF_f1.groupby('POI_ID')['평점'].mean().reset_index()

# 기존 평점 제거
travelDF_f1.drop(columns=['평점'], inplace=True)

# 위치정보 기준으로 중복 데이터 제거
travelDF_f1.drop_duplicates(subset=['POI_ID'], inplace=True)

# 평균 평점 통합
travelDF_f1 = pd.merge(travelDF_f1, df_avg, on='POI_ID')

# 중복 데이터 제거
#travelDF_f1 = travelDF_f1.drop_duplicates()

# 미션값 리스트로
# travelDF_f1['TRAVEL_MISSION_CHECK'] = travelDF_f1['TRAVEL_MISSION_CHECK'].str.split(';')
# 전처리 부분에서 해야함
#print(travelDF_f1.head())

# 컬럼명 변경하고 순서 바꾸기
travelDF_f1 = travelDF_f1[['POI_ID', 'POI_NM','X_COORD','Y_COORD','SGG_CD','TRAVEL_MISSION_CHECK','여행일수','평점']]
travelDF_f1.columns = ['위치ID', '위치명','X좌표','Y좌표','지역코드','여행목적','여행일수','평점']

travelDF_f1.to_csv('./train_dataset/train_travel_B.csv', index=False)

