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

import torch

# ### squeeze : 1개 요소를 갖는 축 제거 
# - 차원의 size 가 1인 차원을 없애줌 
#
#

# +
x = torch.FloatTensor(10, 1 ,3 ,1 , 4 )
y = torch.squeeze(x)
print(x.size(), y.size())

z = x.squeeze(1)  # dim 을 설정하면, 원하는 위치의 차원 축 삭제 해줌. 
print(z.size())
# -

# ### unsqueeze 연산 
# - 차원 size 가 1 인 차원을 생성 
# - unsqueeze(input, dim) : 추가하고 싶은 차원에 dim index 넣어주기 : idx번째 차원을 만들면 기존 idx차원부터 한칸씩 미뤄짐

# +
x = torch.FloatTensor(10, 3, 4)
y = torch.unsqueeze(x , dim = 0 )
print(x.size(), y.size())

z = torch.unsqueeze(x , dim = 1 )
print(x.size() , z.size())

z = z.unsqueeze( 3 ) # 이렇게도 표현가능 
print(z.size())
# -

# ### 배치 행렬곱 연산 ( 맨 앞에 batch 차원은 유지하면서 뒤에 요소들의 행렬곱 )

# +
import torch

x = torch.FloatTensor([
    [[1,2,3],[4,5,6]],
    [[1,2,3],[4,5,6]]
])

print(x.shape)

y = torch.FloatTensor([
    [[1,2,3],[4,5,6],[7,8,9]],
    [[1,2,3],[4,5,6],[7,8,9]],
])

print(y.shape)

z = torch.bmm(x, y)
print(z.shape )
print(z)
# -


