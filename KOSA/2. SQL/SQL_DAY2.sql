-- 3-2 �����Լ�

SELECT * from dual;
select sysdate from employees;
select sysdate from dual;

select initcap('Javaspecialist') from dual;

select lower('Javaspecialist') from dual;
select upper('Javaspecialist') from dual; -- �ҹ��ڷ� �ٲ���

select length('Javaspecialist') from dual; -- ������ ��
select lengthb('�ڹ�������') from dual;  -- bite ���� �˷��� 
-- utf-8 3bye


select concat('Java' , 'Specialist') from dual; -- �μ��� �ΰ��ۿ� �ȵ�. 
select 'Java' || 'Specialist'||'abc' from dual; -- ������ �����Ϸ���, || ���
select substr('Javaspecialist',5,7) from dual; -- ���� ���ϴ� �κ��� ������
select substrb('Javaspecialist',4,3) from dual; -- byte�� �������� �̱�
select instr('Javaspecialist','s') from dual;  -- 's' ���ڰ� ���° �ִ��� ã��
select instr('Javaspecialist','s',5) from dual;

select lpad(17600,10,'*') from dual; -- 10�ڸ��ε�, ��������  * �� ä���ּ���
select rpad('java',10,'-') from dual; -- �����ʿ� ������ �ڸ��� ���
select rpad(first_name,10,'*') from employees ; 

select ltrim('Javaspecialist','Jav') from dual; -- ���ʿ��� ������ ���ڸ� �ϳ��ϳ� ���ϴ°�.
-- java ��ä�� �������� ������ Jav ��  a �� �ߺ����� ���ֱ� �����̴�. 
select Rtrim('Javaspecialist','list') from dual; -- �ܾ ��ä�� ���� ���� �ƴ϶�, �ϳ��ϳ� ���°�
select Rtrim('Javaspecialist  ') from dual; -- �������ָ� ������ ������
select trim('      Javaspecialist   ') from dual; -- trim�� �յ��� ������ ������
select Replace('Javaspecialist','Java','BigData') from dual;
select Replace('Java   spe cialist',' ','') from dual; -- ���� �߰��� ������ ���ټ� ����
select translate('Javaspecialist','abcdefghijks','1234567890') from dual;
-- ���ڸ� �ϳ��� ���� ��Ű�� ��. ���εɰ� ������, �����ǰ�, / ���� ������ ���� �״�� ���� 


SELECT 
    RPAD(substr(first_name,1,3), Length(first_name),'*') as name,
    LPAD(salary, 10, '*') as salary
FROM
    employees
WHERE
    lower(job_id) = 'it_prog';
    
    
-- 3.3. ���� ǥ����

CREATE TABLE test_regexp (col1 varchar2(10)); -- ���̺� ����
DROP TABLE  test_regexp; -- ���̺� ����

insert into test_regexp values ('ABCDE01234');
insert into test_regexp values ('01234ABCDE');
insert into test_regexp values ('abcde01234');
insert into test_regexp values ('01234abcde');
insert into test_regexp values ('1-234-5678');
insert into test_regexp values ('234-567890');
commit;
-- ��Ŷ�� �����Ϸ��� ��. ���� ����������, �޸𸮿��� ���� �ٽ� ���� ������ �ȵǾ�����
DELETE from test_regexp;  -- ��ü ���� �� �����ϴ� ��. 

select *
from test_regexp;

-- 3.2. regexp_like �Լ�
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

-- 3.3 regexp_instr �Լ�
insert into test_regexp values('@!=)(9&%$#');
insert into test_regexp values('�ڹ�3');

select col1,
    regexp_instr(col1, '[0-9]') as data1,
    regexp_instr(col1, '%') as data2
from test_regexp;

-- 3.4. regexp_substr �Լ�

select col1, regexp_substr(col1,'[C-Z]+')
FroM test_regexp;

-- 3.5. regexp_replace�Լ�

select col1, regexp_replace(col1, '[0-2]+','*')
from test_regexp;


--3.6. gegexp �Լ� ���� ����

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
 

-- 4. ���� �Լ�

SELECT * from employees where department_id = 90;

select round(123.4567,2) from dual;

select round(-3.4), trunc(-3.4), ceil(-3.4), floor(-3.4) from dual;
select round(-3.6), trunc(-3.6), ceil(-3.6), floor(-3.6) from dual;
select round(3.4), trunc(3.4), ceil(3.4), floor(3.4) from dual;
select round(3.6), trunc(3.6), ceil(3.6), floor(3.6) from dual;

-- round trunc�� ��¥ Ÿ�Կ��� ��밡�� 
select round(to_date('20/04/26')) from dual;
select round(systimestamp) from dual; -- ����ð�
select round(to_date('20/04/26'),'Month') from dual;
-- �ϴ����� �ݿø��ؼ� ���� ��ȯ�϶�. 
-- to_date  ���ڸ� ��¥�� ��ȯ


-- 3.5. ��¥ �Լ�

select sysdate from dual; -- ������ ��¥�� ��ȯ�ϴ� �Լ�
select systimestamp from dual; -- ������ ��¥�� �ð��� ��ȯ�ϴ� �Լ�

-- 5.1 ��¥�� ����

select first_name, (sysdate - hire_date)/7 as "weeks"
from employees
where department_id = 60;

-- 5.2 ��¥ �Լ�

select first_name, sysdate, hire_date,
        months_between(sysdate, hire_date) as workmonth
        -- months_between(date1, date2) ��¥ ������ �� ���� ��ȯ
from employees
where first_name  = 'Diana';

select first_name, hire_date, ADD_months(hire_date,100)
 -- ADD_MONTHS( date, n) �� �� n�� date�� ����. 
from employees 
where first_name  = 'Diana';

select sysdate, next_day(sysdate, '��')
from dual;
-- next_day �Լ���  date ������ ��õ� ������ ��¥�� ã��. ������ ' ' �� ��.

select sysdate, last_day(sysdate)
from dual;
-- last_day(date) ���� ������ ��¥�� ã��

select sysdate, round(sysdate), trunc(sysdate)
from dual;
-- round(date[, 'fmt']) �ݿø��� date �� ��ȯ, fmt������ ����¥�� �ݿø�
-- trunc(date[, 'fmt']) fmt�� ��õ� ������ ���� ������ date�� ��ȯ, ������ ����� ���ڷ� ����

select trunc(Sysdate, 'Month') 
from dual;
-- year , month �� �ݿø��ϰų� ������ ������ ������ �� �ִ�.

-- 3.6. ��ȯ �Լ�

-- 6.3. TO_CHAR(date,'fmt') ��¥�� ���ڷ� ��ȯ
 select first_name , to_char(hire_date,'MM/YY') AS hiredmonth
 from employees
 where first_name= 'Steven';
 -- TO_CHAR(date,'fmt')  ��¥�� ���ڷ� ��ȯ 
 
select first_name,
TO_CHAR(hire_date, 'YYYY"��" MM"��" DD"��"') HIREDATE
FROM employees;
-- fm'YYYY"��" MM"��" DD"��" ���� ������������ ��¥ �Ǵ� ���� 0�� ���ŵ�
-- fx�� 0�� ����ִ� ������, ����Ʈ ����.

select first_name,
TO_CHAR(hire_date, 'fmDdspth "of" Month YYYY fmHH:MI:SS AM',
        'NLS_DATE_LANGUAGE=english') as HIREDATE
    FROM employees;
-- fm �� 0�� ��������.  Dd spth : DD �� ���� �� , SPTH : ����� ����
-- "of" ���ڸ� �־���. Month : 9�ڸ��� ���� ������ �߰��� �� �̸�
-- YYYY : ��, HH : �Ϸ� �� �ð� �Ǵ� �ð� , MI : ��, SS: �� , AM :���� ������ 

-- 6.4. TO_CHAR(number, 'fmt') ���ڸ� ���ڷ� ��ȯ

SELECT first_name, last_name , TO_CHAR(salary, '$999,999') salary
from employees
where first_name = 'David';
-- TO_CHAR(number, 'fmt')

select  to_char(2000000, '$999,999') salary
from dual; 
-- �� �����ڸ��� $999,999 �̰ͺ��� ª���� #### �� ����� ���´�.

select first_name, last_name, salary*0.123456 salary1,
        TO_CHAR(salary*0.123456, '$999,999.99') slary2
from employees
where first_name = 'David';

-- 6.5. TO_NUMBER �Լ�

SELECT to_number('$5,500.00','$99,999.99')- 4000 from dual;
-- to_number(char, 'fmt')

-- 6.6 TO_DATE �Լ� : ���� ��Ʈ���� ��¥ �������� ��ȯ 

SELECT first_name, hire_date
from employees
where hire_date = to_date('2003/06/17','YYYY/MM/DD');

SELECT FIRST_NAME, HIRE_DATE
FROM    employees
where hire_date = TO_DATE('2003��06��17��','YYYY"��"MM"��"DD"��"');


-- 8. ��������
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
        '###-###-####') as "��ȭ��ȣ"
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
    TO_CHAR(hire_date,'YYYY"��" MM"��" DD"��"') AS HIRE_DATE,
    ROUND(MONTHS_BETWEEN(sysdate,hire_date)) AS MONTH
FROM employees
where department_id = 30 
ORDER BY SALARY DESC;

-- 8.7
SELECT rpad(first_name || ' '|| last_name,17,'*') as "�̸�",
        to_char(salary + salary * commission_pct,'$99,999.99') as "�޿�"
from employees
where department_id = 80 and salary >10000
order by �޿� desc;