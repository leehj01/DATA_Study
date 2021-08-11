# Chapter 06-1
# 파이썬 심화
# 흐름제어, 병행 처리 (Concurrency)
# 제너레이터, 반복형
# Generator

# 파이썬 반복형 종류
# for , collections, text file, list, dict, set, tuple, unpacking, *args
# 공부할 것  : 반복형 객체 내부적으로 iter 함수 내용, 제너레이터 동작 원리, yield from


# 반복 가능한 이유? -> iter(x) 함수 호출

t = 'ABCDEF'

# for 사용
for c in t:
    print('EX 1-1 -', c)

print()

# while 사용

w = iter(t)

while True:
    try:
        print('EX 1-2 - ', next(w))
    except StopIteration as log:
        print(log)
        break


# 추상 클래스
from collections import abc

# 반복형 확인
print('EX 1-3 -', hasattr(t, '__iter__'))
print('EX 1-4 -', isinstance(t, abc.Iterable))
# dir 에 iter 이 있으면 반복형인것을 확인할 수 있다.

print()

# next 사용

class WordSplitIter:
    def __init__(self, text):
        self._idx = 0
        self._text = text.split(' ')

    def __next__(self):
        # print('Called __next__')
        try:
            word = self._text[self._idx]
        except IndexError:
            raise StopIteration('Stop !')
        self._idx += 1
        return word

    def __iter__(self):
        print('Called __iter__')
        return self

    # 매직 메소드 -  메소드 중에서 __로 시작해서 __로 끝나는 메소드들이 있는데 이를 매직 메소드 또는 특별 메소드(special method)라고 부릅니다.
    # 만약 이걸 안적어주면 뭐가 나오는지 알수 없게 됨.
    # <__main__.WordSplitIter object at 0x00000155FF94EB48>
    def __repr__(self):
        return 'WordSplit(%s)' % (self._text)

wi = WordSplitIter('Who says the nights are for sleeping')

print('EX 2-1 -', wi)
print('EX 2-2 -', next(wi))
print('EX 2-3 -', next(wi))
print('EX 2-4 -', next(wi))

# 제너레이터 : 우리가 필요할때, 호출할 때마다 반환하는 것
# 1. 지능형 리스트, 딕셔너리, 집합 -> 데이터 셋이 증가 될경우 메모리 사용량 증가 -> 제너레이터 완화
#    - 100만개를 다 만들어 놓은게 아니라 하나씩 만들어놓는 것
#    - 사람들이 방문할때마다 그떄 필요할때만 가져오도록 하는 것
# 2. 단위 실행 가능한 코루틴(Coroutine) 구현에 아주 중요
# 3. 딕셔너리, 리스트는 한번 호출할 떄마다 하나의 값만 리턴함 .-> 아주 작은 메모리 양을 필요로 함.

print()

# 제너레이터 패턴으로 바꿔서 다시 하기
class WordSplitGenerator:
    def __init__(self, text):
        self._idx = 0
        self._text = text.split(' ')

    def __iter__(self):
        for word in self._text:
            yield word #  제너레이터 - yield 라는 예약어를 사용하면 위에 코드보다 더 단순하게 사용 가능
            # Break 의 에러도 자동으로 파이썬이 해줌
        return

    def __repr__(self):
        return 'WordSplit(%s)' % (self._text)

wg = WordSplitGenerator('Who says the nights are for sleeping')

wt = iter(wg)

print('EX 3-1 -', wt)
print('EX 3-2 -', next(wt))
print('EX 3-3 -', next(wt))
print('EX 3-4 -', next(wt))

# Gnerator

def generator_ex1():
    print('start')
    yield 'AAA'
    print('continue')
    yield 'BBB'
    print('end')

temp = iter(generator_ex1())
# print('ex 4-1 -', next(temp))
# print('ex 4-2 -', next(temp))
# print('ex 4-2 -', next(temp))  # 자동으로 StopIteration 에러발생

for v in generator_ex1():
    pass
    # print('ex 4-3 -', v)

print()

# Generator 예제 2

temp2 = [ x * 3 for x in generator_ex1()]
temp3 = ( x * 3 for  x in generator_ex1())

print('ex 5-1 -', temp2)
print('ex 5-1 -', temp3) # next 함수를 호출하기 전까지는 메모리에 값을 올리지 않음. 함수 형태로 어떻게 나올지만 되어있음

for i in temp2:
    print('ex 5-2 -', i)

for i in temp3:
    print('ex 5-3 -', i)

print()

# Generator 예제 3 ( 자주사용하는 함수)

import itertools

gen1 = itertools.count(1, 2.5) # 1 부터 2.5 씩 무한대로 만들어내고 싶다.
# next가 생성되기 전까지는, 값을 만들지 않고, next 를 만들때 값이 만들어짐 즉, 필요한 값을 미리 만들어 놓지 않는다.
# 만약 그냥 for 문을 쓰면, print 가 무한대로 찍혀서 컴퓨터가 다운될 수 있다..ㅎ
print('ex 6-1- ', next(gen1))
print('ex 6-1- ', next(gen1))
print('ex 6-1- ', next(gen1))
print('ex 6-1- ', next(gen1))
# ... 무한

print()

# 조건
gen2 = itertools.takewhile(lambda n : n< 10, itertools.count(1, 2.5)) # 마지막 조건(종료 조건)을 넣어줌

for v in gen2:
    print('ex 6-5- ', v)

print()

# 필터와 반대되는 함수
gen3 = itertools.filterfalse(lambda x : x < 3 , [ 1,2,3,4,5])

for v in gen3:
    print('ex 6-6 -', v)

# 누적 함계
gen4 = itertools.accumulate([x for x in range(1, 10)])

for v in gen4:
    print('ex 6-7 -', v)

print()

# 연결해주는 메소드 1
gen5 = itertools.chain('ABCDE', range(1,11,2))

print('EX 6-8 -', list(gen5))

# 연결 2
gen6 = itertools.chain(enumerate('ABCDE'))
print('EX 6-9 -', list(gen6))

# 개별로 쪼개주는 메소드
gen7 = itertools.product('ABCDE')
print('EX 6-10 - ', list(gen7)) # 튜플 형태로 개별적으로 쪼개줌

# 연산
gen8 = itertools.product('ABCDE', repeat=2) # 모든 경우의 수를 다 따져줌.
print('EX 6-11 - ', list(gen8)) # 튜플 형태로 개별적으로 쪼개줌

# 그룹화
gen9 = itertools.groupby('AAABBCCCCDDEEE')
# print('EX 6-12 - ', list(gen9))

for chr, group in gen9:  # 반복되는 것을 집합으로 만들어서 따로 보관 해줌 - 형태소 검사나, 단어중요도로 문서 요약 ,어떤 유사도간의 집합을 만들때 이것을 활용할 수 있음
    print('ex 6-12 -', chr, ' : ', list(group))
