import sqlite3
import os


DB_NAME = "klinik_v2.db"


def get_connection():
    """SQLite bağlantısı oluşturur."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn):
    """Tüm tabloları oluşturur."""
    c = conn.cursor()

    # Ürün tablosu
    c.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        buy_price REAL NOT NULL,
        sell_price REAL NOT NULL,
        stock INTEGER NOT NULL DEFAULT 0,
        category TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Satış tablosu
    c.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        qty INTEGER NOT NULL,
        total REAL NOT NULL,
        profit REAL NOT NULL,
        customer_id INTEGER,
        payment_type TEXT,
        date TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(product_id) REFERENCES products(id)
    )
    """)

    # Müşteri – Veresiye tablosu
    c.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS customer_debts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        description TEXT,
        amount REAL NOT NULL,
        date TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(customer_id) REFERENCES customers(id)
    )
    """)

    # Tedavi tablosu
    c.execute("""
    CREATE TABLE IF NOT EXISTS treatments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        material_cost REAL NOT NULL,
        price REAL NOT NULL,
        profit REAL NOT NULL,
        date TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Gider tablosu
    c.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        amount REAL NOT NULL,
        date TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()


def add_product(conn, name, buy_price, sell_price, stock, category):
    c = conn.cursor()
    c.execute("""
    INSERT INTO products (name, buy_price, sell_price, stock, category)
    VALUES (?, ?, ?, ?, ?)
    """, (name, buy_price, sell_price, stock, category))
    conn.commit()


def update_stock(conn, product_id, qty_change):
    """Stok arttırır veya azaltır."""
    c = conn.cursor()
    c.execute("UPDATE products SET stock = stock + ? WHERE id = ?", (qty_change, product_id))
    conn.commit()


def record_sale(conn, product_id, qty, total, profit, customer_id, payment_type):
    c = conn.cursor()
    c.execute("""
    INSERT INTO sales (product_id, qty, total, profit, customer_id, payment_type)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (product_id, qty, total, profit, customer_id, payment
