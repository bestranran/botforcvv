# database.py
import sqlite3

DB_PATH = "bot_minimal.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# 用户余额
def get_balance(user_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            balance REAL DEFAULT 0
        )
    """)
    c.execute("SELECT balance FROM users WHERE id=?", (user_id,))
    row = c.fetchone()
    if not row:
        c.execute("INSERT INTO users (id, balance) VALUES (?, ?)", (user_id, 0))
        conn.commit()
        balance = 0
    else:
        balance = row["balance"]
    conn.close()
    return balance

def update_balance(user_id, amount):
    balance = get_balance(user_id) + amount
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE users SET balance=? WHERE id=?", (balance, user_id))
    conn.commit()
    conn.close()
    return balance

# 商品和库存
def add_product(name, price, code):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            code TEXT,
            is_sold INTEGER DEFAULT 0
        )
    """)
    c.execute("INSERT INTO products (name, price, code) VALUES (?, ?, ?)", (name, price, code))
    conn.commit()
    conn.close()

def get_available_product():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE is_sold=0 LIMIT 1")
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def mark_product_sold(product_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE products SET is_sold=1 WHERE id=?", (product_id,))
    conn.commit()
    conn.close()
