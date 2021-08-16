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

def sigmoid(x):
    return 1 / (1 + np.exp(-x))
def softmax(x):
    e_x = np.exp(x)
    return e_x / np.sum(e_x)


# ## 얕은 신경망을 이용한 다중분류문제

import numpy as np
import matplotlib.pyplot as plt


# ## 함수 구현
# ### sigmoid 함수 
# - sigmoid(x) = 1/(1 + e^-x)

def sigmoid(x):
    return 1 / ( 1 + np.exp(-x))


# +
# 시그모이드 함수 그래프를 그리는 코드
def sigmoid(x):
    return 1/ (1 + np.exp(-x))

x = np.arange(-5.0 , 5.0 , 0.1)
y = sigmoid(x)

plt.plot(x, y)
plt.plot([0,0], [1.0,0.0], ':') # 가운데 점선 
plt.title('sigmoid function')
plt.show()


# -

# ### softmax 함수
# - softmax(x) 

def softmax(x):
    e_x = np.exp(x)
    return e_x / np.sum(x)


# +
x = np.arange(-5.0, 5.0, 0.1) # -5.0부터 5.0까지 0.1 간격 생성
y = np.exp(x) / np.sum(np.exp(x))

plt.plot(x, y)
plt.title('Softmax Function')
plt.show()


# -

# ## 네트워크 구조 정의

# +
# define network architecture

class ShallowNN:
    def __init__(self, num_input,  num_hidden, num_output): # input , hidden, output의 뉴런의 갯수
        self.W_h = np.zeros((num_hidden, num_input), dtype = np.float32) # 내적 하려고, 히든레이어가 앞에 옴
        self.b_h = np.zeros((num_hidden) , dtype = np.float32 )
        self.W_o = np.zeros((num_output, num_hidden), dtype = np.float32)
        self.b_o = np.zeros(num_output, dtype = np.float32)
        
        # 여기서 적절한 값이 아닌 zeros를 넣어준 후, 아래서 weights를 넣어줌
    
    def __call__(self, x): 
        h = sigmoid(np.matmul(self.W_h,x) + self.b_h )
        # 히든 레이어를 쌓기 [히든레이어 공식]
        # : 시그모이드 활성화함수를 주고, 매트릭스 연산으로 해서 w_h 히든 레이어의 (weight)매트릭스 곱해주고, bias를 더해주는 공식을 이용.
        
        return softmax(np.matmul(self.W_o, h) + self.b_o)
         # 출력 output은 바로 return 에 적어준다. softmax를 해야 다중 분류를 할 수 있음. 


# -

# ## 데이터셋 가져오기, 정리하기

# +
# import and organize dataset

dataset = np.load('ch2_dataset.npz')
inputs = dataset['inputs']
labels = dataset['labels'] # 분류에서는 정답을 label 이라고 해줌 
# -

# ## 모델만들기

# +
#cresate model

model = ShallowNN(2, 128, 10 ) # 인풋갯수, 히든 갯수 ,출력갯수  # 히든 갯수는 적당히 적어주면 됨
# -

# ## 사전에 학습된 파라미터 불러오기

weights = np.load('ch2_parameters.npz')
model.W_h = weights['W_h']
model.b_h = weights['b_h']
model.W_o = weights['W_o']
model.b_o = weights['b_o']

# ## 모델 구동 및 결과 프린트

# +
outputs = list()
for pt, label in zip(inputs, labels):
    output = model(pt) # 소프트 멕스여서 , 각각 확률로 나오는데, 
    outputs.append(np.argmax(output)) # 높은 애의 인덱스가 나오게 됨.
    print(np.argmax(output), label) # 추정값과 실제 값을 프린트함
    
outputs = np.stack(outputs, axis = 0) # 리스트가 넘파이 object가 됨
    
# -

# ## 정답 클래스 스캐터 플랏

plt.figure()
for idx in range(10) :
    mask = labels == idx
    plt.scatter(inputs[mask, 0], inputs[mask, 1])
plt.title('true label')
plt.show()

# ## 모델 출력 클래스 스캐터 플랏 ( 추정한 값 )

plt.figure()
for idx in range(10) :
    mask = outputs == idx
    plt.scatter(inputs[mask, 0], inputs[mask, 1])
plt.title('model outputs')
plt.show()


# b

# Define network architecture
class ShallowNN:
    def __init__(self, num_input, num_hidden, num_output):
        self.W_h = np.zeros((num_hidden, num_input), dtype=np.float32)
        self.b_h = np.zeros((num_hidden,), dtype=np.float32)
        self.W_o = np.zeros((num_output, num_hidden), dtype=np.float32)
        self.b_o = np.zeros((num_output,), dtype=np.float32)
        
    def __call__(self, x):
        h = sigmoid(np.matmul(self.W_h, x) + self.b_h)
        return softmax(np.matmul(self.W_o, h) + self.b_o)


# Import and organize dataset
dataset = np.load('ch2_dataset.npz')
inputs = dataset['inputs']
labels = dataset['labels']

# Create Model
model = ShallowNN(2, 128, 10)

weights = np.load('ch2_parameters.npz')
model.W_h = weights['W_h']
model.b_h = weights['b_h']
model.W_o = weights['W_o']
model.b_o = weights['b_o']

outputs = list()
for pt, label in zip(inputs, labels):
    output = model(pt)
    outputs.append(np.argmax(output))
    print(np.argmax(output), label)
outputs = np.stack(outputs, axis=0)

plt.figure()
for idx in range(10):
    mask = outputs == idx
    plt.scatter(inputs[mask, 0], inputs[mask, 1])
plt.title('model_output')
plt.show()






