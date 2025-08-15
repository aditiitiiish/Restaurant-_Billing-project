
import tkinter as tk
from tkinter import messagebox
from ui.main_ui import RestaurantBillingUI

USERS = {"cashier":"1234", "admin":"admin"}

def start_app():
    root = tk.Tk()
    root.title("Login")
    tk.Label(root, text="Username").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(root, text="Password").grid(row=1, column=0, padx=5, pady=5)
    u = tk.Entry(root); u.grid(row=0, column=1)
    p = tk.Entry(root, show="*"); p.grid(row=1, column=1)
    def go():
        if USERS.get(u.get()) == p.get():
            root.destroy()
            import tkinter as tk
            r = tk.Tk()
            RestaurantBillingUI(r)
            r.mainloop()
        else:
            messagebox.showerror("Error", "Invalid credentials")
    tk.Button(root, text="Login", command=go).grid(row=2, column=0, columnspan=2, pady=8)
    root.mainloop()

if __name__ == "__main__":
    start_app()
