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

# ##  Seq2seq 구현 및 학습

import random
import tensorflow as tf
from konlpy.tag import Okt

tf.__version__

# ## 하이퍼 파라미터

EPOCHS = 10
NUM_WORDS = 2000


# ## Encoder 

class Encoder(tf.keras.Model):
    def __init__(self):
        super(Encoder, self).__init__()
        self.emb = tf.keras.layers.Embedding(NUM_WORDS, 64) # 원핫 형태로 들어오면 인베딩을 먼저 해줌  그래서 우리가 원하는 실수로 바꿔줌
        self.lstm = tf.keras.layers.LSTM(512, return_state = True ) # lstm을 이용해서 state를 뽑게 됨. 
        # state를 return 하게 해줘야 , hidden 과 cell state를 return 하게 됨. 기본적으로 false 하게 됨. 
        # 다음 계층으로 넘어갈것만 있고, 아래의 h ,c 의 값이 안나오므로 꼭 TRUE로 해줘야함  
        
    def call(self, x, training = False , mask = None):
        x = self.emb(x)
        _, h , c = self.lstm(x)
        return h, c # h,c 를 context로 추출해주는게 우리의 목적임! 


# ## Decoder 

class Decoder(tf.keras.Model):
    def __init__(self):
        super(Decoder, self).__init__()
        self.emb = tf.keras.layers.Embedding(NUM_WORDS, 64) # shifted output
        
        self.lstm = tf.keras.layers.LSTM(512, return_sequences = True, return_state = True)
        # return_sequences가 false이면, dense x 의 출력이 마지막 하나면 return하게 되는데
        # 우리는 모든 출력을 알아야 하기 때문에, sequence형태로 출력이 되기 위해 true 로 설정
        
        self.dense = tf.keras.layers.Dense(NUM_WORDS, activation ='softmax') # 원핫 인코딩을 하는 softmax를 하여 어떤 word일지 추정을 함
        
    def call(self, inputs, training = False, mask = None):
        x, h ,c = inputs # shifted outpt, hiddenstate , cellstate 
        x = self.emb(x)  # 입력이 들어온 것을 임베딩 해줌 
        x, h, c = self.lstm(x, initial_state=[h,c]) # 인코더로 들어온 것을 initial_state로 넣어주고 lstm을 돌림 
        # 나온 결과가 dense로 들어가서 어떤 형태로 추정할지 classfication 이 됨 
        # hidden / cell 출력은 train할때는 필요없지만 test할 때는 이것이 필요함. 
        return self.dense(x) , h , c


# ## Seq2Seq
# - traing이랑 test랑 무엇이 다른가 ? 
#  : traing은 shifted output을 입력으로 넣어 주기 때문에 입력을 피딩 해주는게 간단하다.
#   하지만 test를 할때는 마지막에 얻은 출력을 다시 입력으로 넣어주는 부분이 필요하기 때문에 코드가 조금 복잡하다 .( for문 사용 이용 )

class Seq2seq(tf.keras.Model):
    def __init__(self, sos, eos):
        super(Seq2seq, self).__init__()
        self.enc = Encoder()
        self.dec = Decoder() # 위에서 만들어놓은 인코더와 디코드 함수를 불러오기
        self.sos = sos
        self.eos = eos  # sos 와  eos를 받아줌 
        
    def call(self, inputs , training = False , mask = None):
        if training is True:  # 학습 과정
            x, y = inputs  # x 는 입력 y는 출력 - y는 디코더의 입력으로 필요함 
            h, c = self.enc(x) # 인코더에 입력(x)을 넣어서, 히든 state와 cell state를 받아즘 
            y, _, _ = self.dec((y, h, c))  # 디코더의 결과로 y가 됨. - 전체 문장이 됨 
            return y
         
        else : # test의 과정 
            x= inputs  # 정답을 넣어주면 안되기 때문에 input 하나 밖에 없다. 
            h, c = self.enc(x) 
            y= tf.convert_to_tensor(self.sos) # 훈련과 다른 부분! 디코더단에 입력을 어떻게 넣어주는지가 좀 달라짐
            # 첫번째 입력으로는 sos (start of seq 을 넣어주게 됨 )
            
            y = tf.reshape (y, (1,1))  # tensorflow에도 reshape이 있었다!!
            
            seq = tf.TensorArray(tf.int32, 64) # seq을 최대 64길이까지 받을 것이고, 그것을 for문 형태로 
            
            for idx in tf.range(64):  # tf.range를 사용하면, 우리가 사용하는 일반적인 for 문이 아니라
                # tf.keras.Model로 인해,  call 함수는 오토 그래프로 변하게 되는데, 그때, tf.range가 되어있는 부분이
                # 내부가 다 tf 로 되어있다면 tf for문으로 효율적인 for문으로 바뀌게 됨. 
                # for 구문 안에는 tf로 해줘야함
                
                y, h, c = self.dec([y,h,c])  
                
                y = tf.cast(tf.argmax(y, axis = -1), dtype = tf.int32)
                # y는 softmax를 이용하여 마지막 출력으로 나올 것이기 때문에, 원핫벡터로 바꿔주고 
                # ~ 표현으로 바꾸기 위해 가장 큰값을 argmax를 사용하여 그 값의 index 를 가져올 수 있다.
                # 그것을 tf.int32로 cast를 해줌 [ cast : 간단하게 말하면 정수형으로 바꾸어주는것 ]
                
                y = tf.reshape(y, (1,1)) # reshape 의 이유는 : 입력을 넣어줄 때 , 그냥 넣어주면 차원이 1개밖에 없게 되는데
                # 우리는 실제로 네트워크를 사용할 때 배치를 고려해서 사용해줘야하기 때문에, 배치의 하나를 설명하기 위해 (1,1)을 함
                seq = seq.write(idx , y) # 츌력을 seq의 write를 해주면 허나씩 출력을 받을 때마다 입력을 받게 됨 
                
                if y == self.eos :  # 얻어낸 값이 ens라면 바로 끝내고  그렇지 않다면 다시 for문을 돌면 
                    break 
                    
            return tf.reshape (seq.stack(), (1,64)) # 최종적으로 1(배치크기),64(문장의 최대 길이) 로 출력을 해줌 


# ## 학습 , 테스트 루프 정의

# +
# implement training loop 
@tf.function
def train_step(model, inputs, labels, loss_object, optimizer, train_loss, train_accuracy):
    output_labels = labels[:, 1:] # output label과 shifted 로 나누어줌 
    shifted_labels = labels[:, :-1] 
     
    with tf.GradientTape() as tape:
        predictions = model([inputs , shifted_labels], training = True)
        loss = loss_object(output_labels, predictions)
    gradients = tape.gradient(loss, model.trainable_variables )
    
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    train_loss(loss)
    train_accuracy(output_labels, predictions)
    

# implement algorithm test
@tf.function 
def test_step(model, inputs):
    return model(inputs , training = False)

 # test는 어떻게 나올지 모르기 때문에 배치 하나만 받아서 seq을 출력해주는 형태를 가지게 함


# +
# Implement training loop
@tf.function
def train_step(model, inputs, labels, loss_object, optimizer, train_loss, train_accuracy):
    output_labels = labels[:, 1:]
    shifted_labels = labels[:, :-1]
    
    with tf.GradientTape() as tape:
        predictions = model([inputs, shifted_labels], training=True)
        loss = loss_object(output_labels, predictions)
    gradients = tape.gradient(loss, model.trainable_variables)

    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    train_loss(loss)
    train_accuracy(output_labels, predictions)

# Implement algorithm test
@tf.function
def test_step(model, inputs):
    return model(inputs, training=False)


# -

# ## 데이터 셋 준비

# +
# dataset 
d_file = 'chatbot_data.csv' # 출처  : ai허브
okt = Okt()

with open(d_file, 'r', encoding = 'utf-8-sig') as file :
    lines = file.readlines()
    seq = [' '.join(okt.morphs(line)) for line in lines] # 줄을 한줄 한줄을 형태소 분석을 해줌 
    # 스페이스를 기준으로 단어를 나누어주기 때문에, ' ' 를함 
    

# -

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


print(list(zip(questions, answers))) # zip을해주면 질문과 대답이 묶인다 

# +
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
# -

train_ds

# ## 학습환경 정의
# ### 모델생성, 손실함수, 최적화 알고리즘, 평가지표정의

# +
# create model
model = Seq2seq(sos = tokenizer.word_index['\t'],
               eos = tokenizer.word_index['\n'])

# define loss and optimizer
loss_object = tf.keras.losses.SparseCategoricalCrossentropy()
optimizer = tf.keras.optimizers.Adam()

# Define performance metrics
train_loss = tf.keras.metrics.Mean(name = 'train_loss')
train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name = 'trian_accuracy')
# -

# ## 학습루프 동작

for epoch in range(EPOCHS):
    for seqs, labels in train_ds:
        train_step(model, seqs, labels, loss_object, optimizer, train_loss , train_accuracy)
        
    template = 'Epoch {}, Loss : {} , Accuracy : {}'
    print( template.format(epoch +1 ,
                          train_loss.result(),
                          train_accuracy.result()*100))
    
    train_loss.reset_states()
    train_accuracy.reset_states()
    

# ## 테스트 루프

for test_seq , test_labels in test_ds:
    prediction = test_step(model, test_seq)
    test_text = tokenizer.sequences_to_texts(test_seq.numpy()) # 질문 
    gt_text = tokenizer.sequences_to_texts(test_labels.numpy()) # test 정답 
    texts = tokenizer.sequences_to_texts(prediction.numpy()) # 예측한 대답 
    print("_")
    print("q: ", test_text)
    print("a: ", gt_text)
    print('p: ', texts)


