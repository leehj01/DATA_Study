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

# ## numpy.unique

import numpy as np
import pandas as pd

# np.uniquenp.unique(
#     ar,
#     return_index=False,
#     return_inverse=False,
#     return_counts=False,
#     axis=None,
# )
#
# - arr : 입력 배열, 1차원 배열이아니면 병합됨
# - return_index : 입력 배열 요소들의 인덱스를 리턴함
# - return_inverse : 입력 배열을 재구성할 때, 쓰이는 고유 배열의 인덱스들을 반환
# - return_counts : 중복되지 않는 요소들이 입력 배열에 나타난 회 수를 리턴

# +
array = np.array([1, 14, 22, 16, 4, 4, 173, 34, 22, 16, 4, 4])

print('기본 array              :' , array)
print('\n')
print('유니크 함수 사용 array  :' , np.unique(array))
print('\n')
print('유니크 값과 index 번호  :', np.unique(array, return_index = True)) # 자동으로 오름차순! 
print('\n')
print('유니크값과 원래값 index :', np.unique(array, return_inverse = True)) # 원래 array의 순서 
print('\n')
arr , cnt = np.unique(array, return_counts = True)
print('arr 값을 리턴 받음      :', arr)
print('\n')
print('count 값을 리턴 받음    :' , cnt)
# -

# ## numpy로 그룹바이 하는 효과내기.
# - 많은 양의 데이터를 다룰 때, pandas로 그룹바이를 하면, 너무 많은 시간이 걸린다. 
# - 그래서 numpy로 그룹바이를 하는 효과를 내기

# +
## 먼저, 판다스로 groupby해서 각 문제에 대한 갯수를 세기 

# 데이터를 불러오기. 
train  = pd.read_csv('numpy_groupby_example.csv')
train['count'] = 1
train_gro = train.groupby(['user','problem']).count()
train_gro

# +
# 데이터를 불러오기. 
train  = pd.read_csv('numpy_groupby_example.csv')

# df 형식을 -> array형식으로 바꿔주기. .values 를 해주면 됨
train = train.values

# 비어있는 array를 만들어주기. 리스트로 만들때는 [] 하면 되지만, 
# 여기선 내가 만들고 싶은 크기만큼 정확히 만들어줘야한다.
idx_pro = np.zeros((11, 42)) # trian[0] 은 11개 ,train[1] 의 숫자가 42개있기 때문에, (10, 42)라고 적어준다.
print('비어있는 array : ' , idx_pro.shape)

for idx, pro in train :
    idx_pro[idx - 10000, pro - 1 ] += 1   # 인덱스 번호를 기준으로 맞춰주기 위해 -10000 과 -1 을 해줌 
#     # 왜냐면, train 의 값이 10000 부터 시작함 

print('count해서 넣은 array : ' , idx_pro.shape)    

idx_pro = idx_pro.astype(np.int64)
idx_pro[:3]
