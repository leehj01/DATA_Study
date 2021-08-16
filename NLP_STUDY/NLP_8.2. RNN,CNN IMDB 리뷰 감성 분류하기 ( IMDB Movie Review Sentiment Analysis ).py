# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.7.1
#   kernelspec:
#     display_name: PythonWithData 3
#     language: python
#     name: python3
# ---

# # IMDB 리뷰 감성 분류하기 ( IMDB Movie Review Sentiment Analysis )
# - https://wikidocs.net/24586 을 참고하며 공부함 

# ## 1. IMDB리뷰 데이터 이해

# %matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.datasets import imdb  # 데이터 불러오기

# 영화 리뷰는 x_train, 감성정보는 y_train에 저장됨 
(X_train, y_train), (
X_test, y_test) = imdb.load_data()  # load_data(num_word = 10000) 이면 등장 빈도 순위에따라서 단어 집합 크기를 제한할 수 있다.

print('훈련용 리뷰 개수 : {}'.format(len(X_train)))
print('테스트용 리뷰 개수 : {}'.format(len(X_test)))
num_classes = max(y_train) + 1
print('카테고리 : {}'.format(num_classes))

# datasets 에 있는 것은 이미, 토큰화와 정수 인코딩 - 전처리가 끝난 상태로 들어가 있다. 
# 등장 빈도에 따라서, 인덱스를 부여했기 때문에, 숫자가 낮을 수록 데이터 등장 빈도순위가 높다. 
print(X_train[0])
print(y_train[0])

# +
# 훈련용 리뷰의 길이는 다 다르다.
len_result = [len(s) for s in X_train]

print('리뷰의 최대 길이 : {}'.format(np.max(len_result)))
print('리뷰틔 평균 길이 : {}'.format(np.mean(len_result)))

plt.subplot(1, 2, 1)
plt.boxplot(len_result)
plt.subplot(1, 2, 2)
plt.hist(len_result, bins=50)
plt.show()

# 대체적으로 1000이하의 길이를가지며, 100~ 500 길이를 가진 데이터가 많다. 

# +
unique_elements, counts_elements = np.unique(y_train, return_counts=True)
print('각 레이블에 대한 빈도수')
print(np.asarray((unique_elements, counts_elements)))

# 25000개의 리뷰가 존재하는데, 두 레이블 0과 1은 각각 12500개로 균등한 분포를 가지고 있다.
# Unique에 대한  내용 https://www.notion.so/Numpy-d5a081b423244da4acddf669f286d8d1
# -

# #### x_train에 들어있는 숫자들이 각각 어떤 단어들을 나타내고 있는지 확인 
# - imbd.get_word_index()에는 각 단어와 맵핑되는 정수가 저장되어있음. 저장된 값에 +3을 해야 실제 맵핑되는 정수 ( imdb리뷰 데이터셋에서 정한 규칙 )

word_to_index = imdb.get_word_index()
index_to_word = {}
for key, value in word_to_index.items():
    index_to_word[value + 3] = key

print('빈도수 상위 1등 단어 : {}'.format(index_to_word[4]))
print('빈도수 상위 100등 단어 : {}'.format(index_to_word[104]))
# 0,1,2,3 특별 토큰으로, 취급

# +
# x_trian[0]이 인덱스로 바뀌기전에 어떤 단어였는지 확인
for index, token in enumerate(("<pad>", "<sos>", "<unk>")):
    index_to_word[index] = token

print(' '.join([index_to_word[index] for index in X_train[0]]))
# -

# ## LSTM으로 IMDB리뷰 감성 분석하기

import re
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.models import load_model

# +
## 데이터 셋 준비
# 단어의 집합의 크기를 10,000dmfh wpgks
vocab_size = 10000
(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=vocab_size)

# 리뷰 최대 길이는 500으로 제한
max_len = 500
X_train = pad_sequences(X_train, maxlen=max_len)
X_test = pad_sequences(X_test, maxlen=max_len)

"""
pad_sequences : 리뷰의 문장의 길이가 다르기 때문에, 모델이 처리할 수 있도록 길이를 같게 해줄때 사용 .
max_len에 넣는 값으로  길이가 정해지는데,  훈련 데이터가 정한 길이를 초과하면 초과분을 삭제하고, 부족하면 0으로 채운다.
padding='pre'가 기본이기 때문에 앞에 0 이 생긴다. 
"""

## 학습 환경 정의
model = Sequential()
model.add(Embedding(vocab_size, 100))
model.add(LSTM(128))
model.add(Dense(1, activation='sigmoid'))

"""
Embedding( a, b) : 두가지 인자를 받음, a : 단어 집합의 크기, b : 임베딩 후의 벡터의 크기 - 입력단어는 b차원의 임베딩 벡터로 표현됨
"""

es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4)
"""
검증 데이터의 손실이 증가하면, 과적합 징후이므로, 4회 증가하면 학습을 중단하는 earlystopping 사용
"""

mc = ModelCheckpoint('IMDB_model.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)
"""
검증 데이터의 정확도가 이전보다 좋아질 경우만 모델을 저장함.
"""

## 훈련
model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
history = model.fit(X_train, y_train, epochs=4, callbacks=[es, mc], batch_size=60, validation_split=0.2)
"""
긍/부정 판단을 위해 손실함수 binary_crossentropy 사용하며, 최적화함수는 rmsprop사용 . 
에포크마다 정확도를 구하기 위해 accuracy 추가 
historyd에 validation_split을 주어서, 훈련데이터 20%을 검증데이터로 나눔"""
# -

## 테스트 데이터에 대해서 정확도 평가
loaded_model = load_model('IMDB_model.h5')
print('테스트 정확도 :{}'.format(loaded_model.evaluate(X_test, y_test)[1]))

## 에포크마다 변화하는 훈련 데이터와 검증데이터의 손실을 시각화 함.
epochs = range(1, len(history.history['acc']) + 1)
plt.plot(epochs, history.history['loss'])
plt.plot(epochs, history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()


# +
## 임의의 문장에 대해서 리뷰의 긍/부정 예측

def sentiment_predict(new_sentence):
    # 알파벳과 숫자를 제외하고 모두 제거 및 알파벳 소문자화
    new_sentence = re.sub('[^0-9a-zA-Z ]', '', new_sentence).lower()

    # 정수 인코딩
    encoded = []
    for word in new_sentence.split():
        # 단어 집합의 크기를 10,000dmfh wpgks
        try:
            if word_to_index[word] <= 1000:
                encoded.append(word_to_index[word] + 3)
            else:
                # 10,000 이상의 숫자는 <unk>xhzmsdmfh cnlrmq
                encoded.append(2)
        # 단어 집합에 없는 단어는 <unk>토큰으로 취key
        except KeyError:
            encoded.append(2)

    pad_new = pad_sequences([encoded], maxlen=max_len)  # 패딩
    score = float(loaded_model.predict(pad_new))  # 예측

    if (score > 0.5):
        print('{}% 확률로 긍정 리뷰입니다.'.format(score * 100))
    else:
        print('{}% 확률로 부정 리뷰입니다.'.format(score * 100))


# +
temp_str = "This movie was just way too overrated. The fighting was not professional and in slow motion. I was expecting more from a 200 million budget movie. The little sister of T.Challa was just trying too hard to be funny. The story was really dumb as well. Don't watch this movie if you are going because others say its great unless you are a Black Panther fan or Marvels fan."

sentiment_predict(temp_str)

# +
temp_str = " I was lucky enough to be included in the group to see the advanced screening in Melbourne on the 15th of April, 2012. And, firstly, I need to say a big thank-you to Disney and Marvel Studios. \
Now, the film... how can I even begin to explain how I feel about this film? It is, as the title of this review says a 'comic book triumph'. I went into the film with very, very high expectations and I was not disappointed. \
Seeing Joss Whedon's direction and envisioning of the film come to life on the big screen is perfect. The script is amazingly detailed and laced with sharp wit a humor. The special effects are literally mind-blowing and the action scenes are both hard-hitting and beautifully choreographed."

sentiment_predict(temp_str)
# -
# ## 1D CNN으로 IMDB리뷰 분류하기


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Dropout, Conv1D, GlobalAveragePooling1D, Dense
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.models import load_model

embedding_size = 256
batch_size = 256

# 모델 설계
"""
1D합성곱 연산을 수행하되, 커널수는 256 , 커널의 크기느 3을 사용. 두개의 밀집층으로 은닉층과 출력층 설계
"""
model = Sequential()
model.add(Embedding(vocab_size, 256))
model.add(Dropout(0.3))
model.add(Conv1D(256, 3, padding='valid', activation='relu'))
model.add(GlobalAveragePooling1D())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

# +
es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=3)
mc = ModelCheckpoint('CNN_MODEL.h5', monitor='val_acc', mode='max', verbose=1, save_best_only=True)

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
history = model.fit(X_train, y_train, epochs=20, validation_data=(X_test, y_test), callbacks=[es, mc])
# -

loaded_model = load_model('CNN_MODEL.h5')
print('테스트 정확도 : {}'.format(loaded_model.evaluate(X_test, y_test)[1]))

# +
temp_str = "This movie was just way too overrated. The fighting was not professional and in slow motion. I was expecting more from a 200 million budget movie. The little sister of T.Challa was just trying too hard to be funny. The story was really dumb as well. Don't watch this movie if you are going because others say its great unless you are a Black Panther fan or Marvels fan."

sentiment_predict(temp_str)

# +
temp_str = " I was lucky enough to be included in the group to see the advanced screening in Melbourne on the 15th of April, 2012. And, firstly, I need to say a big thank-you to Disney and Marvel Studios. \
Now, the film... how can I even begin to explain how I feel about this film? It is, as the title of this review says a 'comic book triumph'. I went into the film with very, very high expectations and I was not disappointed. \
Seeing Joss Whedon's direction and envisioning of the film come to life on the big screen is perfect. The script is amazingly detailed and laced with sharp wit a humor. The special effects are literally mind-blowing and the action scenes are both hard-hitting and beautifully choreographed."

sentiment_predict(temp_str)
# -

## 에포크마다 변화하는 훈련 데이터와 검증데이터의 손실을 시각화 함.
epochs = range(1, len(history.history['acc']) + 1)
plt.plot(epochs, history.history['loss'])
plt.plot(epochs, history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
