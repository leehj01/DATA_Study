select * from user_constraints;

-- 11.1.2. �� ���� ���� ���� 
create table emp4(
    empno number(4) constraint emp4_empno_pk primary key,
    email varchar2(10) not null,
    sal number(7,2) CONSTRAINT emp4_sal_ck CHECK(sal<= 10000),
    deptno number(2) CONSTRAINT emp4_deptno_dept_deptid_fk
                    REFERENCES departments(department_id)
                    );


-- 11.1.3. ���̺� ���� ���� ���� 

create table emp5(
    empno number(4),
    email varchar2(10) not null,
    sal number(7,2),
    deptno number(2),
    constraint emp5_empno_pk PRIMARY KEY (empno),
    constraint emp5_sal_ck check(sal<=10000),
    constraint emp5_deptno_dept_deptid_fk
        foreign key(deptno) references departments(department_id)
    );
    
-- 2. �������� ���� 
select * from user_constraints where table_name = 'EMP5';
ALTER TABLE  emp5
    drop constraint sys_c007047;

desc emp5;

alter table emp5
    modify ename varchar2(10) not null;


-- 2. ���� ���� ����
-- 11.2.1. NOT NULL ���� ���� : NOT NULL ���� ����, ���� �� ����0�������θ� ������ �� �ִ�.

-- 11.2.2. UNIQUE ���� ���� : ������ �����ؾ��� . NULL���� ���� �� ���� 

ALTER TABLE emp4
ADD (nickname varchar2(20));
-- �г��� �� �߰�

SELECT * FROM emp4;

ALTER TABLE emp4
ADD CONSTRAINT emp4_nickname_uk UNIQUE(nickname);

INSERT INTO emp4 values(1000, 'KILDONG', 2000,10,null); 
INSERT INTO emp4 values(2000, 'KILSEO', 3000,20,'KSEO');

-- 2.3. PRIMARY KEY ���� ����
drop table depts;

CREATE TABLE depts(
    deptno NUMBER(2),
    dname VARCHAR2(14),
    loc VARCHAR2(13),
    CONSTRAINT depts_dname_uk UNIQUE(dname),
    CONSTRAINT depts_deptno_pk PRIMARY KEY(deptno));

-- deptno NUMBER(2) CONSTRAINT depts_deptno_pk PRIMARY KEY,
-- >>  �������� ���� ������ �ɾ �����ϴ�. 

-- 2.4. FOREIGN KEY ���� ����
-- ���̺� ���� ���踦 ������ 

DROP TABLE EMPS CASCADE CONSTRAINTS;

create table emps(
    empno number(4),
    email varchar2(10) not null,
    job  varchar2(9),
    mgr number(4),
    sal number(7,2),
    comm number(7,2),
    deptno number(2) not null,
    constraint emp_empno_pk PRIMARY KEY (empno),
    constraint emp_depts_deptno_fk
        foreign key(deptno) references depts(deptno));
        
-- deptno number(2)
        --CONSTRAINT emps_depts_deptno_fk REFERENCES depts(deptno)
        -- >> �������� �����ϴ� �� 
        
-- 11.2.5. CHECK ���� ����
-- �� ���� �����ؾ��ϴ� ������ ��������. 
-- ���� ���� ���� CHECK���������� ���� �� ����.
-- ���� ������ ���� ���� �Ѱ� ���� 
-- ������, ���̺� �������� ���� �� �� ����. 

select * from emp4;
insert into emp4 values(9999, 'King', 20000,10); -- check�������� ������ ������ �߻��Ѵ�.
-- �������ǿ� �����

---
-- 11.3.  �������� ����
-- 11.3.1 ���� ���� �߰�
ALTER TABLE emps
ADD CONSTRAINT emps_mgr_fk
    FOREIGN KEY(mgr) REFERENCES emps(empno);

-- 11.3.2. ���� ���� ��ȸ
-- ��� ���� ���� ���ǿ� �̸��� ���� ���� USWER_CONSTRAINTS ���̺��� ����
-- USER_CONS_COLUMNS �信�� ���� ���� �̸��� ���õ� ���� ��

SELECT constraint_name, constraint_type, status
FROM USER_CONSTRAINTS
WHERE table_name = 'EMPS';

-- 11.3.3. ���� ���� ����

ALTER TABLE depts DROP PRIMARY KEY CASCADE;

-- 11.3.4. ���� ���� ��Ȱ��ȭ
-- ���Ἲ ���� ������ ��Ȱ��ȭ �ϱ� ���� ALTER TABLE ������ DISABLE���� ����
-- �������� ���Ἲ ���� ������ ��Ȱ��ȭ �ϱ� ���ؼ� CASCADE �ɼ��� ������
insert into emp4 values(9999, 'King', 20000,10,'KING'); -- �Ұ���

select * from user_constraints where table_name = 'EMP4';
alter table emp4 disable constraint emp4_sal_ck;

insert into emp4 values(9999, 'King', 20000,10,'KING'); -- ��������

-- 11.3.5. ���� ���� Ȱ��ȭ
alter table emp4 enable validate constraint emp4_sal_ck;  -- validate �� �ϸ� �ȵ�.
alter table emp4 enable novalidate constraint emp4_sal_ck; --  novalidate �� �ؾ���

-- 12.1. ��(VIEW)
-- VIEW�� ���̺� �Ǵ� �ٸ� �並 ���ʷ� �ϴ� ���� ���̺��Դϴ�.

-- 12.1.1. ���� ��� ����
-- ������� ���� �ڵ� ������ �����ǹǷ� ������ ���̽� �׼����� �����ϱ� ���� �����
-- ������ ���Ǹ� ���� ������ֱ� ������ ������� ������ ������ �����ϰ� ����.

-- 12.1.2. �ܼ� ��� ���� ��

SELECT * FROM USER_VIEWS;
-- view �� ��ȸ

-- 12.2. �����, ������ �˻�,����,����
-- 12.2.1. �� ���� ����
SELECT * FROM USER_ROLE_PRIVS; -- ���� ����ڿ��� �־��� ���� ���
SELECT * FROM USER_SYS_PRIVS; -- ���� ����ڿ��� �־��� ������ ���

-- 12.2.2. �����
-- 1) �� �����ϱ�
CREATE VIEW emp_view_dept60
as select employee_id, first_name, last_name, job_id, salary
    from employees
    where department_id =60;
    
desc emp_view_dept60;
select * from emp_view_dept60;
drop view emp_view_dept60;

-- 2)�� ���� ������������ ��Ī ����ϱ�
CREATE VIEW emp_view_dept60_salary
as select employee_id as empno, first_name|| ' '|| last_name as name,
         salary as monthly_salary
    from employees
    where department_id =60;
    
create view emp_dept60_salary( empno,name, nontly_salary)
as select
    employee_id,first_name|| ' '|| last_name,salary
     from employees
    where department_id =60;
    
select * from emp_dept60_salary;

-- 12.2.3. �� ����

select * from user_views; -- ����� �信 ���� ���� ���

-- 12.2.4. �� ����
-- or replace �ɼ��� ��� �� �̸��� �����ϴ��� �䰡 �����ǵ��� ��. 

CREATE OR REPLACE VIEW emp_dept60_salary
as select
    employee_id as empno, first_name|| ' '|| last_name as name,
    job_id as job,  salary 
    from employees
    where department_id =60;

-- 12.2.5. ���պ� ���� 
-- �ΰ� �̻� ���̺�� ���� ���� ���÷��� �ϴ� �並 ������ 


create view emp_view
as select 
    e.employee_id as id, 
    e.first_name as name,
    d.department_name as department,
    j.job_title as job
from employees e
left join departments d on e.department_id = d.department_id
join jobs j on e.job_id = j.job_id;

select * from emp_view;

select * from emp_details_view; -- hr ��Ű���� �̹� ���ǵ� ���� ���� ��


--12.2.6. �����
-- ��� ������ ���̽����� �⺻ ���̺��� ������� �ϹǷ� ������ �ս� ���� �並 ������. 

DROP VIEW emp_dept60_salary;

-- 12.3. �並 �̿��� DML ���� 
--12.3.1

CREATE OR REPLACE VIEW emp_test1234
as select employee_id, last_name, email, hire_date
from employees;

insert into emp_test1234
values (200, 'HEO', 'HEOJK', '02/02/02');   -- cannot insert NULL into  �̶� ����....?
-- NOT NULL�� ���� VIEW�� ���ؼ� ���õ��� ����...?


-- 13�� 

-- 13.1.1. ������ ����

create sequence depts_seq
    increment by 1
    start with 91 
    maxvalue 100
    nocache
    nocycle;

-- 13.1.2.

select sequence_name , min_value, max_value, increment_by, last_number
from user_sequences;

select object_name
from user_dbjects
where object_type = ' SEQUENCE';

-- 13.1.4.
INSERT INTO depts (deptno, dname, loc)
values (depts_seq.NEXTVAL, 'MARKETING', 'SAN DIEGO');


SELECT depts_seq.CURRVAL
FROM dual;

-- 13.1.5. 
ALTER SEQUENCE depts_seq
    MAXVALUE 99999;
    
-- 13.1.6
DROP SEQUENCE depts_seq;