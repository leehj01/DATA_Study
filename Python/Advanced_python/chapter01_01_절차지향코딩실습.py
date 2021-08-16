# chapter01- 1
# 객체 지향 프로그래밍 ( oop ) -> 코드의 재사용, 코드 중복 방지 등
# 클래스 상세 설명, 클래스 변수, 인스턴스 변수


# 리스트 구조
student_names_list = ['Kim','Lee','Park']
student_numbers_list = [1,2,3]
student_grades_list = [1,2,4]
student_details_list = [
    {'gender':'Male', 'score1':95 , 'score2' : 88},
    {'gender':'FeMale', 'score1':77 , 'score2' : 88},
    {'gender':'Male', 'score1':95 , 'score2' : 88},
]

# 삭제
del student_names_list[1]
del student_numbers_list[1]
del student_grades_list[1]
del student_details_list[1]

print(student_names_list, student_numbers_list, student_grades_list)
print(student_details_list)

# 딕셔너리 구조 도 굉장히 귀찮음 -  서드파티 ( 외부의 있는 것 ) 과 비슷한 구조, 하지만 직접짜는것은 매우 비효율적이다

# 클래스 구조: 구조 설게 후 재사용성 증가, 코드 반복 최소화, 메소드 활용

class Student(): # 클래스
    def __init__(self, name, number, grade,details):  # 생성자
        self._name = name
        self._number = number
        self._grade = grade
        self._details = details

    # 우선순위는 str - > repr 이며, 둘다 없으면 그냥 객체를 반환
    def __str__(self):
        return 'str : {}'.format(self._name)

    def __repr__(self):
        return 'repr : {} - {}'.format(self._name , self._number)


student1 = Student( 'Kim' ,1,  1 , {'gender':'Male', 'score1':95, 'score2' : 30})
student2 = Student( 'Lee' ,2,  1 , {'gender':'FeMale', 'score1':95, 'score2' : 30})
student3 = Student( 'Park' ,3,  1 , {'gender':'Male', 'score1':95, 'score2' : 30})


print(student1.__dict__)  # student1 에 어떤값이 들어갔는지 다 확인할 수 있다. - 이건, 파이썬이 만들어졌을 때부터 이렇게 된거다!
print(student1, student2, student3)


student_list  = []

student_list.append(student1)
student_list.append(student2)
student_list.append(student3)

print()
print(student_list)

# [<__main__.Student object at 0x10f7635e0>, <__main__.Student object at 0x10f7634f0>, <__main__.Student object at 0x10f763460>]


# __str__
for x in student_list:
    print(repr(x))  # print 에 repr 이라는 메소드가 있음
    print(x)
#str : Kim  # str   함수가 있기 때문에, print() 해줬을때, lee 가 나오게된다. str 함수가 없다면, 그냥
# <__main__.Student object at 0x10f7635e0> - 가 나오게 된다.
# str : Lee
# str : Park
