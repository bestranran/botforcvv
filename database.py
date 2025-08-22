import sqlite3
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY, username TEXT, balance REAL DEFAULT 0
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY, name TEXT, price REAL, country TEXT, category TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS stock (
        id INTEGER PRIMARY KEY, product_id INTEGER, code TEXT, is_sold INTEGER DEFAULT 0
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY, user_id INTEGER, product_id INTEGER, code TEXT, created_at TEXT
    )''')
    conn.commit()
    conn.close()

def get_conn():
    return sqlite3.connect(DB_PATH)
