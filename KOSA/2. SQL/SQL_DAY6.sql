select * from user_constraints;

-- 11.1.2. 열 레벨 제약 조건 
create table emp4(
    empno number(4) constraint emp4_empno_pk primary key,
    email varchar2(10) not null,
    sal number(7,2) CONSTRAINT emp4_sal_ck CHECK(sal<= 10000),
    deptno number(2) CONSTRAINT emp4_deptno_dept_deptid_fk
                    REFERENCES departments(department_id)
                    );


-- 11.1.3. 테이블 레벨 제약 조건 

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
    
-- 2. 제약조건 종류 
select * from user_constraints where table_name = 'EMP5';
ALTER TABLE  emp5
    drop constraint sys_c007047;

desc emp5;

alter table emp5
    modify ename varchar2(10) not null;


-- 2. 제약 조건 종류
-- 11.2.1. NOT NULL 제약 조건 : NOT NULL 제약 조건, 열레 벨 제약0조건으로만 설정할 수 있다.

-- 11.2.2. UNIQUE 제약 조건 : 값들이 유일해야함 . NULL값을 가질 수 있음 

ALTER TABLE emp4
ADD (nickname varchar2(20));
-- 닉네임 열 추가

SELECT * FROM emp4;

ALTER TABLE emp4
ADD CONSTRAINT emp4_nickname_uk UNIQUE(nickname);

INSERT INTO emp4 values(1000, 'KILDONG', 2000,10,null); 
INSERT INTO emp4 values(2000, 'KILSEO', 3000,20,'KSEO');

-- 2.3. PRIMARY KEY 제약 조건
drop table depts;

CREATE TABLE depts(
    deptno NUMBER(2),
    dname VARCHAR2(14),
    loc VARCHAR2(13),
    CONSTRAINT depts_dname_uk UNIQUE(dname),
    CONSTRAINT depts_deptno_pk PRIMARY KEY(deptno));

-- deptno NUMBER(2) CONSTRAINT depts_deptno_pk PRIMARY KEY,
-- >>  열레벨로 제약 조건을 걸어도 가능하다. 

-- 2.4. FOREIGN KEY 제약 조건
-- 테이블 간의 관계를 설정함 

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
        -- >> 열레벨로 정의하는 것 
        
-- 11.2.5. CHECK 제약 조건
-- 각 행을 만족해야하는 조건의 ㄹ정의함. 
-- 단일 열은 복수 CHECK제약조건을 가질 수 있음.
-- 제약 조건의 수에 대한 한계 없음 
-- 열레벨, 테이블 레벨에서 정의 될 수 있음. 

select * from emp4;
insert into emp4 values(9999, 'King', 20000,10); -- check제약조건 때문에 에러가 발생한다.
-- 제약조건에 위배됨

---
-- 11.3.  제약조건 관리
-- 11.3.1 제약 조건 추가
ALTER TABLE emps
ADD CONSTRAINT emps_mgr_fk
    FOREIGN KEY(mgr) REFERENCES emps(empno);

-- 11.3.2. 제약 조건 조회
-- 모든 제약 조건 정의와 이름을 보기 위해 USWER_CONSTRAINTS 테이블을 질의
-- USER_CONS_COLUMNS 뷰에서 제약 조건 이름과 관련된 열을 봄

SELECT constraint_name, constraint_type, status
FROM USER_CONSTRAINTS
WHERE table_name = 'EMPS';

-- 11.3.3. 제약 조건 삭제

ALTER TABLE depts DROP PRIMARY KEY CASCADE;

-- 11.3.4. 제약 조건 비활성화
-- 무결성 제약 조건을 비활성화 하기 위해 ALTER TABLE 문장의 DISABLE절을 실행
-- 종속적인 무결성 제약 조건을 비활성화 하기 위해서 CASCADE 옵션을 적용함
insert into emp4 values(9999, 'King', 20000,10,'KING'); -- 불가능

select * from user_constraints where table_name = 'EMP4';
alter table emp4 disable constraint emp4_sal_ck;

insert into emp4 values(9999, 'King', 20000,10,'KING'); -- 가능해짐

-- 11.3.5. 제약 조건 활성화
alter table emp4 enable validate constraint emp4_sal_ck;  -- validate 로 하면 안됨.
alter table emp4 enable novalidate constraint emp4_sal_ck; --  novalidate 로 해야함

-- 12.1. 뷰(VIEW)
-- VIEW는 테이블 또는 다른 뷰를 기초로 하는 논리적 테이블입니다.

-- 12.1.1. 뷰의 사용 목적
-- 접근제어를 통한 자동 보안이 제공되므로 데이터 베이스 액세스를 제한하기 위해 사용함
-- 복잡한 질의를 쉽게 만들어주기 때문에 사용자의 데이터 관리를 간단하게 해줌.

-- 12.1.2. 단순 뷰와 복합 뷰

SELECT * FROM USER_VIEWS;
-- view 를 조회

-- 12.2. 뷰생성, 데이터 검색,수정,삭제
-- 12.2.1. 뷰 생성 권한
SELECT * FROM USER_ROLE_PRIVS; -- 현재 사용자에게 주어진 롤을 출력
SELECT * FROM USER_SYS_PRIVS; -- 현재 사용자에게 주어진 권한을 출력

-- 12.2.2. 뷰생성
-- 1) 뷰 생성하기
CREATE VIEW emp_view_dept60
as select employee_id, first_name, last_name, job_id, salary
    from employees
    where department_id =60;
    
desc emp_view_dept60;
select * from emp_view_dept60;
drop view emp_view_dept60;

-- 2)뷰 생성 서브쿼리에서 별칭 사용하기
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

-- 12.2.3. 뷰 질의

select * from user_views; -- 사용자 뷰에 대한 정보 출력

-- 12.2.4. 뷰 수정
-- or replace 옵션은 비록 이 이름이 존재하더라도 뷰가 생성되도록 함. 

CREATE OR REPLACE VIEW emp_dept60_salary
as select
    employee_id as empno, first_name|| ' '|| last_name as name,
    job_id as job,  salary 
    from employees
    where department_id =60;

-- 12.2.5. 복합뷰 생성 
-- 두개 이상 테이블로 부터 값을 디스플레이 하는 뷰를 생성함 


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

select * from emp_details_view; -- hr 스키마에 이미 정의된 복합 뷰의 예


--12.2.6. 뷰삭제
-- 뷰는 데이터 베이스에서 기본 테이블을 기반으로 하므로 데이터 손실 없이 뷰를 삭제함. 

DROP VIEW emp_dept60_salary;

-- 12.3. 뷰를 이용한 DML 연산 
--12.3.1

CREATE OR REPLACE VIEW emp_test1234
as select employee_id, last_name, email, hire_date
from employees;

insert into emp_test1234
values (200, 'HEO', 'HEOJK', '02/02/02');   -- cannot insert NULL into  이라 오류....?
-- NOT NULL인 열이 VIEW에 의해서 선택되지 않은...?


-- 13장 

-- 13.1.1. 시퀀스 생성

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