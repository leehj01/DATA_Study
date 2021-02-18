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

# 어텐션 클래스
# 선형 변환을 위한 가중 파라미터를 편향이 없는 선형 계층으로 대체했음을 확인 할수 있다.

from torch import nn
class Attention(nn.Module):

    def __init__(self, hidden_size):
        super(Attention, self).__init__()

        self.linear = nn.Linear(hidden_size, hidden_size, bias=False)
        self.softmax = nn.Softmax(dim=-1)  # 맨 마지막 차원에 대해서 소프트 맥스 함수를 적용한다는 의미에서 dim = -1 을 써줌

    def forwrd(self, h_src, h_t_tgt, mask=None):
        # h_ src = ( batch_size , length, hidden_size)
        # h_t_tgt =  ( batch_size , 1, hidden_size )
        # mask = (batch_sie, length )

        query = self.linear(h_t_tgt.squeeze(1)).unsqeeze(-1)  # 두번째 차원을 삭제하고, -1 차원 ( 마지막 차원 )을 추가해라.
        # query = (batch_size, hidden_size, 1 )

        weight = torch.bmm(h_src, query).squeeze(-1)  # 배치 행렬곱 연산 : 배치 사이즈를 유지한 채, 뒤의 행렬곱 연산
        # weight = (batch_size , length)

        if mask is not None:  # 마스크가 none이 아니라면,
            # 각각의 weight를 -inf 로 만듦면, 마스크의 values는 1로 공평해진다.
            # softmax함수는 -inf를 0으로 만들기 때문에, 마스크 weight는 소프트함수 이후 0으로 설정된다.
            # 그러므로, 만약 mini batch안에서 다른 샘플보다 그 샘플이 더 적다면,
            # weight는 0으로 가게 된다.

            weight.masked_fill_(mask, -float('inf'))

        weight = self.softmax(seight)

        context_vector = torch.bmm(weight.unsqueeze(1), h_src)
        # context_vector = ( batch_size , 1, hidden_size)

        return context_vector