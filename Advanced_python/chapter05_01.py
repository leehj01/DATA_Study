# Chpter-01-01
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