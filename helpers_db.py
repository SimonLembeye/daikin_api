import sqlite3


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def query_db(query, args=(), one=False):
    cur = get_db_connection().cursor()
    cur.execute(query, args)
    r = [
        dict((cur.description[i][0], value) for i, value in enumerate(row))
        for row in cur.fetchall()
    ]
    cur.connection.close()
    return (r[0] if r else None) if one else r


