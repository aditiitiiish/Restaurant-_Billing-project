
import streamlit as st
import sqlite3, pandas as pd, os

DB_PATH = os.path.join("db", "restaurant.db")

st.title("Restaurant Billing Dashboard")

con = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM bills ORDER BY ts DESC", con)
con.close()

st.subheader("Recent Bills")
st.dataframe(df)

st.subheader("Totals by Payment Method")
if not df.empty:
    st.bar_chart(df.groupby("payment_method")["total"].sum())
else:
    st.info("No data yet. Generate some bills from the Tkinter app.")
