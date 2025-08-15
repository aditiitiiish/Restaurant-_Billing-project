
# Restaurant Billing System (Tkinter + Streamlit)

Features:
- Menu entry with quantities
- Dine-in/Takeaway mode, table selector, payment method (Cash/Card/UPI)
- GST 5% + optional discounts (wired in utils/calculator.py)
- Itemized bill shown in UI
- Save to SQLite (`db/restaurant.db`)
- Export PDF (uses `reportlab`; falls back to .txt if not installed)
- Celebration sound on save (`assets/celebration.wav`)
- Streamlit dashboard for reports (`streamlit run streamlit_app.py`)

## Run (Tkinter)
```bash
python app.py
```

## Run (Login -> Tkinter)
```bash
python login.py
# user: cashier  pass: 1234
```

## Run (Streamlit Dashboard)
```bash
pip install streamlit pandas
streamlit run streamlit_app.py
```

## Install Optional Dependency for PDF
```bash
pip install reportlab
```
