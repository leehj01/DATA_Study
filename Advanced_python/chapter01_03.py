# Chapter01-3
# 파이썬 심화
# 클래스 메소드, 인스턴스 메소드, 스테이틱 메소드

# 기본 인스턴스 메소드
class Student(object):
    """
    Student Class
    Author : Lee
    Data : 2021.05.21
    Description : Class, Static , Instance Method
    """

    # Class Variable
    tuition_per = 1.0

    def __init__(self, id, first_name, last_name, email , grade, tuition , gpa):
        self._id = id
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._grade = grade
        self._tuition = tuition
        self._gpa = gpa

    # 인스턴스 메소드 - self 를 통해서 어떤것을 return 해주는 함수를 인스턴스 메소드라고 함
    def full_name(self):
        return '{} {}'.format(self._first_name , self._last_name)

    # 인스턴스 메소드
    def detail_info(self):
        return 'student Detail Info : {} {} {} {} {} {} '.format(self._id , self.full_name(), self._email, self._grade, self._tuition, self._gpa)


    # 인스턴스 메소드
    def get_fee(self): # 얼만큼 등록금을 내는가 ?
        return 'Before Tuition -> id : {} , fee : {}'.format(self._id, self._tuition)

    # 인스턴스 메서드
    def get_fee_culc(self):
        return 'After Tuition -> id : {} , fee : {}'.format(self._id, self._tuition * Student.tuition_per)

    # 인스턴스 메서드
    def __str__(self):
        return 'Student Info -> name : {} grade {} email {}'.format(self.full_name() , self._grade, self._email)

    # 클래스 메서드 - 아래와 같은 로직도 넣을 수 있다.
    @classmethod # 데코레이터
    def raise_fee(cls , per): # cls 는 클래스가 넘어옴을 의미함 - 여기서는 Student 와 동일
        if per <= 1:
            print('Please Enter 1 or More')
            return
        cls.tuition_per = per  # Student.tuition_per = per 도 같은 의
        print('Succed ! tuition increased !  ')


    # 파이써닉한 코드! - 보통 잘만들어진 코드들은 클래스 메서드를 선언한다 !
    # 클래스 매서드
    @classmethod
    def student_construct(cls, id, first_name, last_name, email , grade, tuition , gpa ):
        return cls(id, first_name, last_name, email , grade, tuition  * cls.tuition_per, gpa)

    #스테이틱 메서드 - 데코레이터가 스테이틱 메서드가 붙으면 편해짐 ..?!
    # 클래스도, 인스턴스랑도 관련이 없을 경우에 사용 - 이렇게 하면 접근하는 방법이 유연해짐 ( 2가지 방법 )
    # cls, self 로 구분하지 않는다. 즉 넘겨받지 않는다. 내가 넘겨받는 인자로만 받는다. 
    # 요즘은 이것이 별로 효율성이 없다!? 라는 의견이 있기도 함 - 밖에서 써도 된다! 라는 의견이 있기도 함
    @staticmethod
    def is_scholarship_st(inst):
        if inst._gpa >= 4.0:
            return '{} is a scholarship recipient.'.format(inst._last_name)
        return 'Sorry , Not a scholarship recipient'


# 학생 인스턴스
student1 = Student(1, 'kim', 'arang', 'dore@naver', '1', 400, 3.5)
student2 = Student(1, 'LEE', 'aram', 'dore@naver', '2', 500, 4.5)

# 기본정보
print(student1.__dict__)
print(student2)

# 전체정보
print(student1.detail_info())
print(student2.detail_info())

# 학비정보 ( 인상전 )
print(student1.get_fee())
print(student2.get_fee())

print()

# 학비 인상 ( 클래스 메소드 미사용 )
# 값은 바뀌게 되지만, 위애 처럼 값을 직접 접근해서 바꾸는것은 좋지 않다.
# 모든 변수가 바라보는 클래스 변수같은 경우에는, 보호가 되어야한다. 즉 캡슐화가 되야한다.
# Student.tuition_per = 1.2

# 클래스 메소드를 사용하여 학비 인상
Student.raise_fee(1.2)

# 학비정보 ( 인상 후 )
print(student1.get_fee_culc())
print(student2.get_fee_culc())


# 클래스 메소드 인스턴스 생성 실습 -  파이써닉한 코드
# 이렇게 클래스 메소드를 사용해서 하는게, 인스턴스를 생성하는구나! 를 분명하게 알수 있기 때문에 좋다!
student3 = Student.student_construct(3, 'Park' ,'minji', 'st@naver', '3', 550, 4.0 )
student4 = Student.student_construct(4, 'JO' ,'ara', 'st@naver', '4', 600, 3.0 )

# 전체 정보
print(student3.detail_info())
print(student4.detail_info())

# 학생 학비 변경 확인
print(student3._tuition)
print(student4._tuition)
print()

# 장학금 혜택 여부 ( 스테틱 메소드 미사용 )
def is_scholarship(inst):
    if inst._gpa >= 4.0 :
        return '{} is a scholarship recipient.'.format(inst._last_name)
    return 'Sorry , Not a scholarship recipient'

print(is_scholarship(student1))
print(is_scholarship(student2))
print(is_scholarship(student3))
print(is_scholarship(student4))

# 하지만, 위에처럼, class 로 묶이는게 아니라, 따로 있을때 -  고치려면 좀 번거러워진다.

print()
#  장학금 혜택 여부 ( 스테이틱 메소드 사용 ) - 1. 클래스로 접근 가능
print(Student.is_scholarship_st(student1))
print(Student.is_scholarship_st(student2))
print(Student.is_scholarship_st(student3))
print(Student.is_scholarship_st(student4))

print()

# 2. 인스턴스로도 사용가능
print('Static : ', student1.is_scholarship_st(student1))
print('Static : ', student2.is_scholarship_st(student2))
print('Static : ', student3.is_scholarship_st(student3))
print('Static : ', student4.is_scholarship_st(student4))

