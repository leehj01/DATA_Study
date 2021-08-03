# chapter 04-2
# 파이썬 심화
# 일급함수 ( 입급 객체)
# 파이썬 함수 특징
# Decorator & Closure

# 파이썬 변수 범위(global)

# 예제1
def func_v1(a):
    print(a)
    print(b)

# 예외
# func_v1(5)  # name 'b' is not defined

# 예제2
b = 10

def func_v2(a):
    print(a)
    print(b)

func_v2(5)

# 예제3

# 실행 되는 순간, b라는 존재에 대해서 알지만(인터프린트가 체크만 함),
# 할당되기 전에 출력을 하려니깐 에러가 발생하게 됨
def func_v3(a):
    print(a)
    print(b)
    b = 5

# func_v3(5)  # local variable 'b' referenced before assignment

# 바이트 코드의 흐름을 체크하는 함수
from dis import dis

print('ex 1-1 -')
print(dis(func_v3)) # 프린트의 호출이 값의 할당보다 빠르다.

# Closure(클로저)
# 반환되는 내부 함수에 대해서 선언된 연결 정보을 가지고 참조하는 방식
# 반환 당시 함수 유효번위를 벗어난 변수 또는 메소드에 직접 접근이 가능하다.

print()

a = 10
print('ex 2-1 -', a+ 10)
print('ex 2-2 -', a+ 100)

# 결과를 누적 할 수 있을 까? - reduce  , sum
print('ex 2-3 -', sum(range(1,51)))
print('ex 2-4 -', sum(range(51,101)))

# 클래스 이용
class Averager():
    def __init__(self):
        self._series = []  # self 의 인스턴스 안에 append 로 누적을 시키고 있기 때문에 - 호출할 떄마다 값이 누적이됨.

    def __call__(self, v):
        self._series.append(v)
        print('class >>> {} / {}'.format(self._series, len(self._series)))
        return sum(self._series) / len(self._series)
# 인스턴스 생성
avg_cls = Averager()

# 누적 확인
print('ex 3-1 - ' , avg_cls(15))
print('ex 3-2 - ' , avg_cls(35))
print('ex 3-3 - ' , avg_cls(40))

# sum 함수 또한 위와 같은 코드로 만들어진 것을 알수 있다.

print()

# 클로저(Closure) 사용
# 전역변수 사용 감소
# 디자인 패턴 적용
# 변수에 대해서 은닉화 / 캡슐화도 가능하다.
# 조심해야하는 점이 몇개 있다.

def closure_avg1():
    # 외부함수와 내부함수의 사이 - Free variable
    # 계속 메모리를 가지고 있기 때문에, 리소스를 너무 소모할 수 있다. - 꼭 필요한 경우만 사용
    series = []  # 반환 당시 함수 유효번위를 벗어난 변수 또는 메소드
    # 클로저 영역
    def averager(v):  # 반환 당시 함수 유효범위
        # series = [] # 이걸 쓰면, 유지가 되지 않음 
        series.append(v)
        print('def >>> {} / {}'.format(series, len(series)))
        return sum(series) / len(series)
    return averager  # averager() 을 하면 안됨 - 이건 실행 상태

avg_closure1 = closure_avg1()

print('ex 4-1 -', avg_closure1(15))
print('ex 4-2 -', avg_closure1(35))
print('ex 4-3 -', avg_closure1(40))

print()

print('ex 5-1-  ', dir(avg_closure1))
print()
print('ex 5-2-  ', dir(avg_closure1.__code__))  # co_freevars 라는 애가 있음
print()
# ('series',) 를 가지고 있음 - 즉 자기 영역밖에 있는 것도 가지고 있음을 확인할 수 있음
print('ex 5-3-  ', avg_closure1.__code__.co_freevars)  #('series',) 가 있음
print()
print('ex 5-4-  ', dir(avg_closure1.__closure__[0])) # closure에도 함수처럼 속성들이 있음
print()
print('ex 5-5-  ', dir(avg_closure1.__closure__[0].cell_contents))


print()
print()

# 잘못된 클로저 사용 예
