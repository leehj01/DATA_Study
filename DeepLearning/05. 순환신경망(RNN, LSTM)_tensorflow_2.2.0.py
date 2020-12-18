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

# ## 순환 신경망 구현 및 학습
# - tensorflow 를 이용하여 순환 신경망 구현할 것! 

import tensorflow as tf

 tf.__version__

# ## 하이퍼 파라미터

EPOCHS = 10
NUM_WORDS = 10000 # 분석을 하기위해서 만개의 단어만 사용하겠다는 의미


# ## 모델정의
# - 여기서 SimplerRNN -> LSTM 으로 바꾸어주면, LSTM으로 바뀌게 됨. 혹은 GRU로 바꾸면 GRU가 됨 

class MyModel(tf.keras.Model):
    def __init__(self):
        super(MyModel, self).__init__()
        self.emb = tf.keras.layers.Embedding(NUM_WORDS, 16) 
        # 원핫 벡터가 10000일때, 첫번째가 MY 였다면, 특정 단어들이 원핫 벡터들이 하나씩 표현됨. 
        # Embedding : 원핫 벡터는 정수값이라서, 심지어 0,1의 바이너리값이여서, 실수값을 가져오기 위해서 길이가 10000인 원핫 벡터를 길이가 16인 피쳐 벡터로 바꿔주는 역할을 함
        
        self.rnn = tf.keras.layers.SimpleRNN(32) # rnn layer를 사용하는데, 심플하게 바닐라 rnn사용
        # 여기서 SimplerRNN -> LSTM 으로 바꾸어주면, LSTM으로 바뀌게 됨. 혹은 GRU로 바꾸면 GRU가 됨 
        
        self.dense = tf.keras.layers.Dense(2, activation = 'softmax') # 감정분석 을 할거기 때문에, 길이가 2인 소프트 맥스를 사용 
        
    def call(self, x , training = None, mask = None):
        x = self.emb(x)
        x = self.rnn(x)
        return self.dense(x)
    


# #### LSTM은 히든 레이러를 늘리면 성능이 더 안좋아 진다고 한다.

class MyModel(tf.keras.Model):
    def __init__(self):
        super(MyModel, self).__init__()
        self.emb = tf.keras.layers.Embedding(NUM_WORDS, 16) 
        
        self.rnn1 = tf.keras.layers.LSTM(32) 
        self.rnn2 = tf.keras.layers.LSTM(32)
        self.rnn3 = tf.keras.layers.LSTM(32)
        
        self.dense = tf.keras.layers.Dense(2, activation = 'softmax') 
        
    def call(self, x , training = None, mask = None):
        x = self.emb(x)
        x = self.rnn(x)
        return self.dense(x)
    


# ## 학습, 테스트 루프 정의

# +
# Implement training loop 

@tf.function
def train_step(model, inputs , labels, loss_object, optimizer, train_loss, train_accuracy ) :
    with tf.GradientTape() as tape :
        predictions = model(inputs, training = True )
        loss = loss_object(labels, predictions )
    gradients = tape.gradient(loss, model.trainable_variables)
    
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    train_loss(loss)
    train_accuracy(labels, predictions )
    

# Implement algorithm test
@tf.function 
def test_step(model, inputs, labels, loss_object, test_loss, test_accuracy):
    predictions = model(inputs, training = False)
    
    t_loss = loss_object(labels, predictions)
    test_loss(t_loss)
    test_accuracy(labels, predictions)


# -

# ## 데이터 셋 준비
# - Y가 다중 출력인 경우는 pre대신에 post를 사용하면 0이 뒤로 간다.

# +
imdb = tf.keras.datasets.imdb
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words = NUM_WORDS)


# 데이터의 L 의 길이가 다르기 때문에, PRE -PADDING 을 해준다. 
x_train = tf.keras.preprocessing.sequence.pad_sequences(x_train, 
                                                        value = 0,  # 0으로 패팅을 해줌
                                                        padding = 'pre',
                                                        maxlen = 32) # 최대길이를 32로 잘라주면서 앞에 패팅 0해줌

x_test = tf.keras.preprocessing.sequence.pad_sequences(x_test, 
                                                        value = 0,  # 0으로 패팅을 해줌
                                                        padding = 'pre',
                                                        maxlen = 32) # 최대길이를 32로 잘라주면서 앞에 패팅 0해줌

# 학습할 때마다 셔플이 일어날 수 있도록 설정 
train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train)).shuffle(10000).batch(32)
test_dataset = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(32)
# -

# ## 학습 환경 정의
# ### 모델 생성, 손실함수, 최적화 알고리즘, 평가지표 정의

# +
# Create model
model = MyModel()

# Define loss and optimizer
loss_object = tf.keras.losses.SparseCategoricalCrossentropy()
optimizer = tf.keras.optimizers.Adam()

# Define performance metrics
train_loss = tf.keras.metrics.Mean(name = 'train_loss')
train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name= 'train_accuracy')

test_loss = tf.keras.metrics.Mean(name = 'test_loss')
test_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name = 'test_accuracy')
# -

# ## 학습루프 동작

for epoch in range(EPOCHS):
    for inputs , labels in train_dataset:
        train_step(model, inputs , labels, loss_object, optimizer, train_loss, train_accuracy)
        
    for test_seqs , test_labels in test_dataset:
        test_step(model, test_seqs, test_labels, loss_object, test_loss, test_accuracy)
        
    template = 'Epoch {} , loss : {}, Accuracy : {}, Test Loss : {} , Test Accuracy : {}'
    print( template.format(epoch +1,
                          train_loss.result(),
                          train_accuracy.result()*100,
                          test_loss.result(),
                          test_accuracy.result()*100))
    
    train_loss.reset_states() # 다음 훈련할 데이터가 이전의 훈련할 데이터와 완전히 연관 없을 때 사용하는 것이다
    train_accuracy.reset_states()
    test_loss.reset_states()
    test_accuracy.reset_states()
