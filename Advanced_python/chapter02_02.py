# Chapter02 - 2
# 파이썬의 magic 메소드 실습
# 파이썬의 중요한 핵심 프레임워크 -> 시퀀스(sequence), 반복(iterator), 함수(Functions), 클래스

# 매직 메소드 기초 설명
# 기본형


print(int)

# 모든 속성 및 메소드 출력
print(dir(int))
print()

n = 100

# 사용
print('ex 1-1 : ', n + 200 )
print('ex 1-2 : ', n.__add__(200)) # + 라고 쓰면 파이썬에서 자동으로 __add__ 로 인식 , 호출됨
print('ex 1-3 : ', n.__doc__)  # 설명해주는 문
print('ex 1-4 : ', n.__bool__(), bool(n))
print('ex 1-5 : ' , n * 100, n.__mul__(100) )

print()

# 클래스 예제
class Student:
    def __init__(self, name, height):
        self._name = name
        self._height = height

    # 파이썬이 이미 가지고 있는것을  우리가 다시 선언해주는 것이다.  - 오버라이딩
    def __str__(self):
        return 'Studnet Class Info : {} {}'.format(self._name, self._height)

    # 오버로딩 : 파이썬이 만든것을 우리가 직접 구현해줌
    def __ge__(self, x):
        print('Called >> __ge__ Method')
        if self._height >= x._height:
            return True
        else:
            return False

    def __le__(self , x):
        print('Called >> __le__ Method')
        if self._height <= x._height:
            return True
        else:
            return False

    def __sub__(self ,x ):
        print('Called >> __sub__ Method')
        return self._height - x._height

# 인스턴스 생성
s1 = Student('James', 181)
s2 = Student('ANN', 165)

# print(s1 >= s2)  # 에러 TypeError: '>=' not supported between instances of 'Student' and 'Student'

print(s1._height > s2._height)

# 매직메소드 출력
print('ex2-1 : ', s1 >= s2 )
print('ex2-2 : ', s1 <= s2 )
print('ex2-3 : ', s1 - s2 )  # 만약 오바로딩하지 않으면 에러가 발생하게 된다.
print(s1 , s2)

print()

# 클래스 예제 2 : 벡터를 계산해주는 클래스
# 벡터 (vector)

class Vector(object):
    def __init__(self, *args):
        """
        Create a vector , example : v = Vecotr(1,2 )
        """
        if len(args) == 0:
            self._x , self._y = 0 ,0
        else:
            self._x , self._y = args

    def __repr__(self):
        return 'Vector(%r, %r)' % (self._x, self._y)

    def __add__(self, other):
        return Vector(self._x + other._x , self._y  + other._y)

    def __mul__(self, y):
        return Vector(self._x * y , self._y  * y)

    def __bool__(self):
        return bool(max(self._x , self._y))


# 벡터 인스턴스 생성
v1 = Vector(  3,5 )
v2 = Vector( 15, 20)
v3 = Vector() # 만약 위에서 선언할때, if 를 사용해서 하지않으면, 아무것도 안넣었을 때 , 오류가 남

# 매직메소드 출력
print('ex 3-1 : ', Vector.__init__.__doc__)
print(v1 , v2 , v3) # Vector(3, 5) Vector(15, 20) Vector(0, 0)
print( 'ex 3-2 : ', Vector.__repr__.__doc__)  #None - doc 을 안적으며 none 이됨
print('ex 3 -3 : ', v1 + v2)
print('ex 3 -4 : ', v1 * 4 )
print('ex 3-5 : ', bool(v1), bool(v2))
print('ex 3-6 : ', bool(v3))