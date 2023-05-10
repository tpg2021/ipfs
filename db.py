import sqlite3


def get_connection():
    conn = sqlite3.connect('file_info.db')
    return conn


def insert(*params):
    conn1 = get_connection()
    insert_query = 'INSERT INTO FILE_INFO VALUES(?,?)'
    conn1.execute(insert_query, (params[0], params[1]))
    conn1.commit()
    print(f'Record with cid {params[0]} and file_name {params[1]} inserted successfully')
    conn1.close()


def execute_query(input_query, cid: str):
    conn = get_connection()
    cursor = conn.cursor()
    data = cursor.execute(input_query, (cid,)).fetchone()
    if data:
        return data[0]
    else:
        return str()


def __init__():
    conn1 = get_connection()
    conn1.execute('''
    CREATE TABLE IF NOT EXISTS FILE_INFO 
       (CID TEXT PRIMARY KEY     NOT NULL, 
       FILE_NAME        TEXT    NOT NULL);
    ''')
    print('Table successfully created!! ')
    conn1.commit()
    conn1.close()

