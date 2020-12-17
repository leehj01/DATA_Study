select * from employees;

select * from departments;

select *
from employees;

select employee_id , first_name, last_name, salary
from employees;

select * from departments;

select *
from employees;

desc employees;

select first_name, salary, commission_pct
from employees;

select first_name, hire_date, salary
from employees;

select first_name, salary , salary+salary*0.1 
from employees;

select department_name, location_id
from departments;

select first_name, hire_date
from employees;

select first_name , department_id
from employees;

select employee_id, salary, commission_pct
from employees;

select first_name as  이름,  salary  급여
from employees;

 select first_name , last_name , salary
 from employees;
 
 select first_name || ' ' || last_name || '''s 급여는' || salary 
 from employees;
 
 select rowid, rownum, employee_id, first_name
 from employees;
 -- row 가 가지고 있는, 고유 id 와 num 
 
select first_name , job_id, department_id 
from employees
where job_id = 'IT_PROG';

select first_name, department_id
from employees
where department_id > 50;

select count(*) from employees
where department_id = 50;
-- count(*) 모든 행을 셈

SELECT first_name, salary, hire_date
from employees
where salary > 15000;

select first_name, salary, hire_date
FROM employees
where hire_date = '04/01/30';

select first_name, salary, hire_date
FROM employees
where first_name = 'Steven';

select first_name, salary
FROM employees
where salary between 1000 and 12000;

select first_name, salary, hire_date
FROM employees
where hire_date between '03/01/01' and '03/12/13';
-- 2003 년도의 입사자 출력, date 도 비트윈 연산자 가능 

select first_name, salary, hire_date
FROM employees
WHere first_name BETWEEN 'A' and 'Bz';
-- 문자도 가능 , 그러나 B라고 입력하면 안되고 Bz까지 입력해야함. 

select first_name , commission_pct
from employees
where commission_pct <0; 

select employee_id , first_name , salary , manager_id
from employees
where manager_id in (101,102,103);

select employee_id , first_name , job_id , department_id
from employees
where job_id in('IT_PROG', 'FI_MGR', 'AD_VP');

SELECT first_name , last_name, job_id, department_id
from employees
where job_id like 'IT%';

SELECT first_name, hire_date
from employees
where hire_date like '03%';


SELECT  first_name, job_id , salary
from employees
where job_id= 'IT_PROG' AND salary>= 5000;

select count(*) from employees
where commission_pct = null;
-- 실행 결과가 0 이다. 왜냐하면,  null은 연산이 안되기 때문에, ㅎㅎ..

select count(*) from employees
where commission_pct is null;
-- is null, is not null 을 해야 값을 구할 수 있다. 

select first_name , salary*12  
from employees
order by 2, first_name ;

select first_name , hire_date  
from employees
order by hire_date desc, first_name asc ;

--
-- 1. 모든 사원의 사원번호, 이름, 입사일, 급여를 출력하세요. 
select employee_id, first_name, last_name, hire_date, salary
from employees;

-- 2. 모든 사원의 이름과 성을 붙여 출력하세요. 열별칭은 name 으로 하세요.
select first_name || ' ' || last_name as "name"
from employees;

-- 3. 50번 부서 사원의 모든 정보를 출력하세요.
select * from employees
where department_id = 50;

-- 4. 50번 부서 사원의 이름, 부서번호, 직무아이디를 출력하세요 .
select first_name , last_name, department_id , job_id
from employees
where department_id = 50;

-- 5. 모든 사원의 이름, 급여 그리고 300달러 인상된 급여를 출력하세요.
select first_name , last_name, salary + 300
from employees;

-- 6. 급여가 10000보다 큰 사원의 이름과 급여를 출력하세요
select first_name, salary
from employees
where salary > 10000;

-- 7. 보너스를 받는 사원의 이름과 직무, 보너스율을 출력하시오.
select first_name, job_id, commission_pct
from employees
where commission_pct is not null;

-- 8. 2003년도 입사한 사원의 이름과 입사일 그리고 급여를 출력하세요.(비트윈연산자사용)
select first_name, hire_date, salary 
from employees
where hire_date between '03/01/01' and '03/12/30';

-- 9. 2003년도 입사한 사원의 이름과 입사일 그리고 급여를 출력하세요. (like 연산자 사용)
select first_name, hire_date, salary 
from employees
where hire_date like '03/%/%';

-- 10. 모든 사원의 이름과 급여를 급여가 많은 사원부터 적은 사원 순으로 출력하세요.
select first_name , salary
from employees
order by salary desc;

-- 11. 위 질의를 60번 부서의 사원에 대해서만 질의 하세요.
select first_name , salary
from employees
where department_id = 60
order by salary desc;

-- 12.  직무아이디가 IT_PROG 이거나, SA_MAN인 사원의 이름과 직무아이디를 출력하세요.
SELECT first_name , job_id
from employees 
where job_id = 'IT_PROG' or job_id = 'SA_MAN';

-- 13. Steven King 사원의 정보를 "Steven King  사원의 급여는 24000달러입니다"형식으로 출력하세요.
SELECT first_name ||' '|| LAST_NAME ||'사원의 급여는'||SALARy||'달려입니다' AS info
from employees
where first_name = 'Steven' and last_name = 'King';

-- 14. 매니저 직무에 해당하는 사원의 이름과 직무아이디를 출력하세요.
select first_name , job_id
from employees
where JOB_ID LIKE '%MAN';

-- 15. 매니저 직무에 해당하는 사원의 이름과 직무아이디를 직무 아이디 순서대로 출력하세요.
select first_name , job_id
from employees
where JOB_ID LIKE '%MAN'
ORDER BY job_ID ;

-- coderby 의 시습문제

select salary + salary * 0.1
from employees
where first_name = 'Neena';

select first_name, salary
from employees
where salary between 15000 and 20000;

select first_name, job_id
from employees
where job_id like 'SA%' and first_name = 'Gerald';

select first_name, job_id
from employees
where (job_id = 'IT_PROG' OR job_id ='FI_MGR') 
    AND SALARY >= 6000;
    
SELECT  COUNT(*) FROM employees where commission_pct =null;
SELECT  COUNT(*) FROM employees where commission_pct in(null);
SELECT  COUNT(*) FROM employees where commission_pct <>null;
SELECT COUNT(*) FROM employees where commission_pct is null;


select first_name, salary*12 ann_sal
from employees
where department_id = 60
order by salary*12;

select first_name, salary, hire_date
from employees
where hire_date LIKE '03%';


select first_name, salary, hire_date, job_id
from employees
where hire_date LIKE '%/10/%';

select first_name, salary, hire_date, department_id
from employees
where department_id in(40,60,70);

select first_name ||''|| last_name || '''s 급여는'||salary 
from employees;












