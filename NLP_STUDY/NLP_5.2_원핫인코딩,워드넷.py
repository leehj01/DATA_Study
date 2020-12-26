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
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# ## 원핫인코딩 함수 구현

from konlpy.tag import Okt
okt = Okt()
token = okt.morphs("나는 사과를 좋아한다")
print(token)

# 각 토큰에 대한 고유한 인텍스 부여 ( 빈도수대로 정렬하기도 함 )
word2index = {}
for i in token :
    if i not in word2index.keys():
        word2index[i] = len(word2index)
print(word2index)


# 원핫 인코딩 함수
def one_hot_encoding(word, word2index):
    one_hot_vector = [0]*(len(word2index))
    index  = word2index[word]
    one_hot_vector[index] = 1
    return one_hot_vector


one_hot_encoding('사과', word2index)

# ## 케라스(Keras)를 이용한 원핫 인코딩

# +
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical

text = "오늘은 파스타랑 감바스를 만들었는데 맛이 그냥 그랬다"

# 정수 인코딩 
token = Tokenizer()
token.fit_on_texts([text])
print(token.word_index)

# +
encoded = token.texts_to_sequences([text])
print(encoded)

one_hot= to_categorical(encoded)
print(one_hot)
# -

# ## 워드넷을 활용한 단어간 유사도 비교
# - 원핫 벡터로는 단어간의 계층적 구조라는 특징을 잘 반영할 수 없기 때문에, 잘 구축되어진 데이터 베이스를 이용한다. 그럿을 '시소러스(어휘분류사전)이라고 부르는데 그 중 대표적인 것이 '워드넷'이 있다.

import nltk
nltk.download('wordnet')

# +
from nltk.corpus import wordnet as wn

def hypernyms(word):
    current_node = wn.synsets(word)[0]
    yield current_node
    
    while True :
        try :
            current_node = current_node.hypernyms()[0]
            yield current_node
            
        except IndexError :
            break
            
for h in hypernyms('student'):
    print(h)
# -

[h for h in hypernyms('student')]

wn.synsets('student')


# +
def distance(word1, word2):
    word1_hypernyms = [h for h in hypernyms(word1)]
    
    for i, word2_hypernym in enumerate(hypernyms(word2)):
        try:
            return i + word1_hypernyms.index(word2_hypernym)
        except ValueError:
            continue

distance('dog', 'cat')

# +
import numpy as np

def similarity(word1, word2):
    return -np.log(distance(word1, word2))

print(similarity('dog', 'student'))
print(similarity('dog', 'cat'))
# -


