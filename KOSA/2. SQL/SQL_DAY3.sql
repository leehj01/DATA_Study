-- nvl(��, ���ϰ���ȯ��)
select first_name, salary+salary*nvl(commission_pct, 0)
from employees;

-- nv2(��, ���� �ƴѰ��, ���ϰ��)
select first_name, salary+salary*nvl2(commission_pct,commission_pct,0) as salary
from employees;

select first_name, nvl2(commission_pct,salary+salary*commission_pct,salary) as salary
from employees;
-- nvl2 �� ����ϴ� ������ ���ʿ��� ������ ���ϱ� ���ؼ���. ���� �������� ���� ���� �� ��ȣ

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
union  -- �������ϱ�
select first_name, coalesce(salary*commission_pct,0) as salary
from employees
where salary * commission_pct is null;

-- DECODE (ǥ����, �񱳰�1, ���1, �񱳰�2, ���2,,,)
select job_id, salary,
        decode(job_id, 'IT_PROG', salary*1.10,
                        'FI_MGR', salary*1.15,
                        'FI_ACCOUNT',salary*1.20,
                        salary)
        as revised_salary
from employees;
                    

-- CASE ǥ���� WHEN �񱳰�1 THEN ���1
-- CASE WHEN ���� THEN ������ ���ϰ�� ���
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


-- 4��. �׷��Լ�
-- 4.1.  

select avg(salary), max(salary),min(salary), sum(salary)
from employees
where job_id like 'SA%';
--  null ���� ������, ���, �ִ�, �ּ�, �հ踦 ���

SELECT min(hire_date), max(hire_date)
from employees;
-- �̷��� �̴� ���� ���� �Ի��� ����� �Ի��ϰ� ���߿� �Ի��� ����� �� ���

select min(first_name) ,max(first_name) from employees;

select max(salary) from employees;
-- ���� ���� ������ ������. ���� ���� ������ �޴� ����� �̸��� �˰������ ������

select first_name, max(salary) from employees;
-- �̰� �˰������ ���������� �ذ��ؾ���. 7�忡 ����..

select * from employees;

-- 80�� �μ��� 50�� �μ��� �޿� ��հ� ǥ�������� ����ϼ���.
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
-- ����ó�� ���Ѱ� �ƴ϶�, �׷쳢�� ���� ������ �ϰ� ������ , union������,
-- �̰� �ʹ� ���ŷӱ� ������ , group-by�� ����Ѵ�.

-- 2.1 group by ���
select department_id , AVG(salary)
from employees
group by department_id ;

-- 2.2. �ϳ� �̻��� ���� �׷�ȭ
select department_id, job_id, sum(salary)
from employees
group by department_id, job_id;
--  �ΰ��� ���� �� ������, ������ �߿��ϴ�. ���� �׷�ǰ� ���߿� �׷�ȴ�. 


-- 2.3.  �׷��Լ��� �߸� ����� ����
-- select ���� �׷��Լ��� �ƴ� ��� ���̳� ǥ������ group by���� �־����.
-- where ���� ����Ͽ� �׷��� ���� �Ҽ� �����ϴ� 

select department_id, count(first_name)
from employees;
-- �̷��� �ϸ� ���� �߻�

select department_id, count(first_name)
from employees
group by department_id;
-- �̷��� �׷��� �����������.

select department_id , AVG(salary)
from employees
where avg(salary) > 2000
group by department_id;
--  �̷��� where ���� ����Ͽ� �׷������� �ȵ�. �׷��� having ���� ���.

-- having
-- where ���� ����Ͽ� �˻��ϴ� ���� ���� �ϴ� �Ͱ� �Ȱ��� ������� having�� ���
-- [ HAVING goup_by_condition ]

-- 3.1. having ���
select department_id, ROUND(avg(salary),2)
from employees
group by department_id
having AVG(salary) > 8000;

-- �޿� ����� 8000�� �ʰ��ϴ� �� ������ ���Ͽ� ������ ������ �޿� ����� ���
-- sales ������ ����ϴ� ����� �����ϰ� �޿� ������� ����� ���� 
select job_id, avg(salary) payroll
from employees
where job_id not like 'SA%'
group by JOB_ID
having AVG(salary) > 8000
order by AVG(salary);

-- 4. GROUP SET

-- �μ��� �޿��� ��հ� ������ �޿��� ���
SELECT department_id , round(avg(salary),2)
from employees
group by department_id;
union -- department ��  jobid �� Ÿ���� �޶�, ������
SELECT job_id, round(avg(salary),2)
from employees
group by job_id;

SELECT TO_CHAR(department_id) , round(avg(salary),2) -- �μ��� ���ڷ� ���� �����Ŵ
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
-- ���Ʒ� �ΰ��� ���ϱ�. 
SELECT DEPARTMENT_ID , JOB_ID, ROUND(AVG(SALARY),2)
FROM EMPLOYEES
GROUP BY grouping sets (DEPARTMENT_ID, JOB_ID) -- �ݵ�� �Ұ�ȣ �����ֱ� 
order by department_id, job_id;

-- 5��
-- 5.1. ROLLUP, CUBE ���
SELECT DEPARTMENT_ID, JOB_ID, ROUND(AVG(SALARY),2),COUNT(*)
FROM EMPLOYEES
GROUP BY DEPARTMENT_ID, JOB_ID
ORDER BY DEPARTMENT_ID, JOB_ID;
-- ���⿡�� �Ұ谡 ��������� ����


SELECT DEPARTMENT_ID, JOB_ID, ROUND(AVG(SALARY),2),COUNT(*)
FROM EMPLOYEES
GROUP BY ROLLUP(DEPARTMENT_ID, JOB_ID)
ORDER BY DEPARTMENT_ID, JOB_ID;


SELECT DEPARTMENT_ID, JOB_ID, ROUND(AVG(SALARY),2),COUNT(*)
FROM EMPLOYEES
GROUP BY CUBE( DEPARTMENT_ID, JOB_ID)
ORDER BY DEPARTMENT_ID, JOB_ID;

-- 6��
SELECT 
    NVL2(department_id, DEPARTMENT_ID||'',
        DECODE(GROUPING(DEPARTMENT_ID),1,'�Ұ�')) AS �μ�,
    NVL(JOB_ID, DECODE(GROUPING(JOB_ID),1,'�Ұ�')) AS ����,
    ROUND(AVG(SALARY),2) AS ���, 
    COUNT(*) AS ����Ǽ�
FROM employees
GROUP BY CUBE(department_ID, JOB_ID)
ORDER BY DEPARTMENT_ID, JOB_ID;
-- ||'' : '' �� ������ ���ڰ� ��.

    
-- 7 �� 
SELECT 
    NVL2(department_id, department_id||'',
        DECODE(GROUPING_ID(department_id,job_id),2,'�Ұ�',3,'�հ�')) AS �μ�,
    NVL(JOB_ID, DECODE(GROUPING_ID(department_id,job_id),1,'�Ұ�',3,'�հ�')) AS ����,
    GROUPING_ID(department_id,job_id) AS GID,
    ROUND(AVG(SALARY),2) AS ���, 
    COUNT(*) AS ����Ǽ�
FROM employees
GROUP BY CUBE(department_ID, JOB_ID)
ORDER BY DEPARTMENT_ID, JOB_ID;

-- 8�� ��������
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
-- �� ����?

-- 8.7. 
select job_id , count(*)
from employees 
where department_id =50
group by department_id, job_id
having count(*) < 10;

-- 8 .8 
select to_char(hire_date,'YYYY') AS "�Ի�⵵",
        ROUND(avg(salary)) as �޿����,
        count(*) as �����
from employees
group by to_char(hire_date,'YYYY')
order by �Ի�⵵;


-- 8.9.
select to_char(hire_date,'YYYY') as �Ի�⵵,
        to_char(hire_date,'MM') AS �Ի��,
        round(avg(salary)) as �޿���� , count(*) as �����
from employees
group by rollup(to_char(hire_date,'YYYY'), to_char(hire_date,'MM'))
order by �Ի�⵵,�Ի��;


-- 8.10 
select to_char(hire_date,'YYYY') as �Ի�⵵,
        to_char(hire_date,'MM') AS �Ի��,
        round(avg(salary)) as �޿���� , count(*) as �����
from employees
group by cube(to_char(hire_date,'YYYY'), to_char(hire_date,'MM'))
order by �Ի�⵵,�Ի��;

--8.11
select 
    NVL(to_char(hire_date,'YYYY'),DECODE(GROUPING_ID(to_char(hire_date,'YYYY')),1,'�հ�')) as �Ի�⵵,
    NVL(to_char(hire_date,'MM'),DECODE(GROUPING_ID(to_char(hire_date,'MM')),1,'�Ұ�')) AS �Ի��,
    GROUPING_ID(to_char(hire_date,'YYYY'),to_char(hire_date,'MM')) AS GRID,
    round(avg(salary)) as �޿���� , count(*) as �����
from employees
group by cube(to_char(hire_date,'YYYY'), to_char(hire_date,'MM'))
order by �Ի�⵵,�Ի��;

-- 5�� �м��Լ�
-- �Լ��� ���Ŀ� ����, over() �ڿ� ���� ���� �޶���. �� ������ �����ؾ��Ѵ�. 
SELECT department_id,
    round(avg(salary) over (partition by department_id),2)
from employees;

select department_id, round(avg(salary),2)
from employees
group by department_id;

-- �� �ΰ����� �ڵ带 ���� �׷��Լ��� �м��Լ��� ���̸� �����غ���.
-- �׷��Լ��� ������ ���� ���� ������, �м��Լ��� �ٳ��´�.


-- 1.1. ������ ��Ÿ���� �Լ� 
select employee_id, department_id, salary,
    RANK()  OVER(ORDER BY salary DESC) sal_rank, -- �ش簪�� �������� ( �ߺ����� ��� )
    DENSE_RANK() OVER(ORDER BY salary DESC) sal_dense_rank, -- �ߺ������� ������� x
    ROW_NUMBER()OVER(ORDER BY salary DESC) sal_number --������ �����ϴ� ������� ��ȣ ����. �Ϸù�ȣ����
from employees;

-- 1.2 ��������� ����

select employee_id, department_id, salary,
    CUME_DIST() OVER (ORDER BY salary DESC) sal_cume_dist,
    -- �ִ밪 1�� �������� �л�� ���� ����. �ּڰ��� �ִ� ������ ������� ��ġ �ǹ�
    -- ó�� ���� 1�̴�. 
    PERCENT_RANK() OVER (ORDER BY salary DESC) sal_pct_rank
    -- �ִ밪�� 1�� �������� ������ ���տ��� Ư������ ����� ������ ����. ù��° ��ġ�� 0���� ���� 
from employees;

-- 1.3.  �����Լ�

select first_name, salary,
    round(RATIO_TO_REPORT(salary) OVER (),4) as salary_ratio
from employees
where job_id = 'IT_PROG';
-- �ش� �� ���� ������� �Ҽ������� ������. �׷쳻���� �ش��ϴ� ������� ���� �� ����. 

--1.4 �й��Լ�

select first_name, department_id, salary,
    NTILE(10) OVER ( ORDER BY salary DESC) as sal_quart_tile
from employees
where department_id = 50;
--  ��ü �������� ������ n���� �������� ������ ǥ������. 
-- ���� row �� �յ��ϰ� ������ ������, ���������� �߰���.  

-- 1.5. LAG, LEAD 
SELECT EMPLOYEE_ID, 
    LAG(salary,1,0) over ( ORDER BY salary ) as lower_sal, 
    salary,
    LEAD(salary,1,0) over ( ORDER BY salary ) as higher_sal
from employees
order by salary;
-- LAG( column, n, �ʱⰪ) : ���� n ��° ���� ���� ������. 
-- LEAD( column, n, �ʱⰪ) : ���� n ��° ���� ���� ������. 

-- 1.6. LISTAGG
select department_id,
    Listagg(first_name,',') WITHIN GROUP(ORDER BY hire_date) as names
    -- group �ȿ��� ��� �����ؾ������� �˼� ����.
    -- ������ ������ ����ؾ� �Ұ��� �̸����� �ؼ� �ѹ��� ����� �� ����. 
from employees
group by department_id;
-- LISTAGG(�ϳ��� ������ ����ϰ� ���� ���̸�, ���� �����ϴ� ������)

select department_id, FIRST_NAME -- ��������. �׷��� ����ó�� ����. 
from employees
group by department_id;


-- 5.2. �������� 
-- 5.2.1.  FIRST_VALUE ,LAST_VALUE : ���ĵ� ���� ó���� / ������ �� ���� 
SELECT employee_id, 
    FIRST_VALUE(salary)
     OVER (ORDER BY salary
        ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS lower_sal,
    salary AS my_sal,
    LAST_VALUE(salary)
     OVER (ORDER BY salary
        ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS higher_sal
FROM employees;

-- 5.3. ����ȸ�� �Լ�
-- 5.3.1. regr_avgx /regr_avgy : x,y �� null�� �����ϰ� ����� ������
select
    avg(salary),
    regr_avgx(commission_pct, salary)
from employees;
-- ���Ʒ��� ���� �ǹ̸� ����
SELECT avg(salary)
from employees
where commission_pct IS NOT NULL;
    
-- 5.3.2. REGR_COUNT : �� �μ��� not null�ΰ��� �� 
SELECT 
    DISTINCT
        department_id,
        REGR_COUNT(manager_id, department_id)
            OVER(partition by department_id) "REGR_COUNT" -- �μ����� ��Ƽ���ؼ� ī���� ����
FROM  employees
ORDER BY department_id;

-- ���� ������ ���ϱ�
select department_id , count(*)
from employees
group by department_id
order by department_id;  -- �̰� null�� ���Ե� ���� ���´�.

--5.3.3. REGR_SLOPE ���� , REGR_INTERCEPT Y������ ��ȯ 
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

-- 5.3.4. REGR_R2(y,x) ������� - 1�� �������� ����. 

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

-- 4�� �ǹ����̺�

-- ����, ���̺� �����ϱ�. 
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

-- ���������Ʈ ���� ���������̺� �����
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

-- 5.5 ��������
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
