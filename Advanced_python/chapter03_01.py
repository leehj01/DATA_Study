# chapter 03-1
# 파이썬 심화
# 시퀀스 형
# 컨테이너( container ) : 서로 다른 자료형 ( List, tuple , collections.deque )
# 플렛형 ( Flat ) : 한개의 자료형 ( str, bytes , bytearray , array.array , memoryview )
# 가변 : list, bytearray , array.array  , memoryview , deque
# 불변 : tuple, str , bytes


# 지능형 리스트 ( comprehending lists)

# Non Comprehending List

chars = '!@#$%^&*()_+'
code1 = []
for s in chars :
    code1.append(ord(s))

print('ex 1-1  : ' , code1)

# Comprehending List - 속도 약간 우세
code2 = [ord(s) for s in chars]
print( 'ex 1-2 : ', code2 )  # 성능이 위보다 좋다

code3 = [ord(s) for s in chars if ord(s) > 40 ]
code4 = list(map(ord, chars))
code5  = list(filter(lambda x : x > 40 , map(ord , chars))) # filter(함수, 값 )

print( 'ex 1-3 : ', code3)
print( 'ex 1-4 : ', code4)
print( 'ex 1-5 : ', code5)
print('ex 1-6 : ', [chr(s) for s in code1])


# Generator : iter 는 단순반복, 애네는 값을 생성해냄
# 한번에 한개의 항목을 생성 (메모리 유지 x ) - 성능상에서 압도적으로 좋음
tuple_g = (ord(s) for s in  chars)
print('ex 2-1  : ', tuple_g)  #  <generator object <genexpr> at 0x109c8cac0>
# comprehension 에서 리스트가 아니라 튜플을 쓰면 generator가 생성되고, 값들을 메모리에 생성하지 않고 기다리는 중!
# 반대로, list는 메모리에 다 올리게 됨.

print('ex 2-2 : ', next(tuple_g))
print('ex 2-3 : ', next(tuple_g))


print()

import array

# array
array_g = array.array('i', (ord(s) for s in chars))
print('ex 2-4 : ', array_g)
print('ex 2-5 : ' ,array_g.tolist())

print()

# 제너레이터 예제
print('ex 3-1 : ', ('%s' % c  + str(n) for c in ['A', 'B', 'C','D'] for n in range(1,11)))

for s in ('%s' % c  + str(n) for c in ['A', 'B', 'C','D'] for n in range(1,4)):
    print('ex 3-2 : ', s)

print()

# 리스트 주의 할 점 : 같아보이지만, 주소가 다를 수 있다 !
marks1 = [['~'] * 3 for n in range(3)]
marks2 = [['~'] *3] * 3

# 아래 두개의 값은 같게 보이지만 , 다르다
print('ex 4-1 :' , marks1)
print('ex 4-2 :' , marks2)

print()

marks1[0][1] = 'x'
marks2[0][1] = 'x'

print('ex 4-3 :' , marks1)
print('ex 4-4 :' , marks2)

# ex 4-3 : [['~', 'x', '~'], ['~', '~', '~'], ['~', '~', '~']]
# ex 4-4 : [['~', 'x', '~'], ['~', 'x', '~'], ['~', 'x', '~']]

# 증명
print('ex 4-5 :', [id(i) for i in marks1])
print('ex 4-6 :', [id(i) for i in marks2])

# tuple Advanced
# Packing & Unpacking

# divmod : 두 숫자를 나누어 몫과 나머지를 tuple로 반환
print( 'ex 5-1 :', divmod(100, 9))
print( 'ex 5-2 :', divmod(*(100, 9))) # 자기가 알아서 언패킹이 됨
print( 'ex 5-3 :', *(divmod(100, 9)))


print()

x, y, *rest = range(10)
print('ex 5-4 : ',x , y , rest)
x, y, *rest = range(2)
print('ex 5-5 : ',x , y , rest)
x, y, *rest = 1,2,3,4,5
print('ex 5-6 : ',x , y , rest)

# * : 묶여서 받음, ** : 딕셔너리로 받음

print()

# Mutable(가변 ) vs Immutable(불변)
ㅣ =


