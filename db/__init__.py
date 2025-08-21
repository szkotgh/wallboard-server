import sqlite3

def create_connection():
    conn = sqlite3.connect("./db/database.db")
    conn.row_factory = sqlite3.Row
    return conn

def close_connection(conn):
    conn.close()
    
def _init():
    conn = create_connection()
    
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS wall (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            create_ip TEXT NOT NULL,
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS wall_item (
            id TEXT PRIMARY KEY,
            wall_id TEXT NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            create_ip TEXT NOT NULL,
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (wall_id) REFERENCES wall (id)
        );
    ''')
    
    close_connection(conn)
    
_init()