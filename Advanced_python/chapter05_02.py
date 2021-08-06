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
print(v.x)

v.x = 10
print(v.x)
