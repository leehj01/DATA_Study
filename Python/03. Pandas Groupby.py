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
# 데이터 프레임을 만들어 주기
import pandas as pd
df = pd.DataFrame({'user_id' : ['C1', 'C2', 'C2', 'C2','C3', 'C3', 'C3', 'C3','C1','C4'],
                   'product_id' : ['P1', 'P1', 'P2', 'P2','P3', 'P3','P4', 'P4','P4','P4'],
                   'buy_cnt' :     [20, 3, 5, 10,5, 7, 8, 9, 4, 10],
                  'point' : [70, 200, 100, 50, 100, 200, 100,20, 50 , 200],
                   'time' : [ '2015-10-14 06:58', '2015-10-14 06:58', '2015-11-14 14:46',
                        '2015-11-14 14:48', '2015-10-14 17:27', '2015-10-14 18:55',
                            '2016-10-14 06:58' , '2016-11-14 15:01' ,'2016-10-14 15:12', '2016-10-14 15:30']}
)

import datetime
df.time = df['time'].apply(lambda _ : datetime.datetime.strptime(_,  '%Y-%m-%d %H:%M'))
# -

df

# # 기본적인 GROUPBY

# ### 1. 한개 열을 기준으로 집계 

# - count, min, mean, sum, max ,cumsum 이 있다.

# min: 상품번호별 판매된 최소 수량
df.groupby(by=['product_id']).min()

# ### 2. 여러개 열을 기준으로 집계

df_grouped = df.groupby(['product_id','user_id']).sum()
df_grouped

df_grouped = df.groupby(['product_id','user_id'], as_index = False).sum()
df_grouped



df_grouped.index

# - groupby 명령의 결과물도 결국 dataframe이기 때문에,
# 두개의 column으로 gropbt할 경우, index가 두개 생성된다.

# group으로 묶여진 데이터를 matrix형태로 전환해줌.
df_grouped.unstack()

# +
# 인덱스 level을 변경할 수 있다.
# -

df_grouped.swaplevel()

df_grouped.swaplevel().sortlevel(0)

# +
## 인덱스 level을 기준으로 기본연산 수행
# -

df_grouped.sum(level = 0)

df_grouped.sum(level = 1)

# sum: 고객별 발송해야 할 상품별 수량 합계
df_grouped_2 = df.groupby(by=['고객번호', '상품번호'], as_index=False).sum()
df_grouped_2

df_grouped_2.unstack()  # value가 두개이기 때문에, 예쁘게 안떨어짐 

# ## grouped 

# ### groupby에 의해 split된 상태를 추출 가능함

# +
grouped = df.groupby('고객번호')

for name, group in grouped:
    print(name)
    print(group)
# -

# ### 특정 key값을 가진 그룹의 정보만 추출 가능
# - 추출된 group 정보에는 3가지 유형의 apply가 가능함
#     - aggregation : 요약된 통계정보를 추출해줌
#     - transformation : 해당정보를 변환해줌
#     - filtration : 특정 정보를 제거하여 보여주는 필터링 가능

grouped.get_group('C2')

## 1. aggregation 
grouped.agg(sum)

import numpy as np
grouped.agg(np.mean)

# 특정 컬럼에 여러개의 function을 apply할 수 도있음
grouped['포인트'].agg([np.sum, np.mean, np.std])

# # 2. trainsformation : agg와 달리 key값 별로 요약된 정보가 아니라, 개별 데이터의 변환을 지원함


# +
## 3. filter  : 특정조건으로 데이터를 검색할 때 사용

df.groupby('고객번호').filter(lambda x: len(x) > 2)

# +
# filter안에는 boolean 조건이 존재해야함. len(x)는 grouped된 dataframe의 개수ㅜ
# -

df.groupby('고객번호').filter(lambda x: x['수량'].sum() > 10)



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






