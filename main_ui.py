
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import os, winsound

from utils.calculator import calculate_bill
from utils.db_utils import save_full_bill, create_tables
from utils.pdf_exporter import export_pdf

class RestaurantBillingUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Billing System")
        self.root.geometry("800x650")
        self.root.configure(bg="#fafafa")
        create_tables()

        # Menu (could also be loaded from CSV)
        self.menu = {"Burger":100, "Pizza":250, "Pasta":180, "Fries":80, "Coke":40}

        # Top title
        tk.Label(root, text="Select Menu Items", font=("Arial", 20), bg="#fafafa").pack(pady=10)

        # Table & mode & payment
        topbar = tk.Frame(root, bg="#fafafa")
        topbar.pack(pady=4)
        self.table_var = tk.StringVar(value="Table 1")
        self.mode_var = tk.StringVar(value="Dine-In")
        self.pay_var = tk.StringVar(value="Cash")
        ttk.OptionMenu(topbar, self.table_var, "Table 1", *[f"Table {i}" for i in range(1,11)]).grid(row=0, column=0, padx=5)
        ttk.OptionMenu(topbar, self.mode_var, "Dine-In", "Dine-In", "Takeaway").grid(row=0, column=1, padx=5)
        ttk.OptionMenu(topbar, self.pay_var, "Cash", "Cash", "Card", "UPI").grid(row=0, column=2, padx=5)

        # Items
        self.quantity_vars = {}
        for item, price in self.menu.items():
            frame = tk.Frame(root, bg="#fafafa")
            frame.pack(pady=2)
            tk.Label(frame, text=f"{item} (₹{price})", width=20, anchor="w", bg="#fafafa").pack(side=tk.LEFT, padx=3)
            var = tk.IntVar(value=0)
            self.quantity_vars[item] = var
            tk.Entry(frame, textvariable=var, width=5).pack(side=tk.LEFT)

        # Buttons
        tk.Button(root, text="Generate Bill", command=self.calculate_total, bg="green", fg="white").pack(pady=8)
        tk.Button(root, text="Clear", command=self.clear_all, bg="red", fg="white").pack(pady=4)

        # Receipt box
        self.bill_text = tk.Text(root, height=16, width=90)
        self.bill_text.pack(padx=10, pady=10)

        # Clock
        self.clock_label = tk.Label(root, font=("Arial", 11), fg="green", bg="#fafafa")
        self.clock_label.pack(pady=5)
        self.update_clock()

    def update_clock(self):
        self.clock_label.config(text=f"Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.root.after(1000, self.update_clock)

    def calculate_total(self):
        result = calculate_bill(self.quantity_vars, self.menu,
                                payment_method=self.pay_var.get(),
                                mode=self.mode_var.get(),
                                table=self.table_var.get(),
                                discount_percent=0)
        # Show in textbox
        self.bill_text.delete(1.0, tk.END)
        self.bill_text.insert(tk.END, result["receipt"])

        # Save to DB
        bill_id = save_full_bill(result)

        # Export PDF (or txt if reportlab not installed)
        pdf_path = export_pdf(result["receipt"])

        # Celebration sound (non-blocking)
        try:
            winsound.PlaySound(os.path.join("assets", "celebration.wav"),
                               winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception:
            pass

        messagebox.showinfo("Success", f"Bill #{bill_id} saved!\nExported: {os.path.basename(pdf_path)}")

    def clear_all(self):
        for var in self.quantity_vars.values():
            var.set(0)
        self.bill_text.delete(1.0, tk.END)
