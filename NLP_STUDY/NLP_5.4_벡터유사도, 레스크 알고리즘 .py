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

# ## 벡터간의 유사도 또는 거리를 구하는 방법

# ### 1. L1 거리

# +
import torch

def get_l1_distance(x1, x2):
    return ( (x1 - x2 ).abs()).sum()


# -

# ### 2. L2 거리

def get_l2_distance(x1, x2 ) :
    return ((x1 - x2)**2).sum()**.5


# ### 3. infinity Norm 

def get_infinity_distance(x1, x2):
    return ((x1 - x2).abs()).max()


# ### 4. 코사인 유사도

def get_cosine_similarity ( x1, x2 ):
    return (x1 * x2).sum() / ((x1**2).sum()**.5 * (x2**2).sum()**.5)


# ### 5. 자카드 유사도

# +
def get_faccard_similarity ( x1, x2 ):
    return torch.stack([x1 , x2]).min(dim=0)[0].sum() / torch.stack([x1, x2 ])

# torch.stack 는 두개의 텐서를 결합하는 함수이다. 


# -

# ## 단어 중의소 해소 : 레스크 알고리즘

# +
# 먼저, NLTK의 워드넷에서 단어 검색

from nltk.corpus import wordnet as wn
for ss in wn.synsets('bass'):
    print(ss, ss.definition()) # 단어의 설명을 구하는 코드 


# +
# 레스크 알고리즘 수행을 위해 간단하게 감싸서 구현

def lesk(sentence, word):
    from nltk.wsd import lesk
    
    best_synset = lesk(sentence.split(), word)
    print(best_synset, best_synset.definition())
    


# -

sentence = "I went fishing last weekend and i got a bass and cooked it " # 물고리를 의미함
word = "bass"
lesk(sentence, word) # 잘 예측함

sentence = 'I love the music from the speaker which has strong beat and bass' # 음악
word = 'bass'
lesk(sentence, word) # 잘 예측함 

sentence = 'I think the bass is more important than guitar'
word = 'bass'
lesk(sentence, word)
