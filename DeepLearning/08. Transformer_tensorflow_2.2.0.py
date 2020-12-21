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
    def __init__(self, d_emb, d_reduced, masked=False):  # word embbeding을 할 Dimension 이랑 Dimension을 줄여서 사용할 건데,
        # 줄여서 사용할 reduced_Dimension을  받을 것

        super().__init__()
        self.q = Dense(d_reduced, input_shape=(-1, d_emb))  # -1은 배치에 따라서 다름. 값을 받아서, reduced 해준다.
        self.k = Dense(d_reduced, input_shape=(-1, d_emb))  # 쿼리, 키 , 벨류를 선어내줌
        self.v = Dense(d_reduced, input_shape=(-1, d_emb))
        self.scale = Lambda(lambda x: x / np.sqrt(d_reduced))  # 논문에는 dk로 되어있는 것
        self.masked = masked

    def call(self, x, training=None, mask=None):  # ( Q, K , V)
        q = self.scale(self.q(x[0]))
        k = self.k(x[1])
        v = self.k(x[2])

        k_T = tf.transpose(k, perm=[0, 2, 1])  # 배치는 그대로 유지하데 transepose하라는 의미
        comp = tf.matmul(q, k_T)  # 쿼리와 key값을 비교해준다. compare해준다.

        # compare 결과를 softmax하기 전에, mask를 씌어줘야함

        # self attention을 할때, 미래시는 참조 안되고 과거시만 참조할 수 있는데, 그걸 구현해 놓은 것
        if self.masked:  # Referrend from https://github.com/LastRemote/Transformer - TF2.0
            length = tf.shape(comp)[-1]  # 컴페어의 shape를 보고 그거에 맞는 length의 사각형을 만들어서 사각형을 만들어주는 것
            mask = tf.fill((length, length),
                           -np.inf)  # 미래시를 참조하는 것은 -np.inf을 넣어주고,  -> -inf 을 넣어주면 softmax를 사용하면 자연스럽게 값이 0 이됨
            mask = tf.linalg.band_part(mask, 0, -1)  # ger upper triangle  # 그렇지 않으면 0 으로 넣어줌
            mask = tf.linalg.set_diag(mask,
                                      tf.zeros((length)))  # Set diagonal to zeros to avoid operations with infinity

            comp += mask  # comp의 결과가 어떻게 되든 마스크상 미래시라면 -inf 가 더해지게됨

        comp = tf.nn.softmax(comp, axis=-1)  # softmax를 쓰면 -inf 가 된 것은 0이 돔 -> weight를 만들게 됨

        return tf.matmul(comp, v)  # compare 결과와 v를 곱하게 됨


# ## Multi-Head Attention
# - dot-scaled를 기반으로 빌드를 해줌

class MultiHeadAttention(Layer):
    def __init__(self, num_head, d_emb, d_reduced, masked=False):  # head의 갯수
        super().__init__()

        self.attention_list = list()  # attention 을 list 해서 여러개 만들어줌
        for _ in range(num_head):  # head 갯수 만큼 만들어 줄것
            self.attention_list.append(DotScaledAttention(d_emb, d_reduced, masked))

        # 마지막 출력 전에 dense 함수가 필요함. 멀티해드 게산한 후에 컨캣 후에 해주는것
        self.linear = Dense(d_emb, input_shape=(-1, num_head * d_reduced))

    def call(self, x, training=None, mask=None):
        attention_list = [a(x) for a in self.attention_list]  # a 는 dotscaledattention 결과를 list로 받아옴
        # attention_list = [ a(x, training ) for a in self.attention_list] # 배치노멀라이제이션 등이 없어서 이건 안씀

        concat = tf.concat(attention_list, axis=-1)  # 리스트로 나온 결과를 concat 해줌

        return self.linear(concat)  # 리니어 함수를 통해 출력


# ## Encoder
# - init과 build를 따로 쓰는 이유는
# - init은 input을 아직 안받은 상태이이다. call을 할때, 그 인풋으로 만들어줌
# - build를 따로 구현해주면, input shape를 이용해서(아는 상태에서) build를 할 수있다.

class Encoder(Layer):
    def __init__(self, num_head, d_reduced):
        super().__init__()
        self.num_head = num_head
        self.d_r = d_reduced

    def build(self, input_shape):  # 필요한 레이어를 만들어주기
        self.multi_attention = MultiHeadAttention(self.num_head, input_shape[-1], self.d_r)
        # d_emb의 경우 입력이 들어오면 입력이 된 단어가 들어옴. 즉 inputshape 의 마지막자리가 임베딩의 크기이다.

        self.layer_norm1 = LayerNormalization(input_shape=input_shape)
        # 논문을 보면 layernormalizetion을 하고 dense를 두번하고 또 레이어 노멀라이제시션을 함

        self.dense1 = Dense(input_shape[-1] * 4, input_shape=input_shape, activation='relu')
        # 논문에 4배로 늘리는 것이 나와있음.

        self.dense2 = Dense(input_shape[-1],
                            input_shape=self.dense1.compute_output_shape(input_shape))
        # 하나는 activation 이 relu고 하나는 안들어가 있다. 출력이 들어가 있기 때문에 compute_output_shape를 이용함

        self.layer_norm2 = LayerNormalization(input_shape=input_shape)

        super().build(input_shape)

    def call(self, x, training=None, mask=None):
        h = self.multi_attention((x, x, x))  # 인코더에서는 셀프 어텐션 구조이기 때문에 x x x 를 넣어주면됨
        ln1 = self.layer_norm1(x + h)  # 스킵 커넥션
        # 레디쥬얼 구조가됨 ..?

        h = self.dense2(self.dense1(ln1))
        return self.layer_norm2(h + ln1)

    def compute_output_shape(self, input_shape):
        return input_shape


# ## Decoder

class Decoder(Layer):
    def __init__(self, num_head, d_reduced):
        super().__init__()
        self.num_head = num_head
        self.d_r = d_reduced

    def build(self, input_shape):  # 멀티해드 어텐션이 2개가 들어감. 하나는 셀프 어텐션이 들어감

        # self attention 은  mask를 필요로 함
        self.self_attention = MultiHeadAttention(self.num_head, input_shape[0][-1], self.d_r, masked=True)
        self.layer_norm1 = LayerNormalization(input_shape=input_shape)

        # 멀티 어텐션은 마스크가 필요 없음
        self.multi_attention = MultiHeadAttention(self.num_head, input_shape[0][-1], self.d_r)
        self.layer_norm2 = LayerNormalization(input_shape=input_shape)

        self.dense1 = Dense(input_shape[0][-1] * 4, input_shape=input_shape[0], activation='relu')
        self.dense2 = Dense(input_shape[0][-1],
                            input_shape=self.dense1.compute_output_shape(input_shape[0]))

        # input_shape[0] 을 안해주면 Dimension value must be integer or None or have an __index__ method, got TensorShape([None, 65, 16]) 오류 발생

        self.layer_norm3 = LayerNormalization(input_shape=input_shape)

        super().build(input_shape)

    def call(self, inputs, training=None, mask=None):  # 입력이 ( x, context(인코더의 출력) ) 를 받아와야함 (튜플로 구성)
        x, context = inputs
        h = self.self_attention((x, x, x))
        ln1 = self.layer_norm1(x + h)

        h = self.multi_attention((ln1, context, context))
        ln2 = self.layer_norm2(ln1 + h)

        h = self.dense2(self.dense1(ln1))
        return self.layer_norm3(h + ln2)  # 임베딩 형태

    def compute_output_shape(self, input_shape):
        return input_shape


# ## Positional Encoding
#

class PositionalEncoding(Layer):  # Referred from https://github.com/LastRemote/Transformer-TF2.0
    def __init__(self, max_len, d_emb):  # 최대길이를 알아야 최대길이로부터 어느정도 비율의 위치를 알 수 있다. # 최대 길이 입력을 받음
        super().__init__()
        self.sinusoidal_encoding = np.array([self.get_positional_angle(pos, d_emb) for pos in range(max_len)],
                                            dtype=np.float32)
        self.sinusoidal_encoding[:, 0::2] = np.sin(self.sinusoidal_encoding[:, 0::2])
        self.sinusoidal_encoding[:, 1::2] = np.cos(self.sinusoidal_encoding[:, 1::2])
        self.sinusoidal_encoding = tf.cast(self.sinusoidal_encoding, dtype=tf.float32)

    def call(self, x, training=None, mask=None):  # call을 하면 더해주는 구조
        return x + self.sinusoidal_encoding[:tf.shape(x)[1]]

    def compute_output_shape(self, input_shape):
        return input_shape

    def get_angle(self, pos, dim, d_emb):
        return pos / np.power(10000, 2 * (dim // 2) / d_emb)

    def get_positional_angle(self, pos, d_emb):
        return [self.get_angle(pos, dim, d_emb) for dim in range(d_emb)]


# ## Transfomer Architecture

# +
class Transfomer(Model):
    def __init__(self, src_vocab, dst_vocab, max_len, d_emb, d_reduced, n_enc_layer, n_dec_layer, num_head):
        super().__init__()
        self.enc_emb = Embedding(src_vocab, d_emb)  # 임베딩
        self.dec_emb = Embedding(dst_vocab, d_emb)
        self.pos_enc = PositionalEncoding(max_len, d_emb)

        self.encoder = [Encoder(num_head, d_reduced) for _ in range(n_enc_layer)]
        self.decoder = [Decoder(num_head, d_reduced) for _ in range(n_dec_layer)]

        self.dense = Dense(dst_vocab, input_shape=(-1, d_emb))

    def call(self, inputs, training=None, mask=None):  # 인풋이 ( src_sentence (입력센텐스), dst_sentence_shift)
        src_sent, dst_sent_shifted = inputs

        h_enc = self.pos_enc(self.enc_emb(src_sent))
        for enc in self.encoder:
            h_enc = enc(h_enc)  # 인코더 출력을 얻어서 h_enc 에 넣음

        h_dec = self.pos_enc(self.dec_emb(dst_sent_shifted))
        for dec in self.decoder:
            h_dec = dec([h_dec, h_enc])

        return tf.nn.softmax(self.dense(h_dec), axis=-1)  # softmax 의 axis 는 마지막 aixs라서 안써줘도 되긴함


# -

# ## 데이터 셋 준비

# +
# dataset
d_file = 'chatbot_data.csv'  # 출처  : ai허브
okt = Okt()

with open(d_file, 'r', encoding='utf-8-sig') as file:
    lines = file.readlines()
    seq = [' '.join(okt.morphs(line)) for line in lines]  # 줄을 한줄 한줄을 형태소 분석을 해줌
    # 스페이스를 기준으로 단어를 나누어주기 때문에, ' ' 를함

# 질문과 답변을 나누어줌
questions = seq[::2]  # 데이터 셋을 보면 질문은 홀수 줄에 있고 ( 0번부터 가져옴 )
answers = ['\t' + lines for lines in seq[1::2]]  # 대답은 짝수 줄에 있다
# 앞에는 tab을 입력해줌 (\t) 그 이유는 나중에 이것을 sos로 사용 하기 위함
# new line 을 eos로 사용할 것

num_sample = len(questions)  # 전체 길이 파악
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
    if perm[idx] > num_sample // 5:  # 섞어준것의 4/5를 train에 넣어주고
        train_q.append(q)
        train_a.append(a)  # 또다시, 질문과 답을 나눈다 .

    else:  # 그 외의 것을 test에 넣어줌
        test_q.append(q)
        test_a.append(a)

tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=NUM_WORDS,
                                                  # 단어 빈도에 따른 사용할 단어 개수의 최대값. 가장 빈번하게 사용되는 num_words개의 단어만 보존합니다.
                                                  filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~')
# keras에 있는 전처리함수로 토크나이즈를 해줌
# 토크나이즈 : 각 단어들을 숫자로 바꿔주는 것을 의미함
# filter 에 들어있는 것은 다 제거 됨 tqp과 \n을 제외하고 filter을 해줌

tokenizer.fit_on_texts(train_q + train_a)  # 질문과 답변에 대해서 fitting을 해줌

# text로 되어있는 것을 sequence 로 - 숫자로 된 단어 나열이라고 보면 됨

train_q_seq = tokenizer.texts_to_sequences(train_q)
train_a_seq = tokenizer.texts_to_sequences(train_a)

test_q_seq = tokenizer.texts_to_sequences(test_q)
test_a_seq = tokenizer.texts_to_sequences(test_a)

# pad sequence를 이용해서 trian 과 test set을 만들어줌.
# 출력에 대해서는 데이터를 앞쪽으로 정렬을 해줘야하기 때문에 제로 패딩을 뒤쪽으로 해줘야함
# 출력의 maxlen 을 65로 한 이유는 65길이를 해서 앞에 지우고 / 뒤에 지워서 결국 64길이로 사용됨.
x_train = tf.keras.preprocessing.sequence.pad_sequences(train_q_seq,
                                                        value=0,
                                                        padding='pre',
                                                        maxlen=64)

y_train = tf.keras.preprocessing.sequence.pad_sequences(train_a_seq,
                                                        value=0,
                                                        padding='post',
                                                        maxlen=65)

# 이것만 추가됨
y_train_shifted = np.concatenate([np.zeros((y_train.shape[0], 1)), y_train[:, 1:]], axis=1)

x_test = tf.keras.preprocessing.sequence.pad_sequences(test_q_seq,
                                                       value=0,
                                                       padding='pre',
                                                       maxlen=64)
y_test = tf.keras.preprocessing.sequence.pad_sequences(test_a_seq,
                                                       value=0,
                                                       padding='post',
                                                       maxlen=65)

train_ds = tf.data.Dataset.from_tensor_slices((x_train, y_train)).shuffle(10000).batch(32).prefetch(1024)
test_ds = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(1).prefetch(1024)
# -

# ## Train using keras

# +
transfomer = Transfomer(NUM_WORDS, NUM_WORDS, 128, 16, 16, 2, 2, 4)

# 모델 컴파일
transfomer.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
transfomer.fit([x_train, y_train_shifted], y_train, batch_size=5, epochs=EPOCHS)  # 모델 훈련
# -


