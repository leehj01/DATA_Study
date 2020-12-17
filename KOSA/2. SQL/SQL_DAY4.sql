-- 6.1. �����̶�

--6.2. ����Ŭ ����

-- 6.2.1. CARTESIAN PRODUCT : ���� ������ ����, �߸�, ���������� ��������� �� ����.
-- ��� ����� ���ϰ� �ǹǷ�, ���� ���� �����ϴ� ������ ����. ����� �������� ����. 

select first_name, department_name
from employees, departments;

SELECT first_name, employees.department_id, department_name
from employees, departments;
-- ���̸��� �ߺ��Ǹ�, ���̺� �̸� ���

select e.first_name, e.department_id, d.department_name
from employees e , departments d;
-- ���̺� �̸��� ��� ���� ������ from���� ���̺� ��Ī �̿� �� �� ����. 
-- ���̺� ��Ī�� �� ��, as ���� �ȵ�. 

--6.2.2. EQUL JOIN : 2���̻� ����Ǵ� ���� ���� �������� �����ϴ� ���� ��� 

-- �μ�����  id�� ���� ����� �̸��� id, �μ� �̸��� �����ֱ�
select e.first_name , e.department_id, d.department_name
from employees e , departments d
where e.department_id = d.department_id; -- ���� ���� 

select e.first_name , e.department_id, d.department_name
from employees e , departments d
where e.department_id = d.department_id -- ���� ���� 
and e.employee_id = 103;

-- ��� ����� �̸��� �����̸� ����ϼ���
select e.first_name, j.job_title
from employees e, jobs j 
where e.job_id = j.job_id;


-- �ڽ��� �Ŵ������� �� ���� �޿��� �޴� ����� �̸��� �޿�, �Ŵ����� �̸��� �޿� 
select e.first_name ,e.salary, m.first_name , m.salary
from employees e, employees m
where e.manager_id = m.employee_id and e.salary > m.salary;


-- 6.2.3. SELF JOIN  : ��ü������ ���̺��� ������. 
SELECT e.first_name as employee_name,
        m.first_name as manager_name
from employees e, employees m  -- ���� ���̺��� ���� �ٸ��� �����ϱ� ���ؼ� ����.
where e.manager_id = m.employee_id 
and e.employee_id = 103; -- and�� �����ָ�, 106���� ������(���嶧��), �� ��ü���� ������ �־��൵ ����
-- ����� �Ŵ��� ���̵�� �Ŵ����� �����ȣ�� ���� �� , �׸��� �װ� ���103�� ã��. 

SELECT e.first_name as employee_name,
        m.first_name as manager_name
from employees e, employees m  -- ���� ���̺��� ���� �ٸ��� �����ϱ� ���ؼ� ����.
where e.manager_id = m.employee_id 
and e.first_name = 'Steven' and e.last_name ='King';
--  ������ �Ŵ��� id �� ���� ������ null�̴�. �׷��� ���� ������ �ʴ´�.
-- �׷��� ����ϴ� ����.  outer join �̴�. 


--6.2.4. NON-EQUL JOIN
SELECT  e.first_name,j.min_salary , e.salary ,j.max_salary , j.job_title
from employees e, jobs j 
where e.salary
BETWEEN j.min_salary and j.max_salary
order by first_name;

desc jobs; --  ���̺��� ���� Ȯ���ϱ�. 

-- 6.2.5.  OUTER JOIN : (+) �� ����Ͽ� ����. 

SELECT e.first_name as employee_name,
        m.first_name as manager_name
from employees e, employees m  
where e.manager_id = m.employee_id (+) -- + �� ���̴ϱ�, ����. leftouter join 
-- null�� �ƴ� �ʿ� + �� �־��ش�. 
and e.first_name = 'Steven' and e.last_name ='King';
-- full outer join �� ���������ʾƼ�, ���ʴ� null���� ���� �������� �ʴ´�. 

SELECT e.employee_id, e.first_name, e.hire_date,
       j.start_date , j.end_date , j.job_id , j.department_id
from employees e, job_history j
where e.employee_id = j.employee_id 
order by j.employee_id;

SELECT e.employee_id, e.first_name, e.hire_date,
       j.start_date , j.end_date , j.job_id , j.department_id
from employees e, job_history j
where e.employee_id = j.employee_id(+)   -- �̷��� + �� �ϸ� �� ���´�.  
order by j.employee_id;


-- 3. �Ƚ����� 

--3.3.1. CROSS JOIN : ����Ŭ�� CARESIAN PRODUCT�� ���� ��� ���. �׳� �ٳ����� ��
-- ȿ������ ����. 
select employee_id, department_name
from employees
cross join departments;

-- 3.3.2. NATURAL JOIN
-- ��� ���� �̸��� ���� ���鿡 ���� ������.  
-- natural������ �ڵ����� �� ���̺��� ���� �̸��� ���� ���� equi���� ����
-- �̶�, ���� ������ ���� ������ �����̾����. 

select first_name, job_title
from employees natural join jobs;

select first_name, department_name
from employees
natural JOIN departments; -- table2 �̸��� ����
-- ���� 32�� �����µ� �� ������, MANGER, department �Ѵ� ���� ���� ����⿡ �׷��� 

select first_name, employee_id , department_id, department_name,manager_id
from employees
natural JOIN departments; -- table2 �̸��� ����


-- 3.3.3. USING JOIN
-- NATURAL ������ ��翭�� ���� ������ �̷���� , 
-- USING�� ����ϸ� ���ϴ� ���� ���ؼ��� ������ ��� ����  
select first_name, department_name 
from employees
join departments
using (department_id);  -- ���� 106�� ���� 

-- 3.3.4. ON JOIN
select department_name, street_address, city, state_province
from departments d
join locations l
ON d.location_id = l.location_id;  -- ��ġ id �� ���� �͵��� �ҷ�����

-- 3.3.4. 1) �������̺��� ����

-- ��� ����� �̸�, �μ��̸�, �μ��� �ּҸ� ��� 
select e.first_name, d.department_name, 
    l.street_address || ',' || l.city ||',' || l.state_province as address
from employees e
join departments d on e.department_id = d.department_id -- ����̸��� �μ��̸�
join locations l on d.location_id = l.location_id; -- �μ��� �ּ� 

-- 3.3.4. 2) where ������ ȥ��

select e.first_name  as name, d.department_name as department
from employees e
join departments d
on e.department_id = d.department_id
where employee_id = 103; -- join�� ������� ������. 

select e.first_name  as name, d.department_name as department,
        l.street_address ||','|| l.city||'.'||l.state_province as address
from employees e
join departments d
on e.department_id = d.department_id
join locations l
on d.location_id = l.location_id
where employee_id = 103;

-- 3.3.4. 3) on���� where �� �� ���� �߰�
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
-- LEFT/ RIGHT/ FULL�� ������. OUTER �� ���� ����. 
-- ������ �Ǵ� ���� �����Ѵ�. ��, ����� ������. 
SELECT e.employee_id, e.first_name, e.hire_date,
       j.start_date , j.end_date , j.job_id , j.department_id
from employees e
LEFT OUTER JOIN job_history j -- ������ �Ǵ��ʿ� ������ ����. ���̺� ����.
ON e.employee_id = j.employee_id 
order by j.employee_id;


--4. ��������

--4.1. �̸�, �μ����̵�, ���ø� �����ֱ�
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
        

-- 7��  ��������

-- 7.1. ��������

select salary from employees where first_name = 'Nancy';  -- 12008

select first_name, salary from employees where salary > 12008;


Select first_name, salary
from employees
where salary > (select salary
                from employees
                where first_name = 'Nancy');
-- ���������� �����Ų �� , �� ����� ���� ������ ����ϱ�.
                
-- 7.2. ������ ��������
select first_name, job_id, hire_date
from employees 
where job_id = (select job_id
                from employees
                where employee_id = 30);
                
-- 7.3.  ������ ��������
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
    


--4. ��ȣ ���� ��������
select first_name, salary
from employees a
where salary > (select avg(salary)
                from employees b
                where b.department_id =a.department_id );

-- 5. ��Į�� ��������

select first_name, (select department_name 
                    from departments d
                    where d.department_id = e.department_id) department_name
from employees e
order by first_name;


select first_name, department_name
from employees e
join departments d on (d.department_id = d.department_id)
order by first_name;

-- 7.6. �ζ��κ�
select row_number, first_name, salary
from (select first_name, salary, 
        row_number() over (order by salary desc) as row_number  
        -- �ݵ�� ��Ī�� �־���� ������������ ���� �ִ�.     
        from employees)
where row_number BETWEEN 1 AND 10 ;
-- ���������� ��� ���������� ���� �ִ�


-- 7.7. 3������
select rownum, first_name, salary 
from employees
order by salary desc;
-- rownum �� �����Ƿ� �Ǿ����� �ʱ� ������ �Ʒ����� ���.

select rownum, first_name, salary 
from ( select first_name, salary from employees
        order by salary desc) -- ������ ������������ ���� ������ 
where rownum between 1 and 10;

select first_name, salary
from (select first_name , salary from employees order by salary desc)
where rownum between 11 and 20; -- �̷��� �ϸ� �ȳ���
-- �ֳ��ϸ� rownum �� ù��° ���� ��ȸ���� ������ ���̾ȳ���.

select *
from (select first_name  salary, rownum as rnum
        from (select first_name , salary
            from employees 
            order by salary desc)
            )
where rnum between 11 and 20; -- Ư������ �Ϸ��� 3������ �ؾ���

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

-- 7.8. ����������

select employee_id, 
    lpad(' ',3*(level-1)) || first_name ||''|| last_name,LEVEL as "level_"
    --  level��ŭ ������ ä���ּ���(lpad �̿�)
FROM employees
start with manager_id is null 
connect by prior employee_id = manager_id ;
-- �Ŵ��� id �� null�� ������� ����.   
-- prior �� ��𿡺������� �߿��ϴ�. ����� ���� prior�� �ٿ��� 
   
SELECT employee_id, lpad(' ',3*(level-1))||first_name|| ' '||last_name, level
from employees
start with manager_id is null
connect by prior employee_id = manager_id 
order siblings by first_name; -- ���� ������ �����ϰڴ� 

SELECT employee_id, lpad(' ',3*(level-1))||first_name|| ' '||last_name, level
from employees
start with manager_id is null
connect by prior employee_id = manager_id 
order by first_name;

select employee_id, lpad(' ',3*(level-1)) || first_name || ' ' || last_name, LEVEL
FROM employees
START WITH employee_id = 113
connect by prior manager_id = employee_id ;


-- 9.1. ��������
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
