# chapter 04-1
# 파이썬 심화
# 일급함수 ( 입급 객체)
# 파이썬 함수 특징
# 1. 런타임 초기화
# 2. 변수 등에 할당 가능
# 3. 함수 인수 전달 가능 ex, sorted(key = len)
# 4. 함수 결과로 반환 가능 return funcs - 자기 자신을 호출해서 재귀함수로 사용가능 혹은 데코레이터


# 함수 객체 예제

def factorial(n):
    """Factorial Funciton -> n:int"""

    if n ==1 : # n < 2
        return 1

    return n * factorial(n-1)

class A :
    pass


print('ex-1 - ', factorial(10))
print('ex-2 - ', factorial.__doc__)
print('ex-3 - ', type(factorial), type(A))
print('ex-4 , ', set(dir(factorial)) - set(dir(A))) # 가지고 있는 함수를 확인할 수 있음
 # def 와 class 가 가지고 있는 함수의 차이. 함수만 가지고 있는 속성 : closeure, globals 등이 있음

print('ex1-5 ', factorial.__name__)
print('ex1-6 ', factorial.__code__)

print()
print()

# 변수 할당
var_func = factorial

print('ex 2-1 - ', var_func) # 변수를 할당하는 것을 확인
print('ex 2-2 - ' , var_func(5)) # 변수를 실행
print('ex 2-3 - ', map(var_func, range(1,6)))
print('ex 2-3 - ', list(map(var_func, range(1,6))))

# 함수의 인수 전달 및 함수로 결과 반환 -> 고위 함수(Highter-order Function)

# 필터함수 안에 익명 함수를 넣어서 실행 - [ 1,3, 5 ] 만 실행
# 여기서, 1 은  true , 0 은  false
print('ex 3-1 - ', list(map(var_func, filter(lambda x:x%2, range(1,6)))))
# 위와 아래가 같은 결과가 나옴.
print('ex 3-2 -', [var_func(i) for i in range(1,6) if i % 2])

# reduce() - 권장하지는 않지만 알고있어야하는 함수
# 횟수를 감소시키면서, 값들을 가지고 싶을 때 사용하는 것
from functools import reduce
from operator import add

# 1을 더해주고, reduce 가 가지고 있음. 마지막은 1~10 까지 다 더한 값이 됨
print('ex 3-3 - ', reduce(add, range(1,11)))
# 하지만 위의 코드를 아래처럼 사용할 수 있음.
print('ex 3-4 - ', sum(range(1,11)))

# sum 이 낫지만, limit 을 주고 위와 같은 누적의 결과를 사용하면 됨...

# 익명함수 (lambda)
# 가급적 주석 사용
# 가급적 함수 사용
# 너무 많이 사용하면, 가독성이 좋지 않으므로, 필요한 경우 잘 쓰자!
# 일반 함수 형태로 리팩토링 권장

print('ex 3-5 - ', reduce(lambda x, t : x + t, range(1,11)))
# 처음에는 1~10 이라면, range의 값이 x = 1 , t = 2 -> x = (1+2)  t = 3 ,
# x = ( 1+2+3)  t= 4 가 됨..


# Callable : 호출 연산자 -> 메소드 형태로 호출 가능한지를 확인하는 것
# 매직 메소드 __call__ - 호출이 가능하다는 의미
# func() 를 사용해서 함수를 호출하듯이 호출해서 가능하는 의미


# 로또 추첨 클래스 선언

import random
class LottoGame:
    def __init__(self):
        self._balls = [n for n in range(1,46)]

    def pick(self):
        random.shuffle(self._balls)
        return sorted([random.choice(self._balls) for n in range(6)])  # 6번 뽑음

    # 함수처럼 쓰기 위해서 call 을 오버라이딩 해주기
    def __call__(self):
        return self.pick()

# 객체 생성
game = LottoGame()

# 게임 실행
print('ex 4-1 - ', game.pick())

# 호출 가능 확인
print('ex 4-2 - ', callable(str), callable(list), callable(3.14), callable(game))  # callable 에 넣으면 호출이 가능한지를 확인 할 수있다.

# -> LottoGame() 은 이렇게 사용이 안된다. 이걸 가능하게 하면, 조금더 편하기 때문에 call 을 오버로딩 해서 쓰면, 함수처럼 사용가능하게 된다.


print('ex 4-3 - ', game())
print('ex 4-4 -', callable(game))  # call 을 넣어주면, callable 해줌

print()
print()

# 다양한 매개변수 입력 ( *args , **kwargs ) - unpacking , packing
def args_test(name, *contents, point=None, **attrs):
    return '<args_test> -> ({})({})({})({})'.format(name, contents, point, attrs)

print('ex 5-1 -', args_test('test1')) # contents 는 패킹해서 넣기 때문에 tuple 형태로, attrs 는 딕셔너리 형태로 넣어진다.
print('ex 5-2 -', args_test('test1', 'test2'))
print('ex 5-3 -', args_test('test1','test2','test3',id ='admin'))
print('ex 5-4 -', args_test('test1','test2','test3',id ='admin', point=7))
print('ex 5-4 -', args_test('test1','test2','test3',id ='admin', point=7, password='1234'))


print()
print()

