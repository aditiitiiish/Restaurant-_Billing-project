
import sqlite3, os
from datetime import datetime

DB_PATH = os.path.join("db", "restaurant.db")

def create_tables():
    os.makedirs("db", exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT,
        mode TEXT,
        table_no TEXT,
        payment_method TEXT,
        subtotal REAL,
        gst REAL,
        discount REAL,
        total REAL
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS bill_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bill_id INTEGER,
        item TEXT,
        qty INTEGER,
        price REAL,
        line_total REAL,
        FOREIGN KEY(bill_id) REFERENCES bills(id)
    )""")
    con.commit()
    con.close()

def save_full_bill(result):
    create_tables()
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""INSERT INTO bills(ts, mode, table_no, payment_method, subtotal, gst, discount, total)
                   VALUES(?,?,?,?,?,?,?,?)""",
                (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), result["mode"], result["table"],
                 result["payment_method"], result["subtotal"], result["gst"], result["discount"], result["grand_total"]))
    bill_id = cur.lastrowid
    for o in result["orders"]:
        cur.execute("""INSERT INTO bill_items(bill_id, item, qty, price, line_total) VALUES(?,?,?,?,?)""",
                    (bill_id, o["item"], o["quantity"], o["price"], o["line_total"]))
    con.commit()
    con.close()
    return bill_id
