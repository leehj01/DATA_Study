# chapter02-1
# 데이터 모델 ( data model)
# 파이썬의 중요한 핵심 프레임워크 -> 시퀀스(sequence), 반복(iterator), 함수(Functions), 클래스

# 객체 -> 파이썬의 데이터를 추상화
# 모든 객체 -> id , type -> value

a = 7
print(id(a) , type(a), dir(a))

# 일반적인 튜플 사용 - 튜플은 변하지 않음 -> 속도가 리스트보다 빠르게 됨
pt1 = (1.0 , 5.0)
pt2 = (2.5 , 1.5)

from math import sqrt # 제곱을 구하는 공식

line_length1 = sqrt((pt2[0]- pt1[0]) **2 + (pt2[1] - pt1[1]) **2)
print( 'ex1-1   : ', line_length1)

# 네임드 튜플 사용
from collections import namedtuple

# 네임드 튜플 선언
# 네임드 튜플은 클래스로 받아드림
Point = namedtuple('Point', 'x y')

# 두점 선언
pt1 = Point(1.0 , 5.0)
pt2 = Point(2.5 , 1.5)

line_length2 = sqrt((pt2.x - pt1.x) ** 2 + (pt2.y - pt1.y ) **2)
print( 'ex1-2   : ', line_length2)

# 이렇게 코드를 쫘주면, 위에서는 인덱스를 가지고 길이를 구해줬기 때문에, 실수 할수 있지만, 여기서는 x, y 가 나오면서 보다 분명해졌다.
# 클래스를 사용한 것같은 느낌이 된다.

print('ex1-3 : ', line_length2 == line_length1)


# 네임드 튜플 선언 방법
Point1 = namedtuple('Point',[ 'x', 'y'])  # 리스트를 넣어도됨
Point2 = namedtuple('Point', 'x, y')
Point3 = namedtuple('Point', 'x y') # 공백을 넣어도되지만, 가능하면 리스트나 , 를 넣어주기
Point4 = namedtuple('Point', 'x y x class', rename= True) # 튜플은 중복을 허용하지 않는데 , x 가 2개 들어가있고, class 는 예약어인데 사용할 수 없음 - 그럼 원래는  에러가 남 = 하지만?! 아래서 확인!
# rename = False 가 디폴트이다.

# 출력
print('ex2 -1 : ' , Point1, Point2, Point3, Point4)
# ex2 -1 :  <class '__main__.Point'> <class '__main__.Point'> <class '__main__.Point'> <class '__main__.Point'>
# 클래스 형태로 되어있음 - 객체를 선언


# dict to unpacking
temp_dict = { 'x' : 75,   'y' : 55}


# 객체를 생성
p1 = Point1(x = 10 , y = 35) # ( 10 , 35 ) 를 하면 순서대로 넣어지는데  지정해도됨
p2 = Point2(20 , 40)
p3 = Point3(45 , y  = 20)
p4= Point4(10 , 20, 30 ,40)
p5 = Point3(**temp_dict) # Point(x=75, y=55) 언페킹을 이용해서도 할 수 있음

print( ' ex2-2 :' , p1, p2, p3, p4 , p5)

# p4 > Point(x=10, y=20, _2=30, _3=40) 원래는 중복되고 예약어라 오류가 나야하지만 , 얘가 알아서 _2, _3 로 값을 바꿔줌
# 보통은 이렇게 중복되게 하지만, ! 혹시 다른곳에서 가져왔을 경우에는 rename 을 true로 주고 확인한다.
# rename을 false 로 주면, 에러가 발생하게 된다.

print()

# 사용
print( 'ex3 -1 : ', p1[0] + p2[1])  # 튜플의 사용을 그대로 가지고 있기 때문에 인덱싱도 가능
# 하지만, 인덱싱을 할거라면 namedtuple 을 사용하지 않았을 것
print('ex3 -2 : ', p1.x + p2.y)  # 클래스 변수 접근 방식

# 언패킹
x , y = p3  # x, y 에 p3 를 넣기
print( 'ex3-3  : ' ,x + y)

# rename 테스트
print('ex3-4 : ', p4 )

print()

# 네임드 튜플 메소드
temp = [ 52,38]

# _make() : 새로운 객체 생성
p4 = Point1._make(temp)

print('ex4-1 : ', p4) # 개수가 안맞으면 패킹이 되서 알아서 들어가지게 됨

# _fields :  필드 네임 확인
print('ex4-2 : ', p1._fields, p2._fields, p3._fields)


# _asdict() : 정렬된 딕셔너리로 반환
print('ex4-3 : ', p1._asdict(), p2._asdict(), p4._asdict())
print(dict(p1._asdict())) # 딕셔너리로 정렬 가능


# _replace() : 수정된 '새로운' ( id 값이 달라짐 ) 객체 반환
print('ex 4-4 : ', p2._replace(y =100))

print()

# 실사용 실습
# 학생 전체 그룹 생성
# 반 20명 , 4개의 반 -> ( a, b, c, d ) 번호

Classes = namedtuple('Classes', ['rank','number']) # 이름을 변수랑 같게하는게, 규칙이라고 함

# 그룹 리스트 선언 - 지능형 리스트 . list comprehension
numbers = [str(n) for n in range(1,21)]
print(numbers)

ranks = 'A B C D'.split(' ')
print(ranks, numbers)

# list Comprehension
students = [Classes( rank , number) for rank in ranks for number in numbers ]

print(students)  # 이런식으로 굉장히 빠르게 구조체를 만들 수 있음
print(len(students))
print(students[4].rank) # 딕셔너리를 사용하듯 이런식으로 사용할 수 있다.

# 가독성이 안좋은 케이스 - 추천하진 않음 : 리스트컨프리헨션을 남발하면가독성이 떨어짐
students2 = [Classes(rank, number)
             for rank in 'A B C D'.split(' ')
                 for number in [str(n)
                        for n in range(1,21)]]
print(students2)

# 출력
for s in students:
    print('ex 7-1', s)