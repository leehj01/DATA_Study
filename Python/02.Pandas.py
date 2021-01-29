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

# # Drop - row, column 삭제 

import numpy as np

data = pd.DataFrame(np.arange(16).reshape((4,4,)),
                   index = ['A','B','C','D'],
                   columns = ['가','나','다','라'])
data

data.drop(['A','B'])

data.drop(['가','나'], axis= 1)

# # 데이터프레임 컬럼이름 변경하기

data

# ## 1) 기존 컬럼명 1:1 매칭으로 변경하기

data = data.rename({'가':'도','나':'레'}, axis = 'columns')
data

# ## 새 컬럼명 직접 덮어쓰기

data.columns = ['이','얼','싼']

data.columns = ['z이','z얼','z싼','z쓰']
data

# ## 3) 기존문자를 대체 문자로 바꾸기

data.columns = data.columns.str.replace('z','zh')
data

# ## 4) prefix 사용

data.add_prefix('lang')

# ## suffix 사용

data.add_suffix('lang')

# # 데이터프레임 컬럼 순서 변경

data = pd.DataFrame(np.arange(16).reshape((4,4,)),
                   index = ['A','B','C','D'],
                   columns = ['나','다','가','라'])
data

data = data[['가','나','다','라']]
data

# # 데이터 프레임 새 컬럼 추가하기

data['마'] = '한글'
data

data.loc[:, '바'] = '언어'
data

# # pandas dataframe에 여러개의 빈열 추가

data["B"] = None
data["C"] = None
data["D"] = None
data

data[["솔", "라", "시"]] = None
data

pd.concat([data,pd.DataFrame(columns=list('EFG'))])

# # 데이터 프레임에 한 행을 추가하기

# ## 1) .loc[index] 메소드
# - ignore_index는 사전을append()함수에 전달할 때 True으로 설정됩니다. 그렇지 않으면 오류가 발생합니다.

# +
# python 3.x
import pandas as pd
# List of Tuples
fruit_list = [ ('Orange', 34, 'Yes' )]

#Create a DataFrame object
df = pd.DataFrame(fruit_list, columns = ['Name' , 'Price', 'Stock'])

#Add new ROW
df.loc[1]=[ 'Mango', 4, 'No' ]
df.loc[2]=[ 'Apple', 14, 'Yes' ]
print(df)
# -

# ## 2) dic을 행으로 추가하여 pandas 데이터 프레임에 추가 

# python 3.x
import pandas as pd
# List of Tuples
fruit_list = [ ('Orange', 34, 'Yes' )]
#Create a DataFrame object
df = pd.DataFrame(fruit_list, columns = ['Name' , 'Price', 'Stock'])
#Add new ROW
df=df.append({'Name' : 'Apple' , 'Price' : 23, 'Stock' : 'No'} , ignore_index=True)
df=df.append({'Name' : 'Mango' , 'Price' : 13, 'Stock' : 'Yes'} , ignore_index=True)
print(df)

# ## 3) 행을 추가하는 데이터 프레임 append() 메소드

# +
import pandas as pd
fruit_list = [ ('Orange', 34, 'Yes' )]

df = pd.DataFrame(fruit_list, columns = ['Name' , 'Price', 'Stock'])
print("Original DataFrame:")
print(df)
print('.............................')
print('.............................')

new_fruit_list = [ ('Apple', 34, 'Yes','small' )]

dfNew = pd.DataFrame(new_fruit_list, columns = ['Name' , 'Price', 'Stock','Type'])
print("Newly Created DataFrame:")
print(dfNew)
print('.............................')
print('.............................')

#append one dataframe to othher
df=df.append(dfNew,ignore_index=True)
print("Copying DataFrame to orignal...")
print(df)
# -



# # 인덱스 세팅과 재설정

# ## 1) 배정을 통한 인덱스 설정

data = pd.DataFrame(np.arange(16).reshape((4,4,)),
                   index = ['A','B','C','D'],
                   columns = ['가','나','다','라'])
data

# 덮어 쓸땐 길이가 동일 해야한다.
data.index = ['a','b','c','d']
data.columns = ['도','레','미','파']
data

# ## 2) dataframe내의 열을 이용한 인덱스 설정 (set_index 메서드 )

# + active=""
# data.set_index(
#     keys,          # 인덱스로 바꾸려는 열을 선택
#     drop=True,     # 인덱스로 세팅한 열을 dataframe내에서 삭제할지 결정
#     append=False,  # 기존에 존재한 인덱스 삭제 여부 
#     inplace=False, # 원본 객체를 변경할지 선택
#     verify_integrity=False,
# )
# -

data.set_index('도')

# ## dataframe의 index의 리셋 (reset_index 메서드 )
#

# - 만약 멀티 index를 가지고 있다면, level 을 통해서 선택해서 리셋해줄수있다. 

# + active=""
# data.reset_index(
#     level: 'Optional[Union[Hashable, Sequence[Hashable]]]' = None,
#     drop: 'bool' = False,
#     inplace: 'bool' = False,
#     col_level: 'Hashable' = 0,
#     col_fill: 'Label' = '',
# ) -> 'Optional[DataFrame]'
# -

data.reset_index()
