# Chapter03-2

# 시퀀스형
# 해쉬 테이블 (hashtable)
# Dict -> Key 중복 허용 x , set -> 중복 허용 x
# Dict 및 Set 심화

# Dict 구조
print('EX1-1 -')
# print(__builtins__.__dict__)  # 파이썬에 내장되어있는 것도 딕셔너리로 되어있음

print()
print()

# Hash 값 확인
t1 = (10, 20, (30, 40, 50))
t2 = (10, 20, [30 ,40, 50]) # 중복을 허용 . 가변형 mutable - hash값이 나오지 않고 오류가 발생하게 됨

print('EX1-2 -', hash(t1))
# print('EX1-3 -', hash(t2))# unhashable type: 'list'

print()
print()

# 지능형 딕셔너리 ( Comprehending Dict )
import csv

# 외부 csv to list of tuple

with open('./resources/test1.csv', 'r', encoding='utf-8') as f:
    temp = csv.reader(f)
    #Header skip
    next(temp)
    # 변환
    NA_CODES = [tuple(x) for x in temp]

print('EX2-1 -', )
print(NA_CODES)

n_code1 = {country : code for country , code in NA_CODES}
n_code2 = {country.upper(): code for country, code in NA_CODES}

print()
print()

print('EX 2-2 - ',)
print(n_code1)

print('EX 2-3 - ',)
print(n_code2)

# Dict Setdefault  예제

source = (('k1','val1'),
          ('k1','val2'),
          ('k2','val3'),
          ('k2','val4'),
          ('k2','val5'))

# 키로 사용할 값들이 중복이라, 딕셔너리로 변환하는데 문제가 발생하게 됨 .

# 1. 수동으로 바꿔보기
new_dict1 = {}

# No use setdefault
for k, v in source:
    if k in new_dict1:
        new_dict1[k].append(v)
    else:
        new_dict1[k] = [v]
print('EX 3-1 -', new_dict1)


new_dict2 = {}

# Use setdefault - 성능도 위에보다 더 좋음
for k, v in source:
    new_dict2.setdefault(k, []).append(v)  # 기본적으로 k , [] 넣고 있으면 v 로 append 한다.

print('EX 3-2 -', new_dict1)

# 사용자 정의 dict 상속 ( UserDict 가능 )

class UserDict(dict):
    def __missing__(self, key):
        print('Called : __missing__')
        if isinstance(key , str):
            raise KeyError(key)
        return self[str(key)]

    def get(self, key, default = None):
        print('Called : __gettiem__')
        try :
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key):
        print("Called : __contains__")
        return key in self.keys() or str(key) in self.keys()

user_dict1 = UserDict(one=1, two=2)
user_dict2 = UserDict({'one':1, 'two':2})
user_dict3 = UserDict([('one',1), ('two',2)])

# 출력
print('EX4-1 - ', user_dict1, user_dict2, user_dict3)
print('EX4-2 - ', user_dict2.get('two')) # 만약에 없는 애를 넣으면 NONE 이 호출
print('EX4-3 - ', 'one' in user_dict3 )
# print('EX4-3 - ', user_dict3['three']) # raise KeyError(key)
print('EX4-3 - ', user_dict3.get('three'))  # None 이 나옴
print('EX4-3 - ', 'three' in user_dict3)  # False 가 나옴

print()

# immutable Dict

from types import MappingProxyType

d = {'key1':'test1'}

# Read Only     읽기 전용인 딕셔너리를 만들어줌
d_frozen = MappingProxyType(d)

print('EX5-1 - ', d, id(d))
print('EX5-2 - ', d_frozen, id(d_frozen))

print('EX5-3 - ', d is d_frozen, d==d_frozen) # id는 다르나, 값은 같음

# d_frozen['key1'] = 'test2'  # TypeError: 'mappingproxy' object does not support item assignment

d['key2'] ='test2'

print('EX5-4 - ', d)
print()

# frozen 은 수정도 안된다.

# SET 구조 ( FrozenSet )
s1 = {'Apple','Orange','Apple','Orange','Kiwi'}
s2 = set(['Apple','Orange','Apple','Orange','Kiwi'])
s3 = {3}
s4 = set() # {} 라고 set을 선언하면 안됨 - 이건 딕셔너리 의미
s5 = frozenset({'Apple','Orange','Apple','Orange','Kiwi'})

# 추가
s1.add('Melon')
print('EX6-1 -', s1, type(s1)) # 순서가 유지되지 않는다. 중복은 알아서 배제 됨. 알아서 데이터를 구성해줌
# 그래서 잘못쓰면, 데이터가 굉장히 느려질 수도 있음 - 내부적으로 중복된 데이터를 찾으려고 알고리즘을 돌림

# 추가 불가
# s5.add('Melon')  # AttributeError: 'frozenset' object has no attribute 'add'
print('EX6-2 -', s1, type(s1))
print('EX6-3 -', s2, type(s2))
print('EX6-4 -', s3, type(s3))
print('EX6-5 -', s4, type(s4))
print('EX6-6 -', s5, type(s5))

# 선언 최적화 - 선언할 때, b 보다 a 가 더 최적화하다.
a = {5}
b = set([10])

from dis import dis

print(dis('{10}'))  # 어떤식으로 동작하는지 보여주는 함수


# 지능형 set , comprehending set
from unicodedata import name

print('EX7-1 -')

print({name(chr(i), '')for i in range(0,256)})
print({(chr(i), '') for i in range(0,256)})