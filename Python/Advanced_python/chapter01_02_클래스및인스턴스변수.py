# chapter01- 2
# 객체 지향 프로그래밍 ( oop ) -> 코드의 재사용, 코드 중복 방지 등
# 클래스 상세 설명, 클래스 변수, 인스턴스 변수

# 클래스 재 선언
class Student():
    """
    Student Class
    Author : LEE
    Data : 2021.05.21
    """

    # 클래스 변수를 선언
    # self 가 없고, 메서드 밖에서 범위를 가지는 함수를 클래스 변수라고 함.
    student_count = 0

    def __init__(self, name , number, grade, details , email = None):
        # 인스턴스 변수들
        self._name = name
        self._number = number
        self._grade = grade
        self._details = details
        self._email = email

        # 객체가 선언될때마다 cnt 가 하나씩 증가하게 된다.
        # 클래스 변수에 접근할때는 클래스이름 . 변수이름 을 적어야함.
        Student.student_count += 1


    # 메소드 들 ..
    def __str__(self):
        return 'str {}'.format(self._name)

    def __repr__(self):
        return 'repr {}'.format(self._name)

    def detail_info(self):
        print('Current ID = {}'.format(id(self))) # 고유의 id 값이 출력됨

        print('Studnet Detail Info : {} {} {}'.format(self._name, self._email, self._details))

    def __del__(self): # 오버라이딩
        Student.student_count -= 1


# self 의미
student1 = Student('cho', 2, 3, {'gender':'M', 'score1':44, 'score2': 80})
student2 = Student('cho', 4, 5, {'gender':'F', 'score1':44, 'score2': 80}, 'lee@naver.com')


# id 값이 다르다 != 가지고 있는 값이 다르다
# id 값은 메모리에 저장된 장소라고 생각하면 된다.
print(id(student1)) #4553099440
print(id(student2)) # 4553099248

print(id(student1) == id(student2)) # False

print(student1._name == student2._name) # 이건 값을 비교하는 것 # True
print(student1 is student2) # 이건 id 를 비교하는 것 # False


# dir 함수, dict 속성값을 확인
# 현업에서는 dict 로 보고 없으면 dir 을 봄 . dir 이 더 자세하나, 코드의 양이 많아짐

print(dir(student1))
# ['__class__', '__del__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_details', '_email', '_grade', '_name', '_number', 'detail_info', 'student_count']
print(dir(student2))

print()

print(student1.__dict__)
#{'_name': 'cho', '_number': 2, '_grade': 3, '_details': {'gender': 'M', 'score1': 44, 'score2': 80}, '_email': None}
# 인스턴스의 속성 값도 가지고 있음. - 필요에 따라서 가져옴
print(student2.__dict__)  # '_email': 'lee@naver.com'}


# Doctstring
# 클래스에 대한 주석을 볼 수 있음
print(Student.__doc__)
print()

# 실행
student1.detail_info()
student2.detail_info()

# 에러
# Student.detail_info() # TypeError: detail_info() missing 1 required positional argument: 'self'

print()

# 클래스로 직접 접근해도, 호출이 가능하다.
Student.detail_info(student1)
Student.detail_info(student2) # 인스턴스화된 변수를 넣어주면 직접 접근 가능 !

print()
# 비교
# class 가 다른 파일에 있거나, 다른 곳에 있을 때, 원형을 알고싶다면 ?!
print(student1.__class__ , student2.__class__)
print(id(student1.__class__) == id(student2.__class__)) # True - 왜냐하면 같은 class 에서 불러온것이기 때문에. 클래스는

# 인스턴스 변수
# 직접 접근 ( PEP 문법적으로 권장 x )
student1_name = 'hahaha'

# 인스턴스 변수 출력 - 인스턴스화 된 변수로 직접 접근해야한다.
print(student1._name , student2._name)
print(student1._email , student2._email)

print()


# 클래스변수
# 접근
print(student1.student_count)
print(student2.student_count)
print(Student.student_count)

print()

# 공유 확인
print(Student.__dict__)
print(student1.__dict__)
print(student2.__dict__)

# 인스턴스 네임스페이스에 없으면, 상위에서 검색  - 파이썬이 알아서 검색!
# 동일한 이름으로 변수 생성가능 == 인스턴스 검색 후 , 상위 클래스 변수나 부모 클래스 변수로 찾음

del student2  # 사실은 del 은 직접 구현해서 사용하지는 않는다.

print(student1.student_count)
print(Student.student_count)