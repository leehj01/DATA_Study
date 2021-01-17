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

# ## numpy.unique

import numpy as np

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

arr


