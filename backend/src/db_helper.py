import sqlite3
from sqlite3 import Error


def create_connection(database_filename):
    try:
        conn = sqlite3.connect(database_filename)
        return conn
    except Error as e:
        print(e)


def wipe_instructors_database(conn):
    try:
        c = conn.cursor()
        c.execute('DELETE FROM instructors')
    except Error as e:
        print(e)


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_instructor(conn, instructor):
    sql = ''' INSERT INTO instructors(name,total)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, instructor)
    return cur.lastrowid


def select_all_instructors(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM instructors")

    rows = cur.fetchall()
    return rows


def select_instructor_by_id(conn, id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM instructors WHERE id=?", (id,))

    row = cur.fetchone()

    return row


def update_auth_code(conn, code, realm_id):
    delete_sql = '''DELETE FROM auth_code'''
    sql = '''INSERT INTO auth_code(code,realmId) 
                VALUES(?,?)'''
    try:
        c = conn.cursor()
        c.execute(delete_sql)
        c.execute(sql, (code, realm_id))
    except Error as e:
        print(e)


def get_auth_code(conn):
    sql ="SELECT * FROM auth_code"
    try:
        cur = conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()
    except Error as e:
        print(e)

    return row