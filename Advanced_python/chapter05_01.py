# Chpter-05-01
# 파이썬 참조 심화
# 파이썬 객체 참조 다양한 특징 Python Object Referrence- copy 얕은 복사 , deep copy 깊은 복사
# 매개변수 전달 주의할 점


print('ex 1-1 - ')
print(__name__)

# id vs __eq__ ( == ) 증명
x = {'name':'kim', 'age':33, 'city':'Seoul'}
y = x

print('ex 2-1 -', id(x), id(y))
print('ex 2-2 -', x == y )
print('ex 2-3 -', x is y )
print('ex 2-4 -', x, y)

x['class'] = 10
print('ex 2-5 -', x, y )  # 객체가 같은 주소값을 가지고 있기 때문에, 주의해야한다. y 도 바뀐다.

z = {'name':'kim', 'age':33, 'city':'Seoul', 'class': 10}

print('ex 2-6 -', x, z)
print('ex 2-7 -', x is z ) # 같은 객체
print('ex 2-8 -', x is not z) # 아이디는 다름
print('ex 2-9 -', x == z ) # 값은 같음

# 객체 생성 후 완전 불변 => 즉, id는 객체 주소(정체성)비교 , ==(__eq__) 는 값 비교
# 값이 많을 경우는 비교하는데 많은 시간이 걸리기 때문에 같은걸 판별할때는 Is를 먼저 판별하고 == 을 사용한다.

# 튜플 불변형의 비교
tuple1= (10,15, [100,1000])
tuple2= (10,15, [100,1000])

print('ex 3-1 -', id(tuple1), id(tuple2))
print('ex 3-2 -', tuple1 is tuple2)
print('ex 3-3 -', tuple1 == tuple2)
print('ex 3-4 -', tuple1.__eq__(tuple2))


# copy 얕은 복사 , deep copy 깊은 복사

# Copy
tl1 = [10, [100, 105], (5, 10, 15)]
tl2 = tl1
tl3 = list(tl1) # 생성자를 통해 넣어줘야 다른 id값을 가지게 됨.

print('ex 4-1 -', tl1 == tl2)
print('ex 4-2 -', tl1 is tl2)
print('ex 4-3 -', tl1 == tl3)
print('ex 4-4 -', tl1 is tl3)


# 증명
tl1.append(1000)
tl1[1].remove(105)

print('ex 4-5 -', tl1)
print('ex 4-6 -', tl2)
print('ex 4-7 -', tl3)

print()

print('튜플 변경전 ' , id(tl1[2]))
tl1[1] += [110, 120]
tl1[2] += (110, 120)

print('ex 4-8 -', tl1)
print('ex 4-9 -', tl2)  # 튜플이 재할당됨 - 튜플은 불변이라서 합산해서 새로운 id값이 되었다고 볼수 있다.
print('ex 4-10 -', tl3)
print('튜플 변경 후 ' , id(tl1[2]))

# 튜플의 값이 달라짐을 볼수 있다. 즉, 튜플을 리스트에 넣어서 값을 할당하는 것은 안전하지 않다고 볼수 있다.

print()
print()


# Deep Copy
class Basket :
    def __init__(self, products = None):
        if products is None:
            self._products = [] # 상품을 안넣었으면 빈 리스트!
        else:
            self._products = list(products) # 상품을 넣었으면, 리스트가 생성되고,

    def put_prod(self, prod_name):
        self._products.append(prod_name)

    def del_prod(self, prod_name):
        self._products.remove(prod_name)

import copy

basket1 = Basket(['Apple', 'Bag', 'Tv', 'Snack', 'Water'])
basket2 = copy.copy(basket1)
basket3 = copy.deepcopy(basket1)

print('ex 5-1 -', id(basket1), id(basket2), id(basket3))  # 객체를 복사하니깐, id가 다 다름을 확인할 수 있다.
print('ex 5-2 -', id(basket1._products), id(basket2._products), id(basket3._products)) # 하지만 안의 존재하는 product1 ,2 는 같다.. - 이러면 큰일남

# 경우에 따라서, 얕은 복사, 깊은 복사를 잘 선택해야한다.

basket1.put_prod('Orange')
basket2.del_prod('Snack')

print('ex 5-3 -', basket1._products) # Snack 도 빠져있음이 보임
print('ex 5-4 -', basket2._products) # Orange 도 포함되어있음
print('ex 5-5 -', basket3._products)

# 함수 매개변수 전달 사용법

def mul(x,y):
    x += y
    return x

x = 10
y = 5

print('ex 6-1 - ', mul(x,y), x, y)

print()

a = [10, 100]
b = [5, 10]
print('ex 6-2 - ', mul(a, b), a, b)
# 처음에 a가 들어갔고, 그게 변경되었다. 위에서 정수는 안변했는데, 이건 변경됨
# 가변형일때는 원본 데이터가 변경됨

c = (10, 100)
d = (5, 10)
print('ex 6-3 - ', mul(c, d), c, d)
# 아이디값은 변경되지 않음.  튜플 - 불변형은 변경되지 않음

# 데이터 구조에 맞춰서, 변경이 가능한지 안가능한지에 따라서 데이터 타입을 정해서 함수에 넣어줘야함

# 파이썬 불변형 예외
# 불변형인데 복사를 하지 않고, 같은 주소값을 보는 형
# str, bytes, frozenset, Tuple : 사본생성을 하지 않고 그냥 바로 참조를 반환
# frozenset : 아에 불변으로 만드는 데이터

tt1 = (1,2,3,4,5) # 오리지널 하나의 자료형 - 안에 리스트나 그런것 없이
tt2 = tuple(tt1) # 보통 생성자를 감싸서 쓰면, 복사가 됨.
tt3 = tt1[:]

# 하지만 튜플의 경우는 굳이 필요없기 때문에, 깊은 복사가 되지 않음.
# 사본생성이 되지 않음
print('ex 7-1 - ', tt1 is tt2, id(tt1), id(tt2))
print('ex 7-2 - ', tt1 is tt3, id(tt1), id(tt3))

tt4 = (10, 20, 30, 40, 50)
tt5 = (10, 20, 30, 40, 50)
ss1 = 'Apple'
ss2 = 'Apple'

print('ex 7-3 - ', tt4 is tt5, tt4 == tt5 , id(tt4), id(tt5))
print('ex 7-3 - ', ss1 is ss2, ss1 == ss2 , id(ss1), id(ss2))
# 문자열도, 같다고 생각함 참조값을 반환함. id값이 똑같음
