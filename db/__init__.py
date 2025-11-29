import sqlite3

def create_connection():
    conn = sqlite3.connect("./db/database.db")
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def close_connection(conn):
    conn.close()
    
def _init():
    conn = create_connection()
    with open('db/schema.sql', 'r') as f:
        conn.executescript(f.read())
    close_connection(conn)
    
_init()