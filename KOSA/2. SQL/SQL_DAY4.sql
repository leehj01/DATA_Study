-- 6.1. 조인이란

--6.2. 오라클 조인

-- 6.2.1. CARTESIAN PRODUCT : 조인 조건이 생략, 잘못, 조인조건을 안집어넣을 때 나옴.
-- 모든 행들을 곱하게 되므로, 많은 행을 생성하는 경향이 있음. 결과도 유용하지 않음. 

select first_name, department_name
from employees, departments;

SELECT first_name, employees.department_id, department_name
from employees, departments;
-- 열이름이 중복되면, 테이블 이름 명시

select e.first_name, e.department_id, d.department_name
from employees e , departments d;
-- 테이블 이름이 길면 조인 구문의 from절에 테이블 별칭 이용 할 수 있음. 
-- 테이블 별칭을 쓸 땐, as 쓰면 안됨. 

--6.2.2. EQUL JOIN : 2개이상 공통되는 열에 의해 논리적으로 결합하는 조인 기법 

-- 부서들의  id가 같을 경우의 이름과 id, 부서 이름을 적어주기
select e.first_name , e.department_id, d.department_name
from employees e , departments d
where e.department_id = d.department_id; -- 조인 조건 

select e.first_name , e.department_id, d.department_name
from employees e , departments d
where e.department_id = d.department_id -- 조인 조건 
and e.employee_id = 103;

-- 모든 사원의 이름과 직무이름 출력하세요
select e.first_name, j.job_title
from employees e, jobs j 
where e.job_id = j.job_id;


-- 자신의 매니저보다 더 많은 급여를 받는 사원의 이름과 급여, 매니저의 이름과 급여 
select e.first_name ,e.salary, m.first_name , m.salary
from employees e, employees m
where e.manager_id = m.employee_id and e.salary > m.salary;


-- 6.2.3. SELF JOIN  : 자체적으로 테이블을 조인함. 
SELECT e.first_name as employee_name,
        m.first_name as manager_name
from employees e, employees m  -- 같은 테이블을 서로 다르게 구별하기 위해서 설정.
where e.manager_id = m.employee_id 
and e.employee_id = 103; -- and를 안해주면, 106행이 나오고(사장때문), 더 구체적인 조건을 넣어줘도 가능
-- 사원의 매니저 아이디와 매니저의 사원번호가 값을 때 , 그리고 그건 사원103을 찾기. 

SELECT e.first_name as employee_name,
        m.first_name as manager_name
from employees e, employees m  -- 같은 테이블을 서로 다르게 구별하기 위해서 설정.
where e.manager_id = m.employee_id 
and e.first_name = 'Steven' and e.last_name ='King';
--  사장은 매니저 id 가 없기 때문에 null이다. 그래서 값이 나오지 않는다.
-- 그래서 사용하는 것이.  outer join 이다. 


--6.2.4. NON-EQUL JOIN
SELECT  e.first_name,j.min_salary , e.salary ,j.max_salary , j.job_title
from employees e, jobs j 
where e.salary
BETWEEN j.min_salary and j.max_salary
order by first_name;

desc jobs; --  테이블의 구조 확인하기. 

-- 6.2.5.  OUTER JOIN : (+) 를 사용하여 만듦. 

SELECT e.first_name as employee_name,
        m.first_name as manager_name
from employees e, employees m  
where e.manager_id = m.employee_id (+) -- + 를 붙이니깐, 나옴. leftouter join 
-- null이 아닌 쪽에 + 를 넣어준다. 
and e.first_name = 'Steven' and e.last_name ='King';
-- full outer join 을 지원하지않아서, 양쪽다 null값인 경우는 지원하지 않는다. 

SELECT e.employee_id, e.first_name, e.hire_date,
       j.start_date , j.end_date , j.job_id , j.department_id
from employees e, job_history j
where e.employee_id = j.employee_id 
order by j.employee_id;

SELECT e.employee_id, e.first_name, e.hire_date,
       j.start_date , j.end_date , j.job_id , j.department_id
from employees e, job_history j
where e.employee_id = j.employee_id(+)   -- 이렇게 + 를 하면 다 나온다.  
order by j.employee_id;


-- 3. 안시조인 

--3.3.1. CROSS JOIN : 오라클의 CARESIAN PRODUCT와 같은 결과 출력. 그냥 다나오는 것
-- 효율성이 없음. 
select employee_id, department_name
from employees
cross join departments;

-- 3.3.2. NATURAL JOIN
-- 모든 같은 이름을 갖는 열들에 대해 조인함.  
-- natural조인은 자동으로 두 테이블에서 같은 이름을 가진 열에 equi조인 수행
-- 이때, 조인 열들은 같은 데이터 유형이어야함. 

select first_name, job_title
from employees natural join jobs;

select first_name, department_name
from employees
natural JOIN departments; -- table2 이름을 넣음
-- 값이 32개 나오는데 그 이유는, MANGER, department 둘다 같은 것을 골랐기에 그런것 

select first_name, employee_id , department_id, department_name,manager_id
from employees
natural JOIN departments; -- table2 이름을 넣음


-- 3.3.3. USING JOIN
-- NATURAL 조인은 모든열에 대해 조인이 이루어짐 , 
-- USING절 사용하면 원하는 열에 대해서만 선택적 사용 가능  
select first_name, department_name 
from employees
join departments
using (department_id);  -- 값이 106개 나옴 

-- 3.3.4. ON JOIN
select department_name, street_address, city, state_province
from departments d
join locations l
ON d.location_id = l.location_id;  -- 위치 id 가 같은 것들을 불러오라

-- 3.3.4. 1) 여러테이블의 조인

-- 모든 사원의 이름, 부서이름, 부서의 주소를 출력 
select e.first_name, d.department_name, 
    l.street_address || ',' || l.city ||',' || l.state_province as address
from employees e
join departments d on e.department_id = d.department_id -- 사원이름과 부서이름
join locations l on d.location_id = l.location_id; -- 부서의 주소 

-- 3.3.4. 2) where 절과의 혼용

select e.first_name  as name, d.department_name as department
from employees e
join departments d
on e.department_id = d.department_id
where employee_id = 103; -- join과 상관없는 조건절. 

select e.first_name  as name, d.department_name as department,
        l.street_address ||','|| l.city||'.'||l.state_province as address
from employees e
join departments d
on e.department_id = d.department_id
join locations l
on d.location_id = l.location_id
where employee_id = 103;

-- 3.3.4. 3) on절에 where 절 의 조건 추가
select e.first_name  as name, d.department_name as department
from employees e
join departments d
on e.department_id = d.department_id and employee_id = 103;

select e.first_name  as name, d.department_name as department,
        l.street_address ||','|| l.city||'.'||l.state_province as address
from employees e
join departments d
on e.department_id = d.department_id and employee_id = 103
join locations l
on d.location_id = l.location_id;

select e.first_name  as name, d.department_name as department,
        l.street_address ||','|| l.city||'.'||l.state_province as address
from employees e
join departments d
on e.department_id = d.department_id 
join locations l
on d.location_id = l.location_id and employee_id = 103;

-- 3.5. outer join
-- LEFT/ RIGHT/ FULL을 적어줌. OUTER 은 생략 가능. 
-- 기준이 되는 쪽을 조인한다. 즉, 사원이 기준임. 
SELECT e.employee_id, e.first_name, e.hire_date,
       j.start_date , j.end_date , j.job_id , j.department_id
from employees e
LEFT OUTER JOIN job_history j -- 기준이 되는쪽에 방향을 붙임. 테이블에 넣음.
ON e.employee_id = j.employee_id 
order by j.employee_id;


--4. 연습문제

--4.1. 이름, 부서아이디, 도시를 적어주기
select e.first_name, e.department_id,  l.city
from employees e , departments d , locations l
where e.department_id = d.department_id and  d.location_id = l.location_id;

select e.first_name, e.department_id, l.city
from employees e 
join departments d 
on e.department_id = d.department_id
join locations l
on d.location_id = l.location_id ; 


-- 4.2. 
SELECT e.employee_id, e.first_name, e.salary, m.first_name as first_name_1, d.department_name
from employees e
join employees m
on e.manager_id = m.employee_id and e.employee_id =103
join departments d
on m.manager_id = d.manager_id ;


--4.3. 
SELECT e.employee_id, e.first_name, e.salary, 
    m.first_name as first_name_1, m.salary, d.department_name
from employees e, employees m, departments d
where  m.employee_id(+) = e.manager_id 
    and m.department_id = d.department_id (+)
    and e.department_id =90;


SELECT e.employee_id, e.first_name, e.salary, 
    m.first_name as first_name_1, m.salary, d.department_name
from employees e
left outer join employees m
on e.manager_id = m.employee_id
left outer join departments d
on m.department_id = d.department_id 
where e.department_id =90;


-- 4.4 
select e.employee_id , l.city
from employees e 
join departments d 
on e.department_id = d.department_id
join locations l
on d.location_id = l.location_id and e.employee_id = 103 ; 


--4.5. 
select l.city as "department location",
    j.job_title as "Manager's job"
from employees e 
join departments d 
on e.department_id = d.department_id
join locations l
on d.location_id = l.location_id and e.employee_id = 103 
join employees m
on e.manager_id = m.employee_id
join jobs j
on m.job_id = j.job_id;

-- 4.6.

select e.employee_id ,e.first_name, e.last_name, e.email, e.phone_number,e.hire_date,
        j.job_title, e.salary, e.commission_pct,
        m.first_name as "manager_first_name", 
        d.department_name
from employees e
join jobs j
on e.job_id = j.job_id
LEFT outer join employees m
on e.manager_id = e.employee_id
LEFT outer join departments d
on e.department_id = d.department_id;
        

-- 7장  서브쿼리

-- 7.1. 서브쿼리

select salary from employees where first_name = 'Nancy';  -- 12008

select first_name, salary from employees where salary > 12008;


Select first_name, salary
from employees
where salary > (select salary
                from employees
                where first_name = 'Nancy');
-- 서브쿼리를 실행시킨 후 , 그 결과로 메인 쿼리를 사용하기.
                
-- 7.2. 단일행 서브쿼리
select first_name, job_id, hire_date
from employees 
where job_id = (select job_id
                from employees
                where employee_id = 30);
                
-- 7.3.  다중행 서브쿼리
select first_name, salary
from employees
where salary > ( SELECT salary
                FROM employees
                WHERE first_name = 'David');
                
select salary
from employees
WHERE first_name = 'David';

select first_name, salary
from employees
where salary > ANY ( SELECT salary
                FROM employees
                WHERE first_name = 'David');

select first_name, salary
from employees
where EXISTS( SELECT salary
                FROM employees
                WHERE first_name = 'David');                
                
select first_name, department_id , job_id 
from employees
where department_id IN ( SELECT department_id       FROM employees
                WHERE first_name = 'David');
    


--4. 상호 연관 서브쿼리
select first_name, salary
from employees a
where salary > (select avg(salary)
                from employees b
                where b.department_id =a.department_id );

-- 5. 스칼라 서브쿼리

select first_name, (select department_name 
                    from departments d
                    where d.department_id = e.department_id) department_name
from employees e
order by first_name;


select first_name, department_name
from employees e
join departments d on (d.department_id = d.department_id)
order by first_name;

-- 7.6. 인라인뷰
select row_number, first_name, salary
from (select first_name, salary, 
        row_number() over (order by salary desc) as row_number  
        -- 반드시 별칭을 넣어줘야 메인쿼리에서 쓸수 있다.     
        from employees)
where row_number BETWEEN 1 AND 10 ;
-- 서브쿼리에 써야 메인쿼리에 쓸수 있다


-- 7.7. 3중쿼리
select rownum, first_name, salary 
from employees
order by salary desc;
-- rownum 이 순서되로 되어있지 않기 때문에 아래같이 사용.

select rownum, first_name, salary 
from ( select first_name, salary from employees
        order by salary desc) -- 월급을 내림차순으로 뽑은 다음에 
where rownum between 1 and 10;

select first_name, salary
from (select first_name , salary from employees order by salary desc)
where rownum between 11 and 20; -- 이렇게 하면 안나옴
-- 왜냐하면 rownum 은 첫번째 부터 조회하지 않으면 답이안나옴.

select *
from (select first_name  salary, rownum as rnum
        from (select first_name , salary
            from employees 
            order by salary desc)
            )
where rnum between 11 and 20; -- 특정블럭을 하려면 3중쿼리 해야함

select rnum, first_name,salary
from(select first_name , salary, rownum as rnum
    from (select first_name , salary
        from employees
        order by salary desc)
        )
where rnum between 11 and 20;

select row_number, first_name, salary
from (select first_name, salary,
        row_number() over ( order by salary desc) as row_number
        from employees)
where row_number between 1 and 10 ;

-- 7.8. 계층형쿼리

select employee_id, 
    lpad(' ',3*(level-1)) || first_name ||''|| last_name,LEVEL as "level_"
    --  level만큼 공백을 채워주세요(lpad 이용)
FROM employees
start with manager_id is null 
connect by prior employee_id = manager_id ;
-- 매니저 id 가 null인 사장부터 시작.   
-- prior 를 어디에붙일지가 중요하다. 선행될 열에 prior를 붙여줌 
   
SELECT employee_id, lpad(' ',3*(level-1))||first_name|| ' '||last_name, level
from employees
start with manager_id is null
connect by prior employee_id = manager_id 
order siblings by first_name; -- 형제 내에서 정렬하겠다 

SELECT employee_id, lpad(' ',3*(level-1))||first_name|| ' '||last_name, level
from employees
start with manager_id is null
connect by prior employee_id = manager_id 
order by first_name;

select employee_id, lpad(' ',3*(level-1)) || first_name || ' ' || last_name, LEVEL
FROM employees
START WITH employee_id = 113
connect by prior manager_id = employee_id ;


-- 9.1. 연습문제
select employee_id, first_name, last_name, email, phone_number , hire_date, job_id,salary
from employees 
where manager_id in(select manager_id
                    from employees  
                    where department_id =20);

-- 9.2. 
select first_name
from employees
where salary = ( select max(salary)
                 from employees);
                 
-- 9.3.
select rnum, first_name,salary
from(select first_name , salary, rownum as rnum
    from (select first_name , salary
        from employees
        order by salary desc)
        )
where rnum between 3 and 5;


select first_name , salary, rownum as rnum
    from (select first_name , salary
        from employees
        order by salary desc);
        
        
-- 9.4.
select department_id, first_name, salary ,
        (select round(avg(salary))
            from employees m
            where e.department_id= m.department_id) as avg_sal
from employees e
where salary >= (select avg(salary) 
            from employees b
            group by department_id
            having e.department_id = b.department_id )
order by department_id;
