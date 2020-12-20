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

# # 08. Transformer

# +
import random
import numpy as np
import tensorflow as tf
from konlpy.tag import Okt

from tensorflow.keras import Model
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Lambda, Layer, Embedding, LayerNormalization
# -

# %pwd

import os 
os.chdir('C:/Users/82102/Desktop/all/computer/fastcampus/deep/deep_part_3/DeepLearning')

EPOCHS = 200
NUM_WORDS = 2000


# ## Dot-Scaled Attention
# - 핵심적인 부분을 직접 구현

class DotScaledAttention(Layer):
    def __init__(self, d_emb, d_reduced, masked = False):  # word embbeding을 할 Dimension 이랑 Dimension을 줄여서 사용할 건데, 
        #줄여서 사용할 reduced_Dimension을  받을 것 
        
        super().__init__()
        self.q = Dense(d_reduced, input_shape = (-1, d_emb))  # -1은 배치에 따라서 다름. 값을 받아서, reduced 해준다.
        self.k = Dense(d_reduced, input_shape = (-1, d_emb))  # 쿼리, 키 , 벨류를 선어내줌
        self.v = Dense(d_reduced, input_shape = (-1, d_emb))
        self.scale = Lambda(lambda x: x/np.sqrt(d_reduced))  # 논문에는 dk로 되어있는 것 
        self.masked = masked
    
    
    def call(self, x, training = None, mask = None): # ( Q, K , V)
        q = self.scale(self.q(x[0]))
        k = self.k(x[1])
        v = self.k(x[2])
        
        k_T = tf.transpose(k, perm = [0,2,1]) # 배치는 그대로 유지하데 transepose하라는 의미
        comp = tf.matmul(q, k_t)  # 쿼리와 key값을 비교해준다. compare해준다.
        
        # compare 결과를 softmax하기 전에, 
        
        # self attention을 할때, 미래시는 참조 안되고 과거시만 참조할 수 있는데, 그걸 구현해 놓은 것 
        if self.masked: # Referrend from https://github.com/LastRemote/Transformer - TF2.0
            length = tf.shape(comp)[-1]
            mask = tf.fill((length, length), -np.inf) # 미래시를 참조하는 것은 -np.inf을 넣어주고,  -> -inf 을 넣어주면 softmax를 사용하면 자연스럽게 값이 0 이됨 
            mask  = tf.linalg.band_part(mask, 0, -1) # ger upper triangle  # 그렇지 않으면 0 으로 넣어줌 
            mask = tf.linalg.set_diag(mask, tf.zeros((length))) # Set diagonal to zeros to avoid operations with infinity
            
        pass


# ## Multi-Head Attention
# - dot-scaled를 기반으로 빌드를 해줌 

class MultiHeadAttention(Layer):
    def __init__(self, num_head, d_emb, d_reduced, masked = False):
        


# ## 데이터 셋 준비

# +
# dataset 
d_file = 'chatbot_data.csv' # 출처  : ai허브
okt = Okt()

with open(d_file, 'r', encoding = 'utf-8-sig') as file :
    lines = file.readlines()
    seq = [' '.join(okt.morphs(line)) for line in lines] # 줄을 한줄 한줄을 형태소 분석을 해줌 
    # 스페이스를 기준으로 단어를 나누어주기 때문에, ' ' 를함 
    

# 질문과 답변을 나누어줌 
questions = seq[::2] # 데이터 셋을 보면 질문은 홀수 줄에 있고 ( 0번부터 가져옴 )
answers  = ['\t' + lines for lines in seq[1::2]] # 대답은 짝수 줄에 있다 
# 앞에는 tab을 입력해줌 (\t) 그 이유는 나중에 이것을 sos로 사용 하기 위함 
# new line 을 eos로 사용할 것

num_sample = len(questions) # 전체 길이 파악
print(num_sample)

# 데이터가 편향된 상태로 있을 수 있기 때문에 데이터를 섞어줌 
perm = list(range(num_sample))
random.seed(0)
random.shuffle(perm)

train_q = list()
train_a = list()
test_q = list()
test_a = list()

for idx, qna in enumerate(zip(questions, answers)):
    q, a = qna
    if perm[idx] > num_sample//5: # 섞어준것의 4/5를 train에 넣어주고
        train_q.append(q)
        train_a.append(a)   # 또다시, 질문과 답을 나눈다 .
        
    else : # 그 외의 것을 test에 넣어줌 
        test_q.append(q)
        test_a.append(a)
            
tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=NUM_WORDS, # 단어 빈도에 따른 사용할 단어 개수의 최대값. 가장 빈번하게 사용되는 num_words개의 단어만 보존합니다.
                                                 filters ='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~')
# keras에 있는 전처리함수로 토크나이즈를 해줌
# 토크나이즈 : 각 단어들을 숫자로 바꿔주는 것을 의미함 
# filter 에 들어있는 것은 다 제거 됨 tqp과 \n을 제외하고 filter을 해줌 

tokenizer.fit_on_texts(train_q + train_a) # 질문과 답변에 대해서 fitting을 해줌 

# text로 되어있는 것을 sequence 로 - 숫자로 된 단어 나열이라고 보면 됨 

train_q_seq = tokenizer.texts_to_sequences(train_q)
train_a_seq = tokenizer.texts_to_sequences(train_a)

test_q_seq = tokenizer.texts_to_sequences(test_q)
test_a_seq = tokenizer.texts_to_sequences(test_a)

# pad sequence를 이용해서 trian 과 test set을 만들어줌. 
# 출력에 대해서는 데이터를 앞쪽으로 정렬을 해줘야하기 때문에 제로 패딩을 뒤쪽으로 해줘야함 
# 출력의 maxlen 을 65로 한 이유는 65길이를 해서 앞에 지우고 / 뒤에 지워서 결국 64길이로 사용됨. 
x_train = tf.keras.preprocessing.sequence.pad_sequences(train_q_seq,
                                                       value = 0,
                                                       padding = 'pre',
                                                       maxlen = 64)

y_train = tf.keras.preprocessing.sequence.pad_sequences(train_a_seq,
                                                       value = 0,
                                                       padding = 'post',
                                                       maxlen = 65)

# 이것만 추가됨 
y_train_shifted = np.concatenate([np.zeros((y_train.shpae[0],1)), y_train[:, 1:]], axis = )




x_test = tf.keras.preprocessing.sequence.pad_sequences(test_q_seq,
                                                       value = 0,
                                                       padding = 'pre',
                                                       maxlen = 64)
y_test = tf.keras.preprocessing.sequence.pad_sequences(test_a_seq,
                                                       value = 0,
                                                       padding = 'post',
                                                       maxlen = 65)

train_ds = tf.data.Dataset.from_tensor_slices((x_train, y_train)).shuffle(10000).batch(32).prefetch(1024)
test_ds = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(1).prefetch(1024)
