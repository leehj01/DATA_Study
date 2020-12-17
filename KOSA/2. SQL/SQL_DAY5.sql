-- 8.2.2.
INSERT INTO departments
Values (280,'Data Analyics', null,1700);

select * from departments;

rollback;

insert into
    departments (department_id, department_name , location_id)
values
    (280, 'Data Analyics',1700);
    
    
-- 8.2.3. 다른 테이블로부터 행 복사

create table managers as
    select employee_id, first_name, job_id, salary, hire_date
    from employees
    where 1=2; -- 이건 결과가 항상 false 기 때문에 값은 안나오고, 테이블만 있음

select  * from managers;

insert into managers
    (employee_id, first_name, job_id, salary, hire_date)
    select employee_id, first_name, job_id, salary, hire_date
    from employees
    where job_id like '%MAN';
    
rollback;

-- 3. 

create table emps as select * from employees; -- 모든 구문 복사
-- 그중에서, not null 제약 조건만 복사되기 때문에 아래 구문이 존재하는 것. 

alter table emps -- 테이블 구조를 그래서 바꿔줌. 
add ( CONSTRAINT emps_emp_id_pk PRIMARY KEY (employee_id), -- 기본키만들기..
        CONSTRAINT emps_manager_fk FOREIGN KEY(manager_id) -- 외래키 만들기
            REFERENCES emps(employee_id) -- employee_id 를 참조하겠다
    );
-- add constraint : 제약조건을 추가하겠다는 의미   

--8.3.1. 테이블 행 갠\갱신
select employee_id , first_name, salary
from emps
where employee_id = 103;

UPDATE emps 
set salary= salary *1.1, commission_pct= 0.01 -- , 를 이용해 복수도 가능
where employee_id = 103;

commit;

-- 8.3.2 서브쿼리로 다중 열 갱신
select employee_id, first_name, job_id, salary, manager_id
from emps
where employee_id IN (108,109);

-- 108 번 정보를 가지고 109 번의 사원의 정보에 덮어쓰기 
update emps  -- 조건에 대해서 여러 테이블 수정도 가능하긴 함. 
set( job_id, salary, manager_id)=  -- 열이름 생략 못가능 pk(기본키)는 수정 불가능 
    (select job_id , salary, manager_id  -- 단일 서브쿼리만 가능!!
    from emps
    where employee_id =108)
where employee_id = 109;

-- 8.4.1. 행 삭제

select distinct department_id from emps;

delete from emps
where employee_id = 104;

delete from emps
where employee_id = 103;
-- 참조 무결성의 위반으로 삭제가 되지 않음
-- 103번은 누군가의 매니저이므로, 삭제가 안됨. 

select * from emps;

ROLLBACK;

-- 8.4.2. 다른 테이블을 이용한 행 삭제  
create table depts as -- 우선 사본 테이블을 생성 
select * from departments;

desc depts; 
-- 테이블의 구조를 확인

delete from emps
where department_id =
                    (select department_id
                    from depts
                    where department_name = 'Shipping');
-- WHERE 절에 서브쿼리를 넣어서 하는 것을 의미함.                    
commit;


SELECT  * FROM  EMPS where department_id = 50;

--8.4.3. RETURNING : DML 조작시 특정값을 임시로 저장할 수 있음. 

--8.5. merge

CREATE TABLE emps_it as select * from employees where 1=2;

insert into emps_it
    (employee_id, first_name, last_name, email, hire_date, job_id)
VALUES
    (105,'David', 'Kim','DAVIDKIM','06/03/04','IT_PROG');

SELECT * FROM EMPS_IT;    

MERGE INTO emps_it a
    USING (SELECT * FROM employees WHERE job_id = 'IT_PROG') b
    ON( a.employee_id = b.employee_id)
WHEN MATCHED THEN
    UPDATE SET
    a.phone_number = b.phone_number,
    a.hire_date = b.hire_date,
    a.job_id = b. job_id,
    a.salary = b.salary,
    a.commission_pct = b.commission_pct,
    a.manager_id = b.manager_id,
    a.department_id = b.department_id
WHEN NOT MATCHED THEN
    INSERT VALUES
    (b.employee_id , b.first_name, b.last_name, b.email,
    b.phone_number, b.hire_date, b.job_id, b.salary,
    b.commission_pct, b.manager_id ,b.department_id);
    
select * from emps_it;


-- 6 . CATS : NOT NULL 제약 조건만 복사된다.


create table emp2 as select * from employees;

select count(*) from emp2;

create table emp3 as select * from employees where 1=2;
select count(*) from emp3;

-- 7. Multiple INSERT : 하나의 INSERT문에서 여러개의 테이블 동시에 하나의 행을 입력
-- 8.7.1 UNCONDITIONAL INSERT ALL 
-- 조건에 상관없이 기술된 여러개의 테이블에 데이터를 입력

create table emp_salary as 
    select employee_id, first_name, salary, commission_pct
    from employees
    where 1=2;
    
create table emp_hire_date as
select employee_id, first_name, hire_date, department_id
from employees
where 1=2;


insert all -- 열단위로 쪼개서 
    into emp_salary values
        (employee_id, first_name, salary, commission_pct)
    into emp_hire_date values
        (employee_id , first_name, hire_date, department_id)
    select * from employees;
-- 조건 설정 없이 그냥 다 집어 넣는 것 


select * from emp_salary;
select * from emp_hire_date;

-- 8.7.2. CONDITIONAL INSERT ALL
-- 특정 조건을 기술하여 그 조건에 맞는 행들을 원하는 테이블에 나누어 삽입

create table emp_10 as select * from employees where 1=2;

create table emp_20 as select * from employees where 1=2;

insert all
    when department_id = 10 then
    into emp_10 values
        (employee_id, first_name, last_name, email,phone_number,
        hire_date, job_id, salary, commission_pct, manager_id,
        department_id)
    when department_id = 20 then 
    into emp_20 values
        (employee_id, first_name, last_name, email,phone_number,
        hire_date, job_id, salary, commission_pct, manager_id,
        department_id)
    select * from employees;  --여기서 조회해서 
    
select * from emp_10;
select * from emp_20;

-- 8.7.3. CONDITIONAL INSERT FIRST
create table emp_sal5000 as 
    select employee_id, first_name, salary from employees where 1=2;

create table emp_sal10000 as  
    select employee_id, first_name, salary from employees where 1=2;
    
create table emp_sal15000 as  
    select employee_id, first_name, salary from employees where 1=2;
    
create table emp_sal20000 as  
    select employee_id, first_name, salary from employees where 1=2;

create table emp_sal25000 as  
    select employee_id, first_name, salary from employees where 1=2;
    
insert first
    when salary <= 5000 then
     into emp_sal5000 values (employee_id, first_name,salary)
    when salary <= 10000 then
     into emp_sal10000 values (employee_id, first_name,salary)
     when salary <= 15000 then
     into emp_sal15000 values (employee_id, first_name,salary)
     when salary <= 20000 then
     into emp_sal20000 values (employee_id, first_name,salary)
     when salary <= 25000 then
     into emp_sal25000 values (employee_id, first_name,salary)
    select employee_id, first_name, salary from employees;
    
select count(*) from emp_sal5000;
select count(*) from emp_sal10000;
select count(*) from emp_sal15000;
select count(*) from emp_sal20000;
select count(*) from emp_sal25000;

-- 8.7.4. PIVOTING INSERT
create table sales(
    employee_id NUMBER(6),
    week_id NUMBER(2),
    sales_mon NUMBER(8,2),
    sales_tue NUMBER(8,2),
    sales_wed NUMBER(8,2),
    sales_thu NUMBER(8,2),
    sales_fri NUMBER(8,2));
    
INSERT INTO sales VALUES(1101, 4, 100, 150, 80,60,120);
INSERT INTO sales VALUES(1102, 5, 300, 300,230, 120, 150);
COMMIT;
SELECT * FROM sales;

create table sales_datA(
employee_id NUMBER(6),
week_id NUMBER (2),
week_day VARCHAR2(10),
sales NUMBER (8,2)
);

SELECT * FROM SALES_DATA;

-- and , then 이 딱히 없다. 넣을순 있지만, 안넣어도됨. 
INSERT ALL
    INTO sales_data
    VALUES(employee_id, week_id, 'SALES_MON', sales_mon)
    INTO sales_data
    VALUES(employee_id, week_id, 'SALES_TUE', sales_tue)
    INTO sales_data
    VALUES(employee_id, week_id, 'SALES_WED', sales_wed)
    INTO sales_data
    VALUES(employee_id, week_id, 'SALES_THU', sales_thu)
    INTO sales_data
    VALUES(employee_id, week_id, 'SALES_FRI', sales_fri)
    select employee_id, week_id, sales_mon, sales_tue, 
        sales_wed, sales_thu, sales_fri
    from sales;
    
    
select  * from sales_data;


-- 8. 연습문제 

--8.1. 
create table emp_salary_info as
    select  employee_id,first_name, salary, commission_pct
    from employees
    where 1=2;

create table emp_hiredate_info as
    select  employee_id,first_name,hire_date, department_id
    from employees
    where 1=2;

insert all
    into emp_salary_info 
    values (employee_id,first_name, salary, commission_pct)
    into emp_hiredate_info
    values (employee_id,first_name,hire_date, department_id)
    select * from employees;
    

-- 8.2. 
insert into employees
VALUES (1030, 'KilDong', 'Hong', 'HONGKD','010-1234-5678',
        '2018/03/20', 'IT_PROG', 6000, 0.2, 103,60);

SELECT * FROM EMPLOYEES;

-- 8.3. 

UPDATE Employees
SET salary = salary * 1.1 
where employee_id =1030;

SELECT * FROM EMPLOYEES;

-- 8.4. 

delete from employees
where employee_id = 1030;

SELECT * FROM EMPLOYEES;

-- 8.5. 

select employee_id, first_name, hire_date, 
        to_char(hire_date,'YYYY') AS YR
FROM EMPLOYEES
WHERE hire_date between '01/01/01' and '03/12/31';
DROP TABLE emp_yr_2003;

CREATE TABLE emp_yr_2001 (
    employee_id NUMBER(6,0), 
    first_name VARCHAR2(20 BYTE), 
    hire_date DATE, 
    YR VARCHAR2(4));

CREATE TABLE emp_yr_2002 (
    employee_id NUMBER(6,0), 
    first_name VARCHAR2(20 BYTE), 
    hire_date DATE, 
    YR VARCHAR2(4));
    
CREATE TABLE emp_yr_2003 (
    employee_id NUMBER(6,0), 
    first_name VARCHAR2(20 BYTE), 
    hire_date DATE, 
    YR VARCHAR2(4));
 

select * from emp_yr_2003;

insert all
    when TO_CHAR(HIRE_DATE,'YYYY') = '2001' then
    into emp_yr_2001 
    values (employee_id, first_name, hire_date,yr)
    when TO_CHAR(HIRE_DATE,'YYYY') = '2002' then
    into emp_yr_2002    
    values (employee_id, first_name, hire_date,yr)
    when TO_CHAR(HIRE_DATE,'YYYY') = '2003' then
     into emp_yr_2003    
    values (employee_id, first_name, hire_date,yr)
    select employee_id, first_name, hire_date,
    TO_CHAR(HIRE_DATE,'YYYY') AS YR FROM employees;
    
    
-- 6.

insert first 
    when TO_CHAR(HIRE_DATE,'YYYY') = '2001' then
    into emp_yr_2001  values (employee_id, first_name, hire_date,yr)
    when TO_CHAR(HIRE_DATE,'YYYY') = '2002' then
    into emp_yr_2002  values (employee_id, first_name, hire_date,yr)
    when TO_CHAR(HIRE_DATE,'YYYY') = '2003' then
     into emp_yr_2003 values (employee_id, first_name, hire_date,yr)
     select employee_id, first_name, hire_date,
    TO_CHAR(HIRE_DATE,'YYYY') AS YR FROM employees;
    
    
    
-- 
create table emp_personal_info as
    select  employee_id,first_name, last_name, email, phone_number
    from employees
    where 1=2;

create table emp_office_info as
    select  employee_id,hire_date,salary,commission_pct,manager_id, department_id
    from employees
    where 1=2;

insert all
    into emp_personal_info 
    values (employee_id,first_name, last_name, email, phone_number)
    into emp_office_info
    values (employee_id,hire_date,salary,commission_pct,manager_id, department_id)
    select * from employees;
    
select * from emp_personal_info;
select * from emp_office_info;


--

create table emp_comm as
    select employee_id, commission_pct from employees where 1=2;
create table emp_nocomm as select employee_id, commission_pct from employees where 1=2;

drop table emp_nocomm;

INSERT all
 when commission_pct is null then
 into emp_comm values (employee_id, commission_pct)
 when commission_pct is not null then
 into emp_nocomm values(employee_id, commission_pct)
 select employee_id, commission_pct from employees;
 
 select * from emp_nocomm;
 
 --
 
 
create table emp as
select employee_id as empno, first_name as ename,
        salary as sal, department_id as deptno
from employees;
 
 
-- 10장 . 테이블 생성과 관리  

create table "Test" (c1 varchar2(1));

select * from Test;

select * from "Test";

drop table dept;
create table dept(
    deptno number(2),
    dname varchar2(14),
    loc varchar2(13)
    );
    
desc dept;

drop table emp;
create table emp(
    empno number(4,0),
    ename varchar2(10),
    job varchar2(9),
    mgr number(4,0),
    hiredate date,
    sal number(4,0),
    comm number (7,2),
    depto number(2,0)
);

drop table emp3;
CREATE TABLE EMP2 AS SELECT * FROM employees;

CREATE  TABLE EMP3 AS SELECT * FROM employees where 1=2;

select count(*) from emp2;

select count(*) from emp3;

create table emp_dept50 as
select employee_id , first_name, salary*2 as ann_sal, hire_date
    from employees
    where department_id = 50;
    
select * from emp_dept50;
    
alter table emp_dept50
add (job varchar2(10));

select * from emp_dept50;

alter table emp_dept50
add (job2 varchar2(10) default 'NONE');

ALTER table emp_dept50
rename column job to job_id;

desc emp_dept50;
    