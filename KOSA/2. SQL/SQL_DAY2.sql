-- 3-2 문자함수

SELECT * from dual;
select sysdate from employees;
select sysdate from dual;

select initcap('Javaspecialist') from dual;

select lower('Javaspecialist') from dual;
select upper('Javaspecialist') from dual; -- 소문자로 바꿔줌

select length('Javaspecialist') from dual; -- 문자의 수
select lengthb('자바전문가') from dual;  -- bite 수를 알려줌 
-- utf-8 3bye


select concat('Java' , 'Specialist') from dual; -- 인수를 두개밖에 안됨. 
select 'Java' || 'Specialist'||'abc' from dual; -- 세개를 연결하려면, || 사용
select substr('Javaspecialist',5,7) from dual; -- 내가 원하는 부분을 가져옴
select substrb('Javaspecialist',4,3) from dual; -- byte를 기준으로 뽑기
select instr('Javaspecialist','s') from dual;  -- 's' 문자가 몇번째 있는지 찾기
select instr('Javaspecialist','s',5) from dual;

select lpad(17600,10,'*') from dual; -- 10자리인데, 나머지는  * 로 채워주세요
select rpad('java',10,'-') from dual; -- 오른쪽에 나머지 자리를 출력
select rpad(first_name,10,'*') from employees ; 

select ltrim('Javaspecialist','Jav') from dual; -- 왼쪽에서 오른쪽 문자를 하나하나 비교하는것.
-- java 통채로 지워지는 이유는 Jav 에  a 가 중복으로 들어가있기 때문이다. 
select Rtrim('Javaspecialist','list') from dual; -- 단어를 통채로 보는 것이 아니라, 하나하나 보는것
select Rtrim('Javaspecialist  ') from dual; -- 안적어주면 공백을 지워줌
select trim('      Javaspecialist   ') from dual; -- trim은 앞뒤의 공백을 지워줌
select Replace('Javaspecialist','Java','BigData') from dual;
select Replace('Java   spe cialist',' ','') from dual; -- 문자 중간의 공백을 없앨수 있음
select translate('Javaspecialist','abcdefghijks','1234567890') from dual;
-- 문자를 하나씩 매핑 시키는 것. 매핑될게 없으면, 삭제되고, / 값이 없으면 원본 그대로 나옴 


SELECT 
    RPAD(substr(first_name,1,3), Length(first_name),'*') as name,
    LPAD(salary, 10, '*') as salary
FROM
    employees
WHERE
    lower(job_id) = 'it_prog';
    
    
-- 3.3. 정규 표현식

CREATE TABLE test_regexp (col1 varchar2(10)); -- 테이블 생성
DROP TABLE  test_regexp; -- 테이블 삭제

insert into test_regexp values ('ABCDE01234');
insert into test_regexp values ('01234ABCDE');
insert into test_regexp values ('abcde01234');
insert into test_regexp values ('01234abcde');
insert into test_regexp values ('1-234-5678');
insert into test_regexp values ('234-567890');
commit;
-- 디스킷에 저장하려는 것. 만약 하지않으면, 메모리에만 들어가고 다시 들어가면 저장이 안되어있음
DELETE from test_regexp;  -- 전체 행을 다 삭제하는 것. 

select *
from test_regexp;

-- 3.2. regexp_like 함수
select *
from test_regexp
where regexp_like(col1, '[0-9][a-z]');

select *
from test_regexp
where REGEXP_LIKE(col1,'[0-9]{3}-[0-9]{4}$');

select *
from test_regexp
where REGEXP_LIKE(col1,'[[:digit:]]{3}-[[:digi:]]{4}$');

select *
from test_regexp
where REGEXP_LIKe(col1, '[[:digit:]]{3}-[[:digi:]]{4}');

-- 3.3 regexp_instr 함수
insert into test_regexp values('@!=)(9&%$#');
insert into test_regexp values('자바3');

select col1,
    regexp_instr(col1, '[0-9]') as data1,
    regexp_instr(col1, '%') as data2
from test_regexp;

-- 3.4. regexp_substr 함수

select col1, regexp_substr(col1,'[C-Z]+')
FroM test_regexp;

-- 3.5. regexp_replace함수

select col1, regexp_replace(col1, '[0-2]+','*')
from test_regexp;


--3.6. gegexp 함수 실전 문제

select first_name, phone_number
from employees
where regexp_like (phone_number, '^[0-9]{3}.[0-9]{3}.[0-9]{4}$');

select first_name, phone_number
from employees
where regexp_like (phone_number,'^[[:digit:]]{3}.[[:digit:]]{3}.[[:digit:]]{4}$');

select first_name,
    regexp_replace(phone_number, '[[:digit:]]{4}$','****') as phone,
    regexp_substr(phone_number, '[[:digit:]]{4}$') as phone2
from employees
where regexp_like (phone_number,'^[0-9]{3}.[0-9]{3}.[0-9]{4}$');
 

-- 4. 숫자 함수

SELECT * from employees where department_id = 90;

select round(123.4567,2) from dual;

select round(-3.4), trunc(-3.4), ceil(-3.4), floor(-3.4) from dual;
select round(-3.6), trunc(-3.6), ceil(-3.6), floor(-3.6) from dual;
select round(3.4), trunc(3.4), ceil(3.4), floor(3.4) from dual;
select round(3.6), trunc(3.6), ceil(3.6), floor(3.6) from dual;

-- round trunc는 날짜 타입에도 사용가능 
select round(to_date('20/04/26')) from dual;
select round(systimestamp) from dual; -- 현재시간
select round(to_date('20/04/26'),'Month') from dual;
-- 일단위를 반올림해서 월에 반환하라. 
-- to_date  문자를 날짜로 변환


-- 3.5. 날짜 함수

select sysdate from dual; -- 현재의 날짜를 반환하는 함수
select systimestamp from dual; -- 현재의 날짜와 시간을 반환하는 함수

-- 5.1 날짜의 연산

select first_name, (sysdate - hire_date)/7 as "weeks"
from employees
where department_id = 60;

-- 5.2 날짜 함수

select first_name, sysdate, hire_date,
        months_between(sysdate, hire_date) as workmonth
        -- months_between(date1, date2) 날짜 사이의 월 수를 반환
from employees
where first_name  = 'Diana';

select first_name, hire_date, ADD_months(hire_date,100)
 -- ADD_MONTHS( date, n) 월 수 n을 date에 더함. 
from employees 
where first_name  = 'Diana';

select sysdate, next_day(sysdate, '월')
from dual;
-- next_day 함수는  date 다음의 명시된 요일의 날짜를 찾음. 요일을 ' ' 로 함.

select sysdate, last_day(sysdate)
from dual;
-- last_day(date) 월의 마지막 날짜를 찾음

select sysdate, round(sysdate), trunc(sysdate)
from dual;
-- round(date[, 'fmt']) 반올림한 date 를 반환, fmt없으면 가까운날짜로 반올림
-- trunc(date[, 'fmt']) fmt에 명시된 단위에 대해 절삭한 date를 반환, 없으면 가까운 날자로 절삭

select trunc(Sysdate, 'Month') 
from dual;
-- year , month 등 반올림하거나 절삭할 단위를 지정할 수 있다.

-- 3.6. 변환 함수

-- 6.3. TO_CHAR(date,'fmt') 날짜를 문자로 변환
 select first_name , to_char(hire_date,'MM/YY') AS hiredmonth
 from employees
 where first_name= 'Steven';
 -- TO_CHAR(date,'fmt')  날짜를 문자로 변환 
 
select first_name,
TO_CHAR(hire_date, 'YYYY"년" MM"월" DD"일"') HIREDATE
FROM employees;
-- fm'YYYY"년" MM"월" DD"일" 으로 지정했을때는 날짜 또는 월에 0이 제거됨
-- fx는 0이 살아있는 것으로, 디폴트 값임.

select first_name,
TO_CHAR(hire_date, 'fmDdspth "of" Month YYYY fmHH:MI:SS AM',
        'NLS_DATE_LANGUAGE=english') as HIREDATE
    FROM employees;
-- fm 은 0을 제거해줌.  Dd spth : DD 는 월의 일 , SPTH : 명시한 서수
-- "of" 문자를 넣어줌. Month : 9자리를 위해 공백을 추가한 월 이름
-- YYYY : 년, HH : 하루 중 시간 또는 시간 , MI : 분, SS: 초 , AM :정오 지시자 

-- 6.4. TO_CHAR(number, 'fmt') 숫자를 문자로 변환

SELECT first_name, last_name , TO_CHAR(salary, '$999,999') salary
from employees
where first_name = 'David';
-- TO_CHAR(number, 'fmt')

select  to_char(2000000, '$999,999') salary
from dual; 
-- 앞 숫자자리가 $999,999 이것보다 짧으면 #### 로 결과가 나온다.

select first_name, last_name, salary*0.123456 salary1,
        TO_CHAR(salary*0.123456, '$999,999.99') slary2
from employees
where first_name = 'David';

-- 6.5. TO_NUMBER 함수

SELECT to_number('$5,500.00','$99,999.99')- 4000 from dual;
-- to_number(char, 'fmt')

-- 6.6 TO_DATE 함수 : 문자 스트링을 날짜 형식으로 변환 

SELECT first_name, hire_date
from employees
where hire_date = to_date('2003/06/17','YYYY/MM/DD');

SELECT FIRST_NAME, HIRE_DATE
FROM    employees
where hire_date = TO_DATE('2003년06월17일','YYYY"년"MM"월"DD"일"');


-- 8. 연습문제
-- 8.1 
SELECT * from employees 
where email like('%LEE%');

-- 8.2.
SELECT first_name, salary , job_id
from employees
where manager_id = 103;

-- 8.3 
select * from employees
where (department_id = 80 and job_id = 'SA_MAN') 
        OR (DEPARTMENT_ID = 20 AND manager_id = 100);
        
-- 8.4 
SELECT regexp_replace(phone_number,'^[0-9]{3}.[0-9]{3}.[0-9]{4}$',
        '###-###-####') as "전화번호"
from employees;

-- 8.5. 
select RPAD(first_name || ' ' || last_name, 20, '*') as  full_name ,
        TO_CHAR(salary,'$009,999.99') AS SALARY, 
        to_char(hire_date,'YYYY-MM-DD') AS HIRE_DATE,
        round(sysdate - hire_date) as work_day
from employees
where job_id = 'IT_PROG' AND SALARY >= 5000 
Order by full_name; 

-- 8.6 
SELECT rpad(first_name || ' ' || last_name,20,'*') as full_name,
    TO_CHAR(salary,'$009,999.99') AS SALARY ,
    TO_CHAR(hire_date,'YYYY"년" MM"월" DD"일"') AS HIRE_DATE,
    ROUND(MONTHS_BETWEEN(sysdate,hire_date)) AS MONTH
FROM employees
where department_id = 30 
ORDER BY SALARY DESC;

-- 8.7
SELECT rpad(first_name || ' '|| last_name,17,'*') as "이름",
        to_char(salary + salary * commission_pct,'$99,999.99') as "급여"
from employees
where department_id = 80 and salary >10000
order by 급여 desc;