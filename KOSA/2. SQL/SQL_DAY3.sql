-- nvl(열, 널일경우반환값)
select first_name, salary+salary*nvl(commission_pct, 0)
from employees;

-- nv2(열, 널이 아닌경우, 널일경우)
select first_name, salary+salary*nvl2(commission_pct,commission_pct,0) as salary
from employees;

select first_name, nvl2(commission_pct,salary+salary*commission_pct,salary) as salary
from employees;
-- nvl2 를 사용하는 이유는 불필요한 연산을 피하기 위해서임. 따라서 위위보다 위의 것을 더 선호

select first_name, coalesce(salary+(salary*commission_pct),salary) as salary
from employees;

select first_name, coalesce(salary+(salary*commission_pct),salary) as salary
from employees
where salary*commission_pct< 650; 

select first_name, coalesce(salary*commission_pct,0) as salary
from employees
where lnnvl(salary*commission_pct >= 650 ); 

select first_name, coalesce(salary*commission_pct,0) as salary
from employees
where salary * commission_pct < 650
union  -- 합집합하기
select first_name, coalesce(salary*commission_pct,0) as salary
from employees
where salary * commission_pct is null;

-- DECODE (표현식, 비교값1, 결과1, 비교값2, 결과2,,,)
select job_id, salary,
        decode(job_id, 'IT_PROG', salary*1.10,
                        'FI_MGR', salary*1.15,
                        'FI_ACCOUNT',salary*1.20,
                        salary)
        as revised_salary
from employees;
                    

-- CASE 표현식 WHEN 비교값1 THEN 결과1
-- CASE WHEN 조건 THEN 조건이 참일경우 결과
select job_id, salary,
        case job_id WHEN 'IT_PROG' THEN salary*1.10
                       WHEN 'FI_MGR' THEN salary*1.15
                        WHEN'FI_ACCOUNT' THEN salary*1.20
                else salary
        end as revised_salary
from employees;

select job_id, salary,
        case WHEN job_id='IT_PROG' THEN salary*1.10
            WHEN job_id='FI_MGR' THEN salary*1.15
            WHEN job_id='FI_ACCOUNT' THEN salary*1.20
                        else salary
        end as revised_salary
from employees;

select first_name, salary,
    case when salary < 5000 then salary*1.20
        when salary < 10000 then salary*1.5
        when salary <15000 then salary*0.5
    end as revised_salary
from employees;


select employee_id , first_name
from employees
where hire_date like '04%'
union
select employee_id , first_name
from employees
where department_id = 20;

select employee_id , first_name, to_char(hire_date)
from employees
where hire_date like '04%'
union
select employee_id , first_name, to_char(department_id)
from employees
where department_id = 20;


-- 4장. 그룹함수
-- 4.1.  

select avg(salary), max(salary),min(salary), sum(salary)
from employees
where job_id like 'SA%';
--  null 값을 무시한, 평균, 최대, 최소, 합계를 출력

SELECT min(hire_date), max(hire_date)
from employees;
-- 이렇게 뽑는 것은 먼저 입사한 사원의 입사일과 나중에 입사한 사원의 수 출력

select min(first_name) ,max(first_name) from employees;

select max(salary) from employees;
-- 가장 많은 봉급을 보여줌. 가장 많은 봉급을 받는 사람의 이름을 알고싶지만 오류남

select first_name, max(salary) from employees;
-- 이걸 알고싶으면 서브쿼리로 해결해야함. 7장에 나옴..

select * from employees;

-- 80번 부서와 50번 부서의 급여 평균과 표준편차를 출력하세요.
select round(avg(salary)), round(stddev(salary),2)
from employees
where department_id= 80 or department_id =50;

select round(avg(salary)), round(stddev(salary),2)
from employees
where department_id= 80
union
select round(avg(salary)), round(stddev(salary),2)
from employees
where department_id =50;
-- 위에처럼 합한게 아니라, 그룹끼리 각각 나오게 하고 싶으면 , union쓰지만,
-- 이건 너무 번거롭기 때문에 , group-by를 사용한다.

-- 2.1 group by 사용
select department_id , AVG(salary)
from employees
group by department_id ;

-- 2.2. 하나 이상의 열로 그룹화
select department_id, job_id, sum(salary)
from employees
group by department_id, job_id;
--  두개도 넣을 수 있지만, 순서가 중요하다. 먼저 그룹되고 나중에 그룹된다. 


-- 2.3.  그룹함수를 잘못 사용한 질의
-- select 절의 그룹함수가 아닌 모든 열이나 표현식은 group by절에 있어야함.
-- where 절을 사용하여 그룹을 제한 할수 없습니다 

select department_id, count(first_name)
from employees;
-- 이렇게 하면 오류 발생

select department_id, count(first_name)
from employees
group by department_id;
-- 이렇게 그룹을 지정해줘야함.

select department_id , AVG(salary)
from employees
where avg(salary) > 2000
group by department_id;
--  이렇게 where 절을 사용하여 그룹제한이 안됨. 그래서 having 절을 사용.

-- having
-- where 절을 사용하여 검색하는 행을 제한 하는 것과 똑같은 방법으로 having절 사용
-- [ HAVING goup_by_condition ]

-- 3.1. having 사용
select department_id, ROUND(avg(salary),2)
from employees
group by department_id
having AVG(salary) > 8000;

-- 급여 평균이 8000을 초과하는 각 직무에 대하여 직무와 직무별 급여 평균을 출력
-- sales 직무를 담당하는 사원은 제외하고 급여 평균으로 결과를 정렬 
select job_id, avg(salary) payroll
from employees
where job_id not like 'SA%'
group by JOB_ID
having AVG(salary) > 8000
order by AVG(salary);

-- 4. GROUP SET

-- 부서별 급여의 평균고 직무별 급여의 평균
SELECT department_id , round(avg(salary),2)
from employees
group by department_id;
union -- department 랑  jobid 가 타입이 달라서, 오류남
SELECT job_id, round(avg(salary),2)
from employees
group by job_id;

SELECT TO_CHAR(department_id) , round(avg(salary),2) -- 부서를 문자로 만들어서 실행시킴
from employees
group by department_id
union 
SELECT job_id, round(avg(salary),2)
from employees
group by job_id
ORDER BY 1;

SELECT DEPARTMENT_ID , JOB_ID, ROUND(AVG(SALARY),2)
FROM EMPLOYEES
GROUP BY DEPARTMENT_ID, JOB_ID 
order by department_id, job_id;
-- 위아래 두개를 비교하기. 
SELECT DEPARTMENT_ID , JOB_ID, ROUND(AVG(SALARY),2)
FROM EMPLOYEES
GROUP BY grouping sets (DEPARTMENT_ID, JOB_ID) -- 반드시 소괄호 묶어주기 
order by department_id, job_id;

-- 5장
-- 5.1. ROLLUP, CUBE 사용
SELECT DEPARTMENT_ID, JOB_ID, ROUND(AVG(SALARY),2),COUNT(*)
FROM EMPLOYEES
GROUP BY DEPARTMENT_ID, JOB_ID
ORDER BY DEPARTMENT_ID, JOB_ID;
-- 여기에는 소계가 만들어있지 않음


SELECT DEPARTMENT_ID, JOB_ID, ROUND(AVG(SALARY),2),COUNT(*)
FROM EMPLOYEES
GROUP BY ROLLUP(DEPARTMENT_ID, JOB_ID)
ORDER BY DEPARTMENT_ID, JOB_ID;


SELECT DEPARTMENT_ID, JOB_ID, ROUND(AVG(SALARY),2),COUNT(*)
FROM EMPLOYEES
GROUP BY CUBE( DEPARTMENT_ID, JOB_ID)
ORDER BY DEPARTMENT_ID, JOB_ID;

-- 6장
SELECT 
    NVL2(department_id, DEPARTMENT_ID||'',
        DECODE(GROUPING(DEPARTMENT_ID),1,'소계')) AS 부서,
    NVL(JOB_ID, DECODE(GROUPING(JOB_ID),1,'소계')) AS 직무,
    ROUND(AVG(SALARY),2) AS 평균, 
    COUNT(*) AS 사원의수
FROM employees
GROUP BY CUBE(department_ID, JOB_ID)
ORDER BY DEPARTMENT_ID, JOB_ID;
-- ||'' : '' 로 이으면 문자가 됨.

    
-- 7 장 
SELECT 
    NVL2(department_id, department_id||'',
        DECODE(GROUPING_ID(department_id,job_id),2,'소계',3,'합계')) AS 부서,
    NVL(JOB_ID, DECODE(GROUPING_ID(department_id,job_id),1,'소계',3,'합계')) AS 직무,
    GROUPING_ID(department_id,job_id) AS GID,
    ROUND(AVG(SALARY),2) AS 평균, 
    COUNT(*) AS 사원의수
FROM employees
GROUP BY CUBE(department_ID, JOB_ID)
ORDER BY DEPARTMENT_ID, JOB_ID;

-- 8장 연습문제
-- 8.1.
SELECT job_id,avg(salary)
from employees
group by job_id;

--8.2. 
SELECT job_id,avg(salary)
from employees
group by job_id;

-- 8.3 
select department_id, job_id, count(*)
from employees
group by department_id, job_id;

-- 8.4. 
select department_id, round(stddev(salary),2) as stddev
from employees
group by department_id;

-- 8.5. 
select department_id, count(*)
from employees
group by department_id
having count(*) >= 4 ;

-- 8.6. 
select job_id, count(*)
from employees
group by job_id, department_id
having department_id =50;

select job_id , count(*)
from employees 
where department_id =50
group by department_id, job_id;
-- 의 차이?

-- 8.7. 
select job_id , count(*)
from employees 
where department_id =50
group by department_id, job_id
having count(*) < 10;

-- 8 .8 
select to_char(hire_date,'YYYY') AS "입사년도",
        ROUND(avg(salary)) as 급여평균,
        count(*) as 사원수
from employees
group by to_char(hire_date,'YYYY')
order by 입사년도;


-- 8.9.
select to_char(hire_date,'YYYY') as 입사년도,
        to_char(hire_date,'MM') AS 입사월,
        round(avg(salary)) as 급여평균 , count(*) as 사원수
from employees
group by rollup(to_char(hire_date,'YYYY'), to_char(hire_date,'MM'))
order by 입사년도,입사월;


-- 8.10 
select to_char(hire_date,'YYYY') as 입사년도,
        to_char(hire_date,'MM') AS 입사월,
        round(avg(salary)) as 급여평균 , count(*) as 사원수
from employees
group by cube(to_char(hire_date,'YYYY'), to_char(hire_date,'MM'))
order by 입사년도,입사월;

--8.11
select 
    NVL(to_char(hire_date,'YYYY'),DECODE(GROUPING_ID(to_char(hire_date,'YYYY')),1,'합계')) as 입사년도,
    NVL(to_char(hire_date,'MM'),DECODE(GROUPING_ID(to_char(hire_date,'MM')),1,'소계')) AS 입사월,
    GROUPING_ID(to_char(hire_date,'YYYY'),to_char(hire_date,'MM')) AS GRID,
    round(avg(salary)) as 급여평균 , count(*) as 사원수
from employees
group by cube(to_char(hire_date,'YYYY'), to_char(hire_date,'MM'))
order by 입사년도,입사월;

-- 5장 분석함수
-- 함수가 뭐냐에 따라서, over() 뒤에 오는 것이 달라짐. 뭘 넣을지 생각해야한다. 
SELECT department_id,
    round(avg(salary) over (partition by department_id),2)
from employees;

select department_id, round(avg(salary),2)
from employees
group by department_id;

-- 이 두가지의 코드를 보고 그룹함수와 분석함수의 차이를 생각해보자.
-- 그룹함수는 묶여진 것의 값만 나오고, 분석함수는 다나온다.


-- 1.1. 순위를 나타내는 함수 
select employee_id, department_id, salary,
    RANK()  OVER(ORDER BY salary DESC) sal_rank, -- 해당값의 순위결정 ( 중복순위 계산 )
    DENSE_RANK() OVER(ORDER BY salary DESC) sal_dense_rank, -- 중복순위를 계산하지 x
    ROW_NUMBER()OVER(ORDER BY salary DESC) sal_number --조건을 만족하는 모든행의 번호 제공. 일련번호생성
from employees;

-- 1.2 가상순위와 분포

select employee_id, department_id, salary,
    CUME_DIST() OVER (ORDER BY salary DESC) sal_cume_dist,
    -- 최대값 1을 기준으로 분산된 값을 제공. 최솟값과 최댓값 사이의 상대적인 위치 의미
    -- 처음 값은 1이다. 
    PERCENT_RANK() OVER (ORDER BY salary DESC) sal_pct_rank
    -- 최대값을 1을 기준으로 데이터 집합에서 특정값의 백분율 순위를 제공. 첫번째 위치가 0부터 시작 
from employees;

-- 1.3.  비율함수

select first_name, salary,
    round(RATIO_TO_REPORT(salary) OVER (),4) as salary_ratio
from employees
where job_id = 'IT_PROG';
-- 해당 열 값의 백분율을 소수점으로 제공함. 그룹내에서 해당하는 백분율을 구할 수 있음. 

--1.4 분배함수

select first_name, department_id, salary,
    NTILE(10) OVER ( ORDER BY salary DESC) as sal_quart_tile
from employees
where department_id = 50;
--  전체 데이터의 분포를 n개의 구간으로 나누어 표시해줌. 
-- 만일 row 가 균등하게 나뉘지 않으면, 위에서부터 추가됨.  

-- 1.5. LAG, LEAD 
SELECT EMPLOYEE_ID, 
    LAG(salary,1,0) over ( ORDER BY salary ) as lower_sal, 
    salary,
    LEAD(salary,1,0) over ( ORDER BY salary ) as higher_sal
from employees
order by salary;
-- LAG( column, n, 초기값) : 이전 n 번째 행의 값을 가져옴. 
-- LEAD( column, n, 초기값) : 이후 n 번째 행의 값을 가져옴. 

-- 1.6. LISTAGG
select department_id,
    Listagg(first_name,',') WITHIN GROUP(ORDER BY hire_date) as names
    -- group 안에도 어떻게 정렬해야할지도 알수 있음.
    -- 여러개 행으로 출력해야 할것을 이름으로 해서 한번에 출력할 수 있음. 
from employees
group by department_id;
-- LISTAGG(하나의 행으로 출력하고 싶은 열이름, 갑을 구분하는 구분자)

select department_id, FIRST_NAME -- 에러나옴. 그래서 위에처럼 해줌. 
from employees
group by department_id;


-- 5.2. 윈도우절 
-- 5.2.1.  FIRST_VALUE ,LAST_VALUE : 정렬된 것중 처음값 / 마지막 값 리턴 
SELECT employee_id, 
    FIRST_VALUE(salary)
     OVER (ORDER BY salary
        ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS lower_sal,
    salary AS my_sal,
    LAST_VALUE(salary)
     OVER (ORDER BY salary
        ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS higher_sal
FROM employees;

-- 5.3. 선형회귀 함수
-- 5.3.1. regr_avgx /regr_avgy : x,y 가 null은 제외하고 평균을 구해줌
select
    avg(salary),
    regr_avgx(commission_pct, salary)
from employees;
-- 위아래는 값은 의미를 지님
SELECT avg(salary)
from employees
where commission_pct IS NOT NULL;
    
-- 5.3.2. REGR_COUNT : 두 인수가 not null인것을 셈 
SELECT 
    DISTINCT
        department_id,
        REGR_COUNT(manager_id, department_id)
            OVER(partition by department_id) "REGR_COUNT" -- 부서별로 파티션해서 카운터 세기
FROM  employees
ORDER BY department_id;

-- 위의 구문과 비교하기
select department_id , count(*)
from employees
group by department_id
order by department_id;  -- 이건 null이 포함된 값이 나온다.

--5.3.3. REGR_SLOPE 기울기 , REGR_INTERCEPT Y절편을 반환 
select
    job_id,
    employee_id,
    salary,
    ROUND(SYSDATE-hire_date) "working_day",
    ROUND(REGR_SLOPE(salary, SYSDATE-hire_date)
        OVER (PARTITION BY job_id),2) "regr_slope",
    Round(REGR_INTERCEPT(salary, SYSDATE-hire_date)
        OVER (PARTITION BY job_id),2) "REGR_INTERCEPT"
FROM employees
where department_id = 80
order by job_id, employee_id;

-- 5.3.4. REGR_R2(y,x) 결정계수 - 1에 가까울수록 좋음. 

select
    DISTINCT
    job_id,
    ROUND(REGR_SLOPE(salary, SYSDATE-hire_date)
        OVER (PARTITION BY job_id),2) "regr_slope",
    Round(REGR_INTERCEPT(salary, SYSDATE-hire_date)
        OVER (PARTITION BY job_id),2) "REGR_INTERCEPT",
    Round(REGR_R2(salary, SYSDATE-hire_date)
        OVER (PARTITION BY job_id),2) "REGR_R2"        
FROM employees
where department_id = 80;

-- 4장 피벗테이블

-- 먼저, 테이블 생성하기. 
CREATE TABLE sales_data(
    employee_id NUMBER(6),
    week_id NUMBER(2),
    week_day VARCHAR2(10),
    SALES   NUMBER(8,2)
);

INSERT INTO sales_data values(1101,4,'SALES_MON',100);
INSERT INTO sales_data values(1102,5,'SALES_MON',300);
INSERT INTO sales_data values(1101,4,'SALES_TUE',150);
INSERT INTO sales_data values(1102,5,'SALES_TUE',300);
INSERT INTO sales_data values(1101,4,'SALES_WED',80);
INSERT INTO sales_data values(1102,5,'SALES_WED',230);

INSERT INTO sales_data values(1101,4,'SALES_THU',60);
INSERT INTO sales_data values(1102,5,'SALES_THU',120);

INSERT INTO sales_data values(1101,4,'SALES_FRI',120);
INSERT INTO sales_data values(1102,5,'SALES_FRI',150);
COMMIT;

SELECT*FROM SALES_DATA;

-- 스프레드시트 형식 데이터테이블 만들기
CREATE TABLE sales(
    employee_id NUMBER(6),
    week_id NUMBER(2),
    sales_mon NUMBER(8,2),
    sales_tue NUMBER(8,2),
    sales_wed NUMBER(8,2),
    sales_thu NUMBER(8,2),
    sales_fri NUMBER(8,2)
);

INSERT INTO sales VALUES(1101,4,100,150,80,60,120);
INSERT INTO sales VALUES(1102,5,300,300,230,120,150);
COMMIT;
SELECT * FROM sales;

-- 5.4.2. PIVOT
SELECT*FROM SALES_DATA;

SELECT *
FROM sales_data
PIVOT
(
    sum(sales)
    FOR week_day
    IN('SALES_MON','SALES_TUE','SALES_WED','SALES_THU','SALES_FRI')
)
ORDER BY employee_id, week_id;

-- 5.4.3. UNPIVOT
SELECT employee_id, week_id, week_day, sales
FROM sales
UNPIVOT
(
    sales
    FOR week_day
    IN(sales_mon, sales_tue,sales_wed, sales_thu,sales_fri)
);

-- 5.5 연습문제
-- 5.5.1. 

SELECT department_id, first_name, salary,
    RANK() OVER(PARTITION BY department_id ORDER BY salary DESC) "sal_rank",
    lag(salary,1,0)over (PARTITION BY department_id order by salary DESC) as prev_salary,
    FIRST_VALUE(salary)
        OVER (PARTITION BY department_id ORDER BY salary DESC ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) as prev_salary2
from employees
ORDER BY department_id;

--5.5.2
select first_name FROM employees
WHERE employee_id = (
    SELECT before_id
    FROM 
    (
    SELECT employee_id, LAG(employee_id,1,0)OVER (ORDER BY employee_id) AS before_id
    FROM employees)
    where employee_id=170);
    
-- 5.5.4
SELECT employee_id, department_id,
    FIRST_VALUE(salary) over (partition by department_id order by salary 
             rows between unbounded preceding and unbounded following) AS lower_salry,
    salary as my_salary,
    LAST_VALUE(salary) over (partition by department_id order by salary 
             rows between unbounded preceding and unbounded following) AS HIGHER_SALARY,
    LAST_VALUE(salary) over (partition by department_id order by salary
             rows between unbounded preceding and unbounded following) - SALARY AS DIFF_SALARY
FROM employees;
