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

# # PyTorch 

# ![image.png](attachment:image.png)

# ## nn.Embedding()을 사용하지 않고, 룩업테이블 과정을 구현 

import torch

# +
train_data = 'i like drinking coffee at cafe'
word_set = set(train_data.split()) # 중복을 제거한 단어들의 집합인 단어 집합 생성

# 단어 집합의 각 단어에 고유한 정수 매핑
vocab = {word : i+2 for i , word in enumerate(word_set)}

vocab['<unk>'] = 0
vocab["<pad"] = 1

print(vocab)

# +
# 단어 집합의 크기를 행으로 가지는 임베딩 테이블을 구현함. 
# 여기서 임베딩 벡터의 차원은 3으로 정함

# 단어 집합의 크기만큼의 행을 가지는 테이블 생성
embedding_table = torch.FloatTensor([
                                       [ 0.0,  0.0,  0.0],
                                       [ 0.0,  0.0,  0.0],
                                       [ 0.2,  0.9,  0.3],
                                       [ 0.1,  0.5,  0.7],
                                       [ 0.2,  0.1,  0.8],
                                       [ 0.4,  0.1,  0.1],
                                       [ 0.1,  0.8,  0.9],
                                       [ 0.6,  0.1,  0.1]
                                    ])

# +
# 임의의 문장 'you need to run'에 대해서 룩업 테이블을 통해 임베딩 벡터들을 가져옴 

sample = 'i like drinking tea'.split()
idxes = []

# 각 단어를 정수로 변환
for word in sample :
    try :
        idxes.append(vocab[word])
    except KeyError:  # 단어 집합에 없는 단어일 경우 < unk > 로 대체 된다.
        idxes.append(vocab['<unk>'])
idxes = torch.LongTensor(idxes)        
print('idxes  :' ,idxes)

# 룩업 테이블
lookup_result = embedding_table[idxes, :] # 각 정수를 인덱스로 임베딩 테이블에서 값을 가져온다.
print(lookup_result)
# -

# ## nn.Embedding () 을 사용하기

# +
# 전처리 과정 
train_data = 'i like drinking coffee at cafe'
word_set = set(train_data.split()) # 중복을 제거한 단어들의 집합인 단어 집합 생성

# 단어 집합의 각 단어에 고유한 정수 매핑
vocab = {word : i+2 for i , word in enumerate(word_set)}

vocab['<unk>'] = 0
vocab["<pad"] = 1

print(vocab)
# -

# #### nn.Embedding 의 인자 
# - num_embeddings : 임베딩을 할 단어들의 개수. 다시 말해 단어 집합의 크기입니다.
# - embedding_dim : 임베딩 할 벡터의 차원입니다. 사용자가 정해주는 하이퍼파라미터입니다.
# - padding_idx : 선택적으로 사용하는 인자입니다. 패딩을 위한 토큰의 인덱스를 알려줍니다.

# +
# 임베딩 테이블 만들기
import torch.nn as nn
embedding_layer = nn.Embedding( num_embeddings= len(vocab),
                              embedding_dim= 3,
                              padding_idx= 1)

print(embedding_layer.weight)
