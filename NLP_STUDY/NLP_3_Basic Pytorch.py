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

import torch

# ### 3.3.1. 텐서
# - 텐서는 넘파이의 배열이 ndarray와 같은 개념 
# - 추가로 텐서간 연산에 따른 그래프와 경사도(gradient)를 저장할 수 있다.
# - 파이토치연산을 수행하기 위한 가장 기본적인 객체이다.

# +
import torch

x = torch.Tensor ([[1,2],[ 3,4]])

print('x :  ', x )

print(sep = '\n')

y = torch.from_numpy(np.array([[1,2],[3,4]]))
print('y :  ',y)

print(sep = '\n')

import numpy as np
z = np.array([[1,2],[3,4]])
print('z :  ', z)
# -

# ### 3.3.2. Autograd
# - 파이토치는 자동으로 미분 및 역전파를 수행하는 autograd 기능을 가짐
# - 대부분의 텐서 간 연산들을 크게 신경 쓸필요 없이 역전파 알고리즘을 수행하는 명령어를 호출하면 됨.
#
# - 파이토치는 텐서들간에 연산을 수행할 때마다 동적으로 연산 그래프를 생성하여 연산의 결과물이 어떤 텐서로부터 어떤 연산을 통해서 왔는지 추정함.
# - 따라서 우리가 최종적으로 나온 스칼라에 역전파 알고리즘을 통해 미분을 수행하도록 했을 때, 각 텐서는 자기 자신의 자식 노드에 해당하는 텐서와 연산을 자동으로 찾아 계속해서 역전파 알고리즘을 수행할 수 있도록 함.

# +
import torch

x = torch.FloatTensor(2,2)  # 2 x 2 의 랜덤값이 나옴

y = torch.FloatTensor(2,2)

y.requires_grad_(True) 

z = ( x+ y) + torch.FloatTensor(2,2)
# -

# - with 문법을 사용하여 연산 수행 

# +
import torch

x = torch.FloatTensor(2,2)
y = torch.FloatTensor(2,2)
y.requires_grad_(True)

with torch.no_grad():
    z = (x + y) + torch.FloatTensor(2,2 )
# -

# ■ 다른 예시 - 자동 미분 실습

# +
import torch
w = torch.tensor(2.0, requires_grad=True)

y = w**2 
z = 5*y + 3

z.backward()
print(z)
# tensor(23., grad_fn=<AddBackward0>)

print('수식을 w로 미분한 값 : {}'.format(w.grad))
# -

# ### 3.3.3. 피드포워드

# - torch.mm :  행렬곱 

# +
import torch

def linear(x, W, b) :
    y = torch.mm(x, W) + b
    
    return y

x = torch.FloatTensor(16,10)
W = torch.FloatTensor(10,5)  
b = torch.FloatTensor(5)

y = linear(x, W, b)

# -

y

# #### 3.4.4. nn.Module
#
# : nn.Module이라는 클래스는 사용자가 그 위에서 필요한 모델 구조를 구현할 수 있게 함.
#
# - nn.Module을 상속한 사용자 정의 클래스는 다시 내부에 nn.Module을 상속한 클래스 객체를 선언하여 소유할 수 있다.
#
# - 즉, nn.Module 상속 객체 안에 nn.Module 상속 객체를 선언하여 변수로 사용할 수 있다.
#
# - nn.Module 의 forward() 함수를 오버라이드(override)하여 피드포워드를 구현 할 수 있다.
#
# - nn.Moduledml 의 특징을 이용하여 한번에 신경망 가중치 파라미터들을 저장 및 불러오기를 수행 할 수있다.

# +
import torch
import torch.nn as nn

class MyLinear(nn.Module): # nn.Module 안에 nn,Nodule을 상속
    
    def __init__(self, input_size , output_size):
        super().__init__()  #  상속받은 부모 클래스를 의미
        
        self.W = torch.FloatTensor(input_size, output_size)
        self.b = torch.FloatTensor(output_size)
        
    def forward(self , x):
        y = torch.mm(x, self.W) + self.b
        
        return y


# -

y

params = [ p.size() for p  in linear.parameters()]
print(params)

# +
import torch
import torch.nn as nn

class MyLinear(nn.Module): # nn.Module 안에 nn,Nodule을 상속
    
    def __init__(self, input_size , output_size):
        super(MyLinear, self).__init__()  #  상속받은 부모 클래스를 의미
        
        self.W = nn.Parameter(torch.FloatTensor(input_size, output_size), requires_grad= True)
        self.b = nn.Parameter(torch.FloatTensor(output_size),requires_grad = True )
        
    def forward(self , x):
        y = torch.mm(x, self.W) + self.b
        
        return y


# -

x = torch.FloatTensor(16,10)
linear = MyLinear(10, 5)
y = linear(x)

params = [ p.size() for p  in linear.parameters()]
print(params)

# - 더 깔끔하게 코드 구현

# +
import torch
import torch.nn as nn

class MyLinear(nn.Module):
    
    def __init__(self, input_size , output_size):
        super(MyLinear, self).__init__()
        
        self.linear = nn.Linear(input_size, output_size)
        
    def forward(self, x):
        y = self.linear(x)
        
        return y


# -

x = torch.FloatTensor(16,10)
linear = MyLinear(10,5)

print(linear)

#
# ### 3.4.5. 역전파 수행
#
# : 피드포워드를 통해 얻은 값에서 실제 정답값과의 차이를 계산하여 오류(손실)을 뒤로 전달 (back - propagation)하는 역전파 알고리즘
#
#
#
# - 원하는 값이 100이라고 했을때, linear의 결과값 텐서의 합과 목푯값과의 거리(error 혹은 loss)을 구하고, 그 값에 대해 bakward() 함수를 사용하여 기울기를 구함. 
#
# - 이때, 에러값은 스칼라로 표현되어야 함. 벡터나 행렬의 형태는 안됨

import torch

# +
objective = 100

x = torch.FloatTensor(16,10)
linear = MyLinear(10, 5)
y = linear(x)
loss = (objective - y.sum())
loss.backward()

# -

loss


