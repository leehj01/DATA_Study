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

# # 1. 데이터 타임 변환하기

import pandas as pd
data = pd.read_csv('datatime_exa.csv')
data.info()

data

# ## 1.1. to_datetime()
# - 판다에 있는 함수를 사용하여 데이터 타입으로 변환
# - 속도가....느리다.

data = pd.read_csv('datatime_exa.csv')

data['time'] = data['time'].astype('str')
data['time'] =  pd.to_datetime(data['time'])

data

# ## 1.2. apply() 함수를 이용한 방법
# - 판다스의 apply함수는 argument로 특정함수와 데이터를 넘겨주게 되면 결과값을 반영되게 됨.
# - 위의 방법보다 apply 방법이 더 성능이 좋다는 의견이 있다고함. 

import datetime

data = pd.read_csv('datatime_exa.csv')
data['time'] = data['time'].astype('str')

data.time = data.time.str[:8]
data['time'] = data['time'].apply(lambda _ : datetime.datetime.strptime(_, '%Y%m%d'))

data['time'] = data['time'].apply(lambda x : x[0:4]+'-'+x[4:6] +'-'+ x[6:8]+ ' '+x[8:10]+ ':'+x[10:12]+ ':'+x[12:14])
data['time'] = data['time'].apply(lambda _ : datetime.datetime.strptime(_, '%Y-%m-%d %H:%M:%S'))

data

data = pd.read_csv('datatime_exa.csv')
data['time'] = data['time'].astype('str')
data['time'] = data['time'].apply(lambda x : x[0:4]+'-'+x[4:6] +'-'+ x[6:8]+ ' '+x[8:10]+ ':'+x[10:12]+ ':'+x[12:14])
data['time'] = pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M:%S', errors='raise')

data


def tranform_datetype(x):
    x = str(x)
    year = int(x[:4])
    month = int(x[4:6])
    day = int(x[6:8])
    hour = int(x[8:10])
    minu = int(x[10:12])
    sec = int(x[12:])
    return datetime.datetime(year, month, day, hour, minu, sec)


data = pd.read_csv('datatime_exa.csv')
data['time'] = data['time'].apply(tranform_datetype)

data

# # 2. 시간을 연/월/일/ 시/분/초 로  나누기
# ## 2.1. lambda 함수사용
# - 단점 : 데이터의 양이 많을때는 시간이 많이 걸린다. 
#          주어진 데이터의 형식이 일정해야 사용할 수 있다.

data = pd.read_csv('datatime_exa.csv')

data

data['year'] = data['time'].map(lambda x : int(str(x)[:4]))
data['month'] =  data['time'].map(lambda x : int(str(x)[4:6]))
data['day'] =  data['time'].map(lambda x : int(str(x)[6:8]))
data['hour'] = data['time'].map(lambda x : int(str(x)[8:10]))
data['min'] = data['time'].map(lambda x : int(str(x)[10:12]))
data['sec'] = data['time'].map(lambda x : int(str(x)[12:14]))

data

# ## datetime 함수 이용

data = pd.read_csv('datatime_exa.csv')
data['time'] = data['time'].astype('str')
data['time'] = data['time'].apply(lambda x : x[0:4]+'-'+x[4:6] +'-'+ x[6:8]+ ' '+x[8:10]+ ':'+x[10:12]+ ':'+x[12:14])
data['time'] = data['time'].apply(lambda _ : datetime.datetime.strptime(_, '%Y-%m-%d %H:%M:%S'))

# +
data['date']       = data['time'].dt.date  
data['year']       = data['time'].dt.year         # 연(4자리숫자)
data['month']      = data['time'].dt.month        # 월(숫자)
data['month_name'] = data['time'].dt.month_name() # 월(문자)

data['day']        = data['time'].dt.day          # 일(숫자)
data['all_time']   = data['time'].dt.time         # HH:MM:SS(문자)
data['hour']       = data['time'].dt.hour         # 시(숫자)
data['minute']     = data['time'].dt.minute       # 분(숫자)
data['second']     = data['time'].dt.second       # 초(숫자)
# -

data

data['quarter']       = data['time'].dt.quarter       # 분기(숫자)
data['day_name']      = data['time'].dt.day_name()       # 요일이름(문자) (=day_name())
data['weekday']       = data['time'].dt.weekday       # 요일숫자(0-월, 1-화) (=dayofweek)
data['weekofyear']    = data['time'].dt.weekofyear    # 연 기준 몇주째(숫자) (=week)
data['dayofyear']     = data['time'].dt.dayofyear     # 연 기준 몇일째(숫자)
data['days_in_month'] = data['time'].dt.days_in_month # 월 일수(숫자) (=daysinmonth)

data

# # 3. 기타
# - add datetime : 데이트 타임의 시간을 늘리거나 뺄 수 있다.

import datetime
data = pd.read_csv('datatime_exa.csv')
data['time'] = data['time'].astype('str')
data['time'] = data['time'].apply(lambda x : x[0:4]+'-'+x[4:6] +'-'+ x[6:8]+ ' '+x[8:10]+ ':'+x[10:12]+ ':'+x[12:14])
data['time'] = data['time'].apply(lambda _ : datetime.datetime.strptime(_, '%Y-%m-%d %H:%M:%S'))
data['time_add'] = data['time']
data['time_subtract'] = data['time']
data['time_add'] += datetime.timedelta(days = 1)
data['time_subtract'] -= datetime.timedelta(days = 1)

data


