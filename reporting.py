
import sqlite3, os, csv

DB_PATH = os.path.join("db", "restaurant.db")

def export_sales_csv(out_path="data/sales_report.csv"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""SELECT b.ts, b.mode, b.table_no, b.payment_method, b.total
                   FROM bills b ORDER BY b.ts DESC""")
    rows = cur.fetchall()
    con.close()
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["timestamp","mode","table_no","payment_method","total"])
        w.writerows(rows)
    return out_path
