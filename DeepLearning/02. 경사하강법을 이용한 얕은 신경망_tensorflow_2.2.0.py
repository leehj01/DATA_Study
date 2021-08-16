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

# ## 경사 하강법을 이용한 얕은 신경망 학습

import tensorflow as tf
import numpy as np

# ## 하이퍼 파라미터 설정

EPOCHS = 1000


# ## 네트워크 구조 정의
# ### 얕은 신경망
# - 입력계층 :2  , 은닉 계층 : 128 ( 시그모이드 함수 ) , 출력계층 : 10 ( 소프트 맥스 함수 ).

# - init 에서 어떤 레이어를 사용할지 정의해줌
# - call 은 모델이 실제로 call이 될때, 입력에서 출력으로 어떻게 되는지 정의하는 함수

class MyModel(tf.keras.Model): # keras의 model을 상속을 해서 클래스를 구현함. - 그리고 2가지 함수를 정의해야함
    def __init__(self):
        super(MyModel, self).__init__()  # 상속을 했으면, 상속한 함수를 initialize 해야함
        self.d1 = tf.keras.layers.Dense(128, input_dim = 2 , activation = 'sigmoid')
        self.d2 = tf.keras.layers.Dense(10, activation = 'softmax')
        # 입력데이터는 정의해줄 필요 x 왜냐하면 자기가 알아서 들어오기 때문 
        
        
    def call(self, x, training = None , mask = None):
        x = self.d1(x) # 은닉계층이 됨
        return self.d2(x) #출력계층이됨


# ## 학습루프 정의

# - tf의 오토그래프를 이용해서 최적화를 해줄것이다. 
# - @tf.function : 이걸 사용하면 trian_step안에 있는 tensor 연산들이 파이썬 문법들로 계산을 하는데, tf.function 을 통해 tensor의 최적화를 해줌
#
# - train_step 에서 가장 중요한 것은, gradient 를 계산해서, 그라디언트를 옵티마이저에 넣어서 학습을 진행하는 것.

@tf.function 
def train_step(model, inputs, labels, loss_object, optimizer, train_loss, train_metric):
    with tf.GradientTape() as tape: # 여기 안에서 계산된것은 gradient가 계산되고 tape 안에 들어가 있음
        predictions = model(inputs)  # 모델안에 인풋을 넣어서 예측값을 계산함 
        loss= loss_object(labels, predictions ) # loss 를 계산하는데, loss_object에다가 정답이랑 예측값을 넣어서 계산
        # 그러면, gradient가 계산된 것들이 tape안으로 들어가게 됨. 
    
    gradients = tape.gradient(loss, model.trainable_variables ) # tape에서 gradient를 계산을 하는데,  
    # 첫번째 변수를 두번째 변수로 미분해서 gradient를 계산하는 것이 gradients 에 들어가게 된다.
    # loss는 스칼라이며, model에 있는 모든 trainable variables 에 미분을 해준다. 
    # df(x)/dx 를 하는 모양이며, 스칼라를 벡터로 미분하는 것이므로, gradients는 벡터가 된다. ( 편미분한게 들어감 )
    # 이 벡터를 가지고 optimizer를 이용해서 gradient를 적용해줌
    
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    # 학습될것을 zip해서 넣어줌. 각 gradients에 대해 각 trainable_variables 들이 gradient가 적용되서 optimizer로 학습이 됨
    
    train_loss(loss) # train_loss가 loss를 종합해주는 역할을 함
    train_metric(labels, predictions ) #trian_metric을 이용해서 정답과 prediction을 비교해서 평가 지표로 계산을헤줌
    # 여기서는 accuray를 사용할 것 . 몇퍼센트가 정확한지 확인 
    


# ## 데이터 셋 생성, 전처리
# - 따로 데이터가 주어진게 아니라 np로 만들어 보기! 
# - 위의 tensorflow로 모델을 만들때, 설정을 해주지 않는다면 자동적으로 float32가됨. 
# - 데이터 셋도 float64가아닌 32로 만들어 줘야 . 오류가 나지 않는다! 

# +
np.random.seed(0) # random seed를 고정하면,  항상 실행해도 동일한 값이 나옴

pts = list()  # 입력값
labels = list()  # 출력값
# 데이터 셋을 구성하는데 있어서, 10개의 클래스를 가지는 포인터를 생성할 것이다.

center_pts = np.random.uniform(-8.0, 8.0 ,(10,2))  # 이렇게 되면 값이 np.float64가 됨. 

for label, center_pt in enumerate(center_pts):
    for _ in range(100):
        pts.append(center_pt + np.random.randn(*center_pt.shape))  # 중앙 포인트를 기준으로 랜덤하게 동그랗게 퍼지게 됨
        labels.append(label)  # 총 10개의 class를 생성해줌
        
pts = np.stack(pts, axis= 0).astype(np.float32) # 리스트형태인 pts를 stack을 이용해서 넘파이 형태로 만들어줌 
labels = np.stack(labels, axis=0)

train_dataset = tf.data.Dataset.from_tensor_slices((pts, labels)).shuffle(1000).batch(32)
# 입력과 정답을 묶어서 넣어주면, train dataset으로 합쳐줨 
# 데이터 1000개까지 섞음 
# cpu가 학습이 안되면  batch사이즈를 줄이면 됨! 

# -

# ## 모델 생성

model = MyModel()

# ## 손실함수와 최적화 알고리즘 설정
# ### CrossEntropy, Adam Optimizer

loss_object = tf.keras.losses.SparseCategoricalCrossentropy() 
optimizer = tf.keras.optimizers.Adam()

# ## 평가지표설정
# ### Accuracy

train_loss = tf.keras.metrics.Mean(name = 'trian_loss')
train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name = 'train_accuaracy')

# ### 학습루프

for epoch in range(EPOCHS):
    for x , label in train_dataset: # 배치를 32이로 해놨기 때문에 32개의 인풋과 정답이 계속 나오게 됨
        train_step(model, x, label, loss_object, optimizer, train_loss, train_accuracy)
        
    template = 'Epoch {} , Loss: {}, Accuracy : {}'
    print(template.format(epoch +1 , train_loss.result(), train_accuracy.result()*100))

# ## 데이터셋 및 학습 파라미터 저장
# - np.savez_compressed  : 여러개의 넘파이오브젝트를 한번에 저장할 수 있으며, 압축해서 저장할 수 있다. 

# +
np.savez_compressed('np_dataset.npz', inputs = pts, labels = labels)

W_h, b_h = model.d1.get_weights() 
W_o, b_o = model.d2.get_weights()
W_h = np.transpose(W_h)
W_o = np.transpose(W_o)
np.savez_compressed('parameters.npz', W_h = W_h, b_h =b_h, W_o =W_o,b_o=b_o )
# -


