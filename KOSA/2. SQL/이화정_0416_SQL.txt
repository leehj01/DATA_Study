-- 4장 그룹함수 연습문제
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



-- 5장 분석함수 연습문제
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