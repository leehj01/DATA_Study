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

# ## Group by 기초

# +
# 한개 열을 기준으로 집계

import pandas as pd
df = pd.DataFrame({'상품번호' : ['P1', 'P1', 'P2', 'P2'],
                   '수량' :     [2, 3, 5, 10]})
# -

df

# - count, min, mean, sum, max ,cumsum 이 있다.

# min: 상품번호별 판매된 최소 수량
df.groupby(by=['상품번호'], as_index=False).min()  # as_index를 false로 해주면, 인덱스로 가지 않아서 , 활용이 편함

# max: 상품번호별 판매된 최대 수량
df.groupby(by=['상품번호'], as_index=False).max()

# 여러개 열을 기준으로 집계할 떄
import pandas as pd
df = pd.DataFrame({'고객번호' : ['C1', 'C2', 'C2', 'C2'],
                   '상품번호' : ['P1', 'P1', 'P2', 'P2'],
                   '수량' :     [2, 3, 5, 10]})

# sum: 고객별 발송해야 할 상품별 수량 합계
df.groupby(by=['고객번호', '상품번호'], as_index=False).sum()

# ## 조건에 따른 데이터 프레임 누적합 계산

import pandas as pd 
d = {'NAME': ['PIKACHU', 'GYARADOS', 'LAPRAS', 'Rattata', 'ZAPDOS'], 'NUM': [10, 250, 10, 20, 700], 'ENERGY' : [1, 1, 1, 1, 1]} 
df = pd.DataFrame(data=d) 
df


# ### NUM이 10일 때까지 ENERGY의 값을 누적하여 저장
# NUM이 10이 되는 순간 다시 cumsum을 reset하고 재 누적합 계산 시작
#

df['cumsum'] = df.groupby((df.NUM == 10).cumsum()).ENERGY.cumsum() 
df



