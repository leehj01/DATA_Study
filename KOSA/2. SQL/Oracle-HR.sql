
drop table books;

create table books(
    bk_index number(4),
    category number(2),
    bk_name varchar2(50),
    bk_writer varchar2(50),
    bk_date date,
    bk_price number(8),
    bk_grade number(2),
    bk_new_price number(8));
    
create sequence books_seq
    increment by 1
    maxvalue 100;