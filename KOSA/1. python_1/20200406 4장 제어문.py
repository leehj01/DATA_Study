# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.7.1
#   kernelspec:
#     display_name: PythonWithData 3
#     language: python
#     name: python3
# ---

# ### 4장 제어문
#
# #### 1절 조건문

# +
score = int(input("숫자를 입력하세요. :  "))
if score >= 70 :
    print(f"당신의 점수는 {score}입니다.")
    print("합격했습니다.")
else :
    print(f"당신의 점수는 {score}입니다.")  # 위에랑 같은 코드사용 따라서, if앞에 위치하는 것이 좋다. 
    print("불합격했습니다.")
    print("다음 기회에 도전해주세요.")
    
print("알림을 종료합니다.")

# +
score = int(input("숫자를 입력하세요. :  "))
print(f"당신의 점수는 {score}입니다.")

if score >= 70 :
    print("합격했습니다.")
else : 
    print("불합격했습니다.")
    print("다음 기회에 도전해주세요.")
    
print("알림을 종료합니다.")

# +
score = int(input("숫자를 입력하세요. :  "))
print(f"당신의 점수는 {score}입니다.")

if score > 100 :
    print("점수를 잘못 입력했습니다. ")
elif  score >= 90 :
    print("당신의 등급은 A 입니다.")
elif score >= 80 :
    print("당신의 등급은 B 입니다.")
elif score >= 70 :
    print("당신의 등급은 C 입니다.")
elif score >= 60 :
    print("당신의 등급은 D입니다.")
else:
    print("당신의 등급은 F입니다.")
    
# 하지만 너무 복잡하다. 

# +
score = int(input("숫자를 입력하세요. :  "))
print(f"당신의 점수는 {score}입니다.")

if score > 100 :
    print("점수를 잘못 입력했습니다. ")
elif  score >= 90 :
    grade = "A"
elif score >= 80 :
    grade = "B"  
elif score >= 70 :
    grade = "C"
elif score >= 60 :
    grade = "D"    
else:
    grade = "F"
    
print(f"당신의 등급은 {grade}입니다.")

# 이렇게 하면 더 깔끔한 코드를 얻을 수 있음 

# +
grades = ['F','F','F','F','F','F','D','C','B','A','A']
score = int(input("숫자를 입력하세요. :  "))
if score > 100 :
    print("점수를 잘못 입력했습니다. ")
else :
    print(f"당신의 점수는 {score}입니다.")
    print(f"당신의 등급은 {grades[score//10]}입니다.")

# 이런식으로 더 단순하게 할 수 있음

# -

# #### 2절 조건문
# * 2.1 for 구문

for data in [3,4,5,6]:
    print(data)

# + active=""
# # 자바코드에서
#
# for( int i = 0; i<10; i++) {
#     System.out.printin(i);
# }

# +
l = [1,2,3,4,5,6,7,8]

for data in l :
    print(data)
# -

for index in range(len(l)):
    print(index,l[index])
    
    # 인덱스 번호와 값을 동시에 알 수 있다.
    # 어떤위치에 있는지도 파악이 가능하다. 

a = [1,3,4,516,62,64,767,34,7,8,9,32,45,7,4,6,8,2,5,8]
b = [0]*len(a)  # a의 길이만큼 0 으로 만들어줘야, 채워질 수 있다.
 # 빈셀로는 채워지지 않는다. 

for i in range(len(a)):
    if a[i]%2 == 0:
        b[i] = 2
    else :
        b[i] = 1

b

# +
# 1 부터 100까지 짝수만 출력하세요. print 구문에 end = ' ' 추가

for i in range(0,101,2):
    print(i,end= ' ')
# -

for i in range(1,101):
    if(i%2 ==0):
        print(i,end= ' ')

# +
b = {'dodo':22, 'coco':33, 'soso':44}

for i in b:
    print(i)
# -

# * 2.2 while 구문

i = 0
while i < 10:
    print(i) # 이게 무한 루프가 됨.. 

i = 0
while i < 10:
    i = i +1
    print(i, end = ' ') 

i = 0
while i < 10:
    print(i, end= ' ') 
    i = i +1

i = 0
while i < 100:
    if(i%2 ==0):
        print(i, end= ' ') 
    i = i +1

# +
# 1부터 100까지 합

sum = 0 
for i in range(101):
    sum = sum + i
print("합계 :",sum)
print(f"합계 : {sum}")
# -

# 1부터 100까지 짝수의 합
sum = 0 
for i in range(101):
    if i %2 ==0:
        sum = sum + i
print("합계 :",sum)
print(f"합계 : {sum}")

# +
i = 1
sum = 0
while i <= 100:
    if i % 2 == 0 :
        sum = sum + i
    i = i + 1  # i += 1 도 같은 의미 
    
print("합계 :",sum)
print(f"합계 : {sum}")
# -

# * 2.3. break와 continue
#
#     - 반복문 내에서 break를 만나며 break를 포함하는 반복문을 완전히 탈출
#     - continue는 반복문 내에서 continue이후의 문장을 건너뜀 (skip)

num = 0
while num <10:
    num += 1
    if num ==5:
        break
    print(num, end=' ')
    #num += 1 하면 오류쓰~
    print('aaa')

num = 0
while num <10:
    num += 1
    if num ==5:
        continue
    print(num, end=' ')
    #num += 1 하면 오류쓰~
    print('aaa')

# #### 3절 중첩루프

# * 3.1 2차원 리스트 인덱싱
#     - 반복문 안에 반복문 포함시킬 수 있다.
#     - 2차원 이상의 데이터 구조의 모든 항목들을 처리하기 위해 사용할 수 있음.
#     - 2차원 리스트 인덱싱 : for문 안에 for문은 또 넣어준다.

list_2d = [[1,2,3,4,5],[11,12,13,14,15],[21,22,23,24,25]]
for row in list_2d:
    for data in row:
        print(data, end = " ")
    print()

# * 3.2. 3차원 리스트 인덱싱

list_3d = [
    [[1,2,3,4,5],[11,12,13,14,15],[21,22,23,24,25]],
    [[6,7,8,9,10],[16,17,18,19,20],[26,27,28,29,30]]]
for face in list_3d:
    for row in face:
        for data in row:
            print(data, end = " ")
    print()

# * 3.3. 구구단 출력하기

for i in range(1,10):
    for j in range(2,10):
        #print(f"{i}x{j} ={i*j}")
        print("{}x{}={:>2}".format(j,i,i*j),end = ' ')
    print()

# #### 5절 연습문제

#1 .
while(True):
    num = eval(input("숫자(양의정수)를 입력하세요. :"))
    if(isinstance(num,int) and num >= 0):
        if num%2 ==0 :
            print("짝수입니다.")
        else:
            print('홀수입니다. ')
        break;
    else :
        print("양의 정수가 아닙니다.")
            

#2. 
sum = 0
for i  in range(1,50):
    if i%3 == 0 :
        sum = sum + i
    else :
        pass
print(sum)

# +
# 4.

for i in range(5):
    print('*',end="")

# +
# 4- a

for i in range(5):
    for j in range(5):
        print('*',end='')
    print()

# +
#4-b. 

for i in range(1,6):
    print(i*'*')
    
print('-------------------------')

n = 5
for i in range(n):
    print('*'*(i+1))
    
print('-------------------------')

n= 5
for row in range(n):
    for i in range(row+1):
        print("*", end = '')
    print()

# +
# 4- c

n= 5
for i in range(n):
    for j in range(n-i):
        print("*",end = '')
    print()

# +
# 4-d

n= 5
for i in range(n):
    for j in range(n-i-1):
        print(" ",end = '')
    for j in range(i+1):
        print("*", end = '')
    print()
# -

n= 5
for i in range(n):
    for j in range(0,i):
        print("_",end = '')
    for j in range(i,5):
         print("*", end = '')
    print()

n= 5
for i in range(n):
    for j in range(i+1 , 5):
        print(" ",end = '')
    for j in range(0,(i*2)+1):
        print("*", end = '')
    print()

# * 3.4. 반복문 실행 상태 표시기

import time
progress = ''
percent = 0
num =100
for i in range(1,num+1):
    percent = (i/num)*100
    progress = int(percent*5/10) * '#'
    time.sleep(10)
    print("{:5.1f}%[{:<50s}]{}".format(percent,progress,i),end='\r')

from tqdm import tqdm
result = []
for i in tqdm(range(9000000)):
    result.append(i)

from tqdm import trange
for i in trange(9000000):
    pass # 아무것도 하지 않고, 문법적으로 문장이 필요하지만, 프로그램이 특별이 할일이 없을 때 사용

# #### 4절. 중첩 루프 탈출 

# * 4.1.플래그 이용
#     - 바깥쪽을 둘러싸는 루프의 다음 반복을 이동하거나 한 번에 여러 루프를 종료하려는 경우에는 레이블이 지정된 break를 모방하는 일반적인 방법으로 플래그 값을 지정.
#     

for a in range(0,3):
    break_out_flag = False 
    for b in range(1,3):
        if a == b:
            break_out_flag = True
            break
        print(a,b)
    if break_out_flag:
        break


# * 4.2. 예외처리를 이용한 중첩루프 탈출
#
#     - 바깥 반복문에서 안쪽 반복문을 실행시키기 위해 예외처리 코드를 작성

class BreakOutOfALoop(Exception):pass


for a in range(0,3):
    try:
        for b in range(1,3):
            if a == b: 
                raise BreakOutOfALoop # 예외를 강제로 발생시켜셔
            print(a,b)
    except BreakOutOfALoop: # breakoutofaloop로 실행시키게 함. 
        break
