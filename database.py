import sqlite3
from config import DATABASE_PATH

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS barcodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            barcode TEXT UNIQUE,
            name TEXT,
            price REAL,
            details TEXT,
            amount REAL
        )
    """)
    conn.commit()
    conn.close()

def add_barcode_info(barcode, name, price, details, amount):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO barcodes (barcode, name, price, details, amount) 
        VALUES (?, ?, ?, ?, ?)
    """, (barcode, name, price, details, amount))
    conn.commit()
    conn.close()

def get_barcode_info(barcode):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, price, details, amount FROM barcodes WHERE barcode=?", (barcode,))
    result = cursor.fetchone()
    conn.close()
    return result
