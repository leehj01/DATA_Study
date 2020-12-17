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

select first_name as  �̸�,  salary  �޿�
from employees;

 select first_name , last_name , salary
 from employees;
 
 select first_name || ' ' || last_name || '''s �޿���' || salary 
 from employees;
 
 select rowid, rownum, employee_id, first_name
 from employees;
 -- row �� ������ �ִ�, ���� id �� num 
 
select first_name , job_id, department_id 
from employees
where job_id = 'IT_PROG';

select first_name, department_id
from employees
where department_id > 50;

select count(*) from employees
where department_id = 50;
-- count(*) ��� ���� ��

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
-- 2003 �⵵�� �Ի��� ���, date �� ��Ʈ�� ������ ���� 

select first_name, salary, hire_date
FROM employees
WHere first_name BETWEEN 'A' and 'Bz';
-- ���ڵ� ���� , �׷��� B��� �Է��ϸ� �ȵǰ� Bz���� �Է��ؾ���. 

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
-- ���� ����� 0 �̴�. �ֳ��ϸ�,  null�� ������ �ȵǱ� ������, ����..

select count(*) from employees
where commission_pct is null;
-- is null, is not null �� �ؾ� ���� ���� �� �ִ�. 

select first_name , salary*12  
from employees
order by 2, first_name ;

select first_name , hire_date  
from employees
order by hire_date desc, first_name asc ;

--
-- 1. ��� ����� �����ȣ, �̸�, �Ի���, �޿��� ����ϼ���. 
select employee_id, first_name, last_name, hire_date, salary
from employees;

-- 2. ��� ����� �̸��� ���� �ٿ� ����ϼ���. ����Ī�� name ���� �ϼ���.
select first_name || ' ' || last_name as "name"
from employees;

-- 3. 50�� �μ� ����� ��� ������ ����ϼ���.
select * from employees
where department_id = 50;

-- 4. 50�� �μ� ����� �̸�, �μ���ȣ, �������̵� ����ϼ��� .
select first_name , last_name, department_id , job_id
from employees
where department_id = 50;

-- 5. ��� ����� �̸�, �޿� �׸��� 300�޷� �λ�� �޿��� ����ϼ���.
select first_name , last_name, salary + 300
from employees;

-- 6. �޿��� 10000���� ū ����� �̸��� �޿��� ����ϼ���
select first_name, salary
from employees
where salary > 10000;

-- 7. ���ʽ��� �޴� ����� �̸��� ����, ���ʽ����� ����Ͻÿ�.
select first_name, job_id, commission_pct
from employees
where commission_pct is not null;

-- 8. 2003�⵵ �Ի��� ����� �̸��� �Ի��� �׸��� �޿��� ����ϼ���.(��Ʈ�������ڻ��)
select first_name, hire_date, salary 
from employees
where hire_date between '03/01/01' and '03/12/30';

-- 9. 2003�⵵ �Ի��� ����� �̸��� �Ի��� �׸��� �޿��� ����ϼ���. (like ������ ���)
select first_name, hire_date, salary 
from employees
where hire_date like '03/%/%';

-- 10. ��� ����� �̸��� �޿��� �޿��� ���� ������� ���� ��� ������ ����ϼ���.
select first_name , salary
from employees
order by salary desc;

-- 11. �� ���Ǹ� 60�� �μ��� ����� ���ؼ��� ���� �ϼ���.
select first_name , salary
from employees
where department_id = 60
order by salary desc;

-- 12.  �������̵� IT_PROG �̰ų�, SA_MAN�� ����� �̸��� �������̵� ����ϼ���.
SELECT first_name , job_id
from employees 
where job_id = 'IT_PROG' or job_id = 'SA_MAN';

-- 13. Steven King ����� ������ "Steven King  ����� �޿��� 24000�޷��Դϴ�"�������� ����ϼ���.
SELECT first_name ||' '|| LAST_NAME ||'����� �޿���'||SALARy||'�޷��Դϴ�' AS info
from employees
where first_name = 'Steven' and last_name = 'King';

-- 14. �Ŵ��� ������ �ش��ϴ� ����� �̸��� �������̵� ����ϼ���.
select first_name , job_id
from employees
where JOB_ID LIKE '%MAN';

-- 15. �Ŵ��� ������ �ش��ϴ� ����� �̸��� �������̵� ���� ���̵� ������� ����ϼ���.
select first_name , job_id
from employees
where JOB_ID LIKE '%MAN'
ORDER BY job_ID ;

-- coderby �� �ý�����

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

select first_name ||''|| last_name || '''s �޿���'||salary 
from employees;












