# Chapter 06-2
# 파이썬 심화
# 흐름제어, 병행 처리 (Concurrency)
# yeild
# 코루틴(Coroutine)

# yield : 메인 루틴 <-> 서브 루틴
   #  yield 를 만나면 일단 멈쳐있다가, 다른 루틴을 실행했다가 next 를 실행하면 ,멈쳐있는 것이 실행
# 코루틴 제어, 코루틴 상태, 양방향 값 전송
# yield from

# 서브루틴 : 메인루틴에서 -> 리턴에 의해 호출 부부느올 돌아와 다시 프로세스 시작
# 코루틴 : 루틴 실행중 멈춤가능 -> 특정 위치로 돌아갔다가 -> 다시 원래 위치로 돌아와 수행을 가능하게 함. -> 동시성을 프로그래밍을 가능하게 해줌
    # 코루틴으로 generator 을 한 걸 열어보면, NEXT 를 하면, 다시 실행되는 동시성이 가능함.
    # 메인루틴은 진입, 탄출구가 하나이지만, 코루틴은 여러방향으로 동시성을 프로그래밍을 가능하게 해줌
    # 코루틴의 단점은 가독성이 떨어져서, 디버깅을 잘해야함. 하나의 쓰레드만 이용하기 때문에 , 어쩔수 없을 땐 멀티쓰레드를 사용해야함
    # 코루틴은 스케쥴링 오버헤드가 매우 적다.! - 하나의 스레드에서 실행하기 때문에! ( 작은 메모리가 움직이기 때문에 오버헤드가 작다. )
# 쓰레드 : 지금까지는 싱글쓰레드로 했는데, 다음시간에는 멀테쓰레드로 함 -> 좀 복잡함 -> 그 이유는
#     공유되는 자원에 대한 교착 상태 발생 가능성이 있다. 따라서, 주의 깊게 코드를 짜야한다. -> 컨텍스트  스위칭 비용 발생, 자원소비 가능성 증가
    # 멀티 쓰레드나, 코루틴이나 잘 쓰면 상관 없음.
    # 멀티 쓰레드는 컨텍스트 스위칭이라는 스케쥴링이기 때문에 좀 느려지는 경향이있다.

# 코루틴 예제1
def coroutine1():
    print('>>> coroutine started.')
    i = yield  # yield  i 를 쓰면 값을 반환만 할 수 있는데, i = yield 이렇게 선언하면, 메인 루틴한테 값을 받을 수 있음 - 양방향 값을 전송할 수 있음
    print('>>> coroutine received : {}'.format(i))

# 제너레이터 선언
c1 = coroutine1()
print('ex 1-1 -', c1 , type(c1)) # <generator object coroutine1 at 0x000001FFAC033D48> <class 'generator'>

# yield 실행 전까지 진행
# next(c1)
# next(c1) # 또 실행하면, coroutine received : None 이면서 에러가 발생함
# -> 원래 기본으로 None 값 을 전달

# 값 전송
# c1.send(100) # coroutine received : 100

# 잘못된 사용
c2 = coroutine1()

# next(c2) # 이걸 입력하지 않으면, 아래와 같은 TypeError 예외 발생하게 된다.
# c2.send(100) # TypeError: can't send non-None value to a just-started generator

# 코루틴 예제2
# GEN_CREATED : 처음 대기 상태
# GEN_RUNNING : 한번이라도 next를 호출한 상태
# GEN_SUSPENDED : yield 대기 상태
# GEN_CLOSED : 실행 완료 상태

def coroutine2(x):
    print('>>> coroutine started : {}'.format(x))
    y = yield x  # x : 메인루틴한테 전달할 값, y 는 메인 루틴한테 send로 보낼 값
    print('>>> corountine received : {}'.format(y))
    z = yield x + y
    print('>>> corountine received : {}'.format(z))
    # 왼쪽에 있는건 우리가 전달해줘야하는 값, 오른쪽은 우리한테 전송하는

c3 = coroutine2(10)

from inspect import getgeneratorstate # 상태값을 볼수 있는 패키지

print('EX 1-2 - ', getgeneratorstate(c3))

print(next(c3))
# >>> coroutine started : 10
# 10 # 나한테 10을 주고 10을 반환해주기 위 대기상태

print('EX 1-3 - ', getgeneratorstate(c3))  # 대기상태인지 확인하기 위해 출력 - yield 대기 상태

print(c3.send(15))  # 현재 z = yield x + y 서 대기상태

# print(c3.send(20)) # 코루틴  - 예외

print()
print()

# generator 때문에 메인과 서브로 왔다갔다 멀티 쓰레드 처럼 사용할 수 있다.
# 항상 코루틴의 시작은 next 로 해줘야함

# next 메소드를 사용하지 않고 바로 실행하기 위해서, decorator 을 이용하

# 데코레이터 패턴
from functools import wraps # 나한테 전달받는 함수를 모두 wrap - 내부 attribute 의 것을 싸고 가겠다.
def coroutine(func):
    '''    Decorator run until yield    '''
    @wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return primer

@coroutine
def sumer(): # send 로 보내는 함수를 계속 더하는 함수
    total = 0
    term = 0
    while True:
        term = yield total
        total += term



sum_ex = sumer()
print('ex 2-1 -', sum_ex.send(100))
print('ex 2-2 -', sum_ex.send(40))
print('ex 2-3 -', sum_ex.send(60))

# while 이 true라서 계속 반복되게 됨
# 데코레이터를 사용하면, 계속 next 를 안써도 됨