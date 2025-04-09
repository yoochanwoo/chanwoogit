import tensorflow as tf

class TravelRecommender(tf.keras.Model):
    def __init__(self, num_places, num_purpose_tags, embedding_dim=32):
        super().__init__()
        self.place_embedding = tf.keras.layers.Embedding(num_places, embedding_dim)
        self.purpose_embedding = tf.keras.layers.Embedding(num_purpose_tags, embedding_dim)
        
        self.day_dense = tf.keras.layers.Dense(embedding_dim)  # 여행일자 (숫자형)
        #self.mlp = tf.keras.Sequential([
        #    tf.keras.layers.Dense(128, activation='relu'),
        #    tf.keras.layers.Dense(64, activation='relu'),
        #    tf.keras.layers.Dense(1)  # 예측 평점
        #])
        self.mlp = tf.keras.Sequential([
            tf.keras.layers.Dense(256, activation='relu'),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(1)
        ])
        
    def call(self, inputs):
        place_id, purpose_ids, days = inputs

        place_vec = self.place_embedding(place_id)

        # 목적은 여러 개 → 평균 or 합산
        purpose_vec = tf.reduce_mean(self.purpose_embedding(purpose_ids), axis=1)

        days_vec = self.day_dense(tf.expand_dims(days, -1))  # 일자 숫자 → 벡터화

        combined = tf.concat([place_vec, purpose_vec, days_vec], axis=-1)
        output = self.mlp(combined)
        return output
    
    def save_model(self, path='travel_recommender_model.h5'):
        if self.mlp is not None:
            self.mlp.save(path)
            print(f"✅ 모델이 '{path}'로 저장되었습니다.")
        else:
            print("❌ 저장할 모델이 없습니다.")
            
    def load_model(self, path='travel_recommender_model.h5'):
        self.mlp = tf.keras.models.load_model(path)
        print(f"✅ 모델이 '{path}'에서 불러와졌습니다.")
