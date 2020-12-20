import cx_Oracle as oci

#conn= oci.connect('hr/hr@localhost:1522/xe')  아래 두개랑 같은 코드
oracle_dsn = oci.makedsn(host="localhost", port=1522,sid ="xe")
conn = oci.connect(dsn = oracle_dsn, user="hr", password="hr")

def get_emp(employee_id):
    sql = "select first_name from employees where employee_id = :empno"
    cursor = conn.cursor()
    cursor.execute(sql, {"empno":employee_id})
    name = cursor.fetchone()
    return name[0]

1