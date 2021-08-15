# Chapter05-2
# 파이썬 심화
# 파이썬 클래스 관련 메소드 심화 활용 및 상속
# Class ABC

# class 선언
class VectorP(object): # object (이름은 아무거나 해도됨)
    # 파이썬 3점대에서는 메타 클래스를 기본적으로 상속을 받기 때문에 () 도 없어도 됨.
    def __init__(self, x, y):
        self.__x = float(x)
        # 내가 원하는 값을 바로 받을 수 있음
        # if y < 30:
        #     raise ValueError('y below 30 not possible')
        self.__y = float(y)

    # iter 메소드를 오버라이딩해서 사용할 수
    # 아래의 코드를 넣으면 next 코드를 포함시키는 거와 동일
    def __iter__(self):
        # 하나씩 하나씩 보내는 제너레이터, 데이터가 많을 떄는 제너레이터 쓰는 것이 좋음.
        # 한번에 보낼때는 리스트로 감싸줘서 사용해도 됨.
        return ( i for i in (self.__x , self.__y))  # Generator

# 객체 선언
v = VectorP(20, 20)

# print('ex 1-1 -', v.__x, v.__y) # 'VectorP' object has no attribute '__x'
# 위에서 변수를 _ 하나쓰는 게 아니라 __ 두개쓰면, 감쳐져서, 위에처럼 프린트가 안됨 값에 접근이 안됨 - 직접접근이 안됨

# Iter 확인
for val in v:
    print('ex 1-2 - ', val)

# 만약에,
# if y < 30:
        #     raise ValueError('y below 30 not possible')
# 값을 직접 접근하게 만든다면, 생성할때는 30이상인 것만 생성할 수 있지만.
# v._y = 10  이렇게 적어서, 값 자체를 바꿔버리게 할 수 있다.
# 그렇다면 위에서 내가 준 조건은 무용지물이 되버리게 된다..ㅠㅠ

# 그래서 직접 바꾸지 않도록, Getter , Setter 의 개념이 등장한다.
# 그다음 게터 세터의 데코레이트 코딩을 배울 것이다!


# class 선언
class VectorP(object): # object (이름은 아무거나 해도됨)
    # 파이썬 3점대에서는 메타 클래스를 기본적으로 상속을 받기 때문에 () 도 없어도 됨.
    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)
    def __iter__(self):
       return ( i for i in (self.__x , self.__y))  # Generator

    # Getter   # Getter을 먼저 만들고 그다음 Setter 를 만들어야 함.
    # 프로퍼티가 먼저 수행되고 그리고 우리가 하고 싶은거 를 불러오는 구나..
    @property # 데코레이터 달리기 - 콜백으로 선행해주는 동작해주는 기능이 달려있는것
    def x(self):  # 함수이름은 변수 이름을 써줌
        print('Called property x')
        return self.__x # 실제 값을 읽어오는것을 해주고 싶기때문에, 실제값을 넣어주면됨

    @x.setter
    def x(self, v):
        print('Called property x Setter')
        self.__x = v

    @property
    def y(self):  # 함수이름은 변수 이름을 써줌
        print('Called property y')
        return self.__y

    @y.setter
    def y(self, v):
        print('Called property y Setter')
        if v < 30:
            raise ValueError('30 Below is not possible')
        self.__y = float(v)  # 내가 원하는데로 값을 세팅할 수 있다.

# 객체 선언
v = VectorP(20, 40)

# Getter, Setter
print('ex 1-2 -', dir(v), v.__dict__) #  'x', 'y' 가 들어가있음
print('ex 1-3 -', v.x, v.y)

v.x = 10
print(v.x)

# Iter 확인
for val in v :
    print('ex 1-4 -', val)

# __slot__
# 파이썬 인터프리터에게 통보
# 해당 클래스가 가지는 속성을 제한
# __dict__ 는 해시값으로 저장하기 때문에, 많은 데이터가 담길경우, 데이터가 많이 차지할 수 있다. - 램문제가 있는 자료형
# slot 을 사용해서 __dict__ 속상을 최적화 -> 다수 객체 생성시 -> 메모리 사용 공간 대폭 감소
# 해당 클래스에 만들어진 인스턴스 속성 관리에 딕셔너리 대신 Set 형태를 사용
# 지정된 속성만 사용할 수 있다. 그래서 메모리를 감소시킬 수 있다.

class TestA(object):
    __slots__ = ('a', 'b')

class TestB(object):
    pass # slot 을 사용하지 않기 때문에, 해당 인수들을 다 dict으로 관리

use_slot = TestA()
no_slot = TestB()

print('ex 2-1 -', use_slot)
# print('ex 2-1 -', use_slot.__dict__) # AttributeError: 'TestA' object has no attribute '__dict__'
# dict 대신에 set 을 사용

# 어떤 작업을 할지, 설정하고 넣으면 좀더 낫다.- 설계에 맞게 딕이든 slot이든 설정하자
# 머신러닝 처럼 많은 데이터를 넣는 애들의 패키지는 거의 slots 으로 되어있음
print('ex 2-2 -', no_slot)
print('ex 2-3 -', no_slot.__dict__)

# 메모리 사용량 비교 - slot을 사용하는게 더 빠르고, 사이드 이펙트도 존재하지 않는다.
import timeit

# 측정을 위한 함수 선언
def repeat_outer(obj):
    def repeat_inner():
        obj.a= 'TEST'
        del obj.a
    return repeat_inner

print(min(timeit.repeat(repeat_outer(use_slot), number=9000))) # 함수를 내가 원하는 횟수만큼 반복해서 반환해주는 함수
print(min(timeit.repeat(repeat_outer(no_slot), number=9000)))

print()
print()

# 객체 슬라이싱
class Objects:
    def __init__(self):
        self._numbers = [n for n in range(1,100,3)] # 클래스 자체를 리스트 형식으로

    def __len__(self):
        return len(self._numbers)

    def __getitem__(self, idx):
        return self._numbers[idx]


s = Objects()
print('ex 3-1 -', s.__dict__)
# print('ex 3-2 -', len(s)) # 만약 위에서 len 메소드를 구현 안하면, 에러가 남
print('ex 3-2 -', len(s._numbers)) # 하지만, 이거는 위에서 Len 을 구현하지 않아도, 실행이 되낟.
print('ex 3-3 -', s[1:10])
print('ex 3-4 -', s[-1])
print('ex 3-5 -', s[::10])


print()
print()

# 파이썬 추상 클래스
# 참고 : 파이썬 공식 문서https://docs.python.org/ko/3/library/index.html

# 추상 클래스를 사용하는 이유
# 자체적으로 객체 생성 불가
# 상속을 통해서 자식 클래스에서 인스턴스를 생성해야 함
# 개발과 관련된 공통된 내용  ( 필드, 메소드 ) 추출 및 통합해서 공통된 내용으로 작성하게 하는 것
# 폰을 상속받은 객럭시 s3, v30 같은 애들은 자신만의 메소드도 물론 가짐

# Sequence 상속 받지 않았지만, 자동으로 __iter__, __contain__ 기능 작동
# 객체 전체를 자동으로 조사해서 -> 시퀀스 프로토콜이 작동하게 함
class IterTestA():
    def __getitem__(self, idx): # 튜플이나, 리스트 일때 사용하는 건데 그래서 파이썬이 똑똑하므로, iter, contain기능이 자동으로 추가
        return range(1, 50, 2)[idx] # range(1,50,2)
        # 만약 위에 idx 가 없다면, 아래서 슬라이싱을 해도 전체를 가져오게 됨 - 쓸모없어짐

i1 = IterTestA()

print('ex 4-1- ', i1[4])
print('ex 4-2- ', i1[4:10])
print('ex 4-3- ', 3 in  i1[1:10]) # contain method 도 자동으로 들어가져있음
print('ex 4-4- ', [i for i in i1]) #__iter__ 도 동작이됨

print()
print()

# Sequence 상속
# 요구사항인 추상 메소드를 모두 구현해야 동작 - 위에서는 안해도 되지만 여기선 해야함

from collections.abc import Sequence

# 하지만 이렇게 상속을 받는게 FM 이다!
class IterTestB(Sequence):  # Sequence 추상 클래스를 상속 받음
    def __getitem__(self, idx):
        return range(1, 50, 2)[idx] # range(1,50,2)

    def __len__(self, idx):
        return len(range(1,50,2)[idx])

# i2 = IterTestB()  - len 메소드를 만들지 않고 하면 아래와 같은 에러가 발생한다.
# TypeError: Can't instantiate abstract class IterTestB with abstract methods __len__

i2 = IterTestB()
print('ex 4-5- ', i2[4])
print('ex 4-6- ', i2[4:10])

# abc 활용 예제
import abc

# 3.4 이하에서는 metaclass=abc.ABCMeta 라고 적어줘야함 - 나는 3.9임
class RandomMachine(abc.ABC): # 추상클래스로 동작
    # 그 이하 에서는 또 , __metaclass__ = abc.ABCMeta 라고 달아줘야함

    # 추상 메소드 를 선언
    @abc.abstractmethod # 데코레이터
    def load(self, iterobj):
        """iterable 항목 추가"""

    # 추상 메소드
    @abc.abstractmethod
    def pick(self, iterobj):
        '''무작위 항목 뽑기'''

    def inspect(self):
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError: # 더이상 찾는게 없으면 에러를 던져줌
                break
            return tuple(sorted(items))

import random

class CraneMachine(RandomMachine): #RandomMachine 을 상속 받음
    def __init__(self, items):
        self._randomizer = random.SystemRandom() # SystemRandom 의 타임스텝프로 뽑기의 확률을 좀더 다양하게 할수 있다.
        self._items = []
        self.load(items)

    # load, pick 은 추상메소드이므로 아래에서 강제적으로 받아야함
    def load(self, items):
        self._items.extend(items)
        self._randomizer.shuffle(self._items)  # 섞어주기

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('Empty Crane Box')

    def __call__(self):
        return self.pick()

# 서브클래스 확인
# 이 부모인지 확인하는 파이썬 메소드 - 뒤에가 부모
print('ex 5-1 -', issubclass(RandomMachine, CraneMachine))
print('ex 5-2 -', issubclass(CraneMachine, RandomMachine))

# 상속 구조 확인하는 메소드 - 상속의 가계도를 보여주는 것
print('ex 5-3 -', CraneMachine.__mro__)

cm = CraneMachine(range(1, 100)) #  @abc.abstractmethod 가 붙은 부모 메소드는 반드시 자식에서 선언해줘야한다. 즉 오버라이딩 안하면 에러

print('ex 5-4 -', cm._items)
print('ex 5-5 -', cm.pick())
print('ex 5-6 -', cm())
print('ex 5-7 -', cm.inspect()) # 자식에는 없는데 부모가 있는 것들