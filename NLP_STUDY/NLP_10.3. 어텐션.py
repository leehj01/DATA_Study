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

# ### attention key-value 함수 

dic = { '형광펜' : 3 , '수첩' : 7 , '지우개' : 4 }

from gensim.models import Word2Vec


# +
def key_value_fnc ( query ):
    weights = []
    
    for key in dic.keys():
        weights += [is_same(key, query)]  # 코사인 유사도값 채워 넣음 
        
    weight_sum = sum(weights)  # 모든 weight를 구한 후에 softmax 계산

    for i , w in enumerate (weights):
        weights[i] = weights[i] / weight_sum
        
    answer = 0
    
    for weight, value in zip(weights, dic.values()):
        answer += weight * value
        
    return answer 

def is_same(key, query):
    if key == query :
        return 1.
    else :
        return .0
    
key_value_fnc('형광펜')
# -

key_value_fnc('형광펜')


