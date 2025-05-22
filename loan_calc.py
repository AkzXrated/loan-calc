import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd

class LoanCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Loan Calculator")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        self.dark_mode = False

        # Main frame
        self.frame = ttk.Frame(root, padding=10)
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Configure root and frame for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        for col in range(5):
            self.frame.columnconfigure(col, weight=1)
        self.frame.rowconfigure(5, weight=1)  # Treeview row
        self.frame.rowconfigure(6, weight=1)  # Graph row

        # Inputs
        ttk.Label(self.frame, text="Loan Amount:").grid(row=0, column=0, sticky="w")
        self.loan_amount_var = tk.StringVar()
        self.loan_amount_entry = ttk.Entry(self.frame, textvariable=self.loan_amount_var)
        self.loan_amount_entry.grid(row=0, column=1, sticky="ew")

        ttk.Label(self.frame, text="Term (months):").grid(row=1, column=0, sticky="w")
        self.term_var = tk.StringVar()
        self.term_entry = ttk.Entry(self.frame, textvariable=self.term_var)
        self.term_entry.grid(row=1, column=1, sticky="ew")

        ttk.Label(self.frame, text="Annual Interest Rate (%):").grid(row=2, column=0, sticky="w")
        self.interest_var = tk.StringVar()
        self.interest_entry = ttk.Entry(self.frame, textvariable=self.interest_var)
        self.interest_entry.grid(row=2, column=1, sticky="ew")

        # Buttons
        self.calc_btn = ttk.Button(self.frame, text="Calculate", command=self.calculate)
        self.calc_btn.grid(row=3, column=0, columnspan=2, pady=10)

        self.export_csv_btn = ttk.Button(self.frame, text="Export CSV", command=self.export_csv)
        self.export_csv_btn.grid(row=3, column=2, pady=10)

        self.export_excel_btn = ttk.Button(self.frame, text="Export Excel", command=self.export_excel)
        self.export_excel_btn.grid(row=3, column=3, pady=10)

        self.darkmode_btn = ttk.Button(self.frame, text="Toggle Dark Mode", command=self.toggle_dark_mode)
        self.darkmode_btn.grid(row=3, column=4, pady=10)

        # Table (Treeview)
        columns = ("Inst.No", "Principal", "Interest", "Total", "Balance")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="e")
        self.tree.grid(row=5, column=0, columnspan=5, pady=10, sticky="nsew")

        # Matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(7,3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=6, column=0, columnspan=5, sticky="nsew")

        # Data container for export and chart
        self.data = []

    def calculate(self):
        # Clear previous data
        self.tree.delete(*self.tree.get_children())
        self.ax.clear()
        self.data.clear()

        # Validate inputs
        try:
            loan_amount = float(self.loan_amount_var.get().replace(',', ''))
            term_months = int(self.term_var.get())
            annual_rate = float(self.interest_var.get())
            if loan_amount <= 0 or term_months <= 0 or annual_rate < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid positive numbers.")
            return

        principal_per_installment = loan_amount / term_months
        balance = loan_amount
        monthly_rate = annual_rate / 100 / 12

        total_principal = 0
        total_interest = 0
        total_payment = 0

        for i in range(1, term_months + 1):
            interest = balance * monthly_rate
            total = principal_per_installment + interest
            balance -= principal_per_installment
            if balance < 0:
                balance = 0.0

            # Round values and format INR style (Indian numbering)
            p = round(principal_per_installment, 2)
            it = round(interest, 2)
            tot = round(total, 2)
            bal = round(balance, 2)

            # Store for export/chart
            self.data.append({
                "Inst.No": i,
                "Principal": p,
                "Interest": it,
                "Total": tot,
                "Balance": bal,
            })

            self.tree.insert("", "end", values=(
                i,
                self.format_inr(p),
                self.format_inr(it),
                self.format_inr(tot),
                self.format_inr(bal),
            ))

            total_principal += p
            total_interest += it
            total_payment += tot

        # Insert totals row
        self.tree.insert("", "end", values=(
            "Total",
            self.format_inr(total_principal),
            self.format_inr(total_interest),
            self.format_inr(total_payment),
            ""
        ))

        # Plot graph: Principal and Interest over installments
        installments = [row["Inst.No"] for row in self.data]
        principals = [row["Principal"] for row in self.data]
        interests = [row["Interest"] for row in self.data]

        self.ax.plot(installments, principals, label="Principal")
        self.ax.plot(installments, interests, label="Interest")
        self.ax.set_xlabel("Installment No")
        self.ax.set_ylabel("Amount (₹)")
        self.ax.set_title("Principal and Interest over time")
        self.ax.legend()
        self.ax.grid(True)

        self.canvas.draw()

    def format_inr(self, amount):
        # Format number with commas in Indian style e.g. 1,23,456.78
        s = f"{amount:,.2f}"
        # Fix for Indian comma style:
        # swap first comma to last occurrence of comma in first 3 digits
        parts = s.split(".")
        integer_part = parts[0].replace(",", "")
        if len(integer_part) > 3:
            # Last 3 digits
            last3 = integer_part[-3:]
            rest = integer_part[:-3]
            # Insert commas every 2 digits in 'rest'
            rest_with_commas = ""
            while len(rest) > 2:
                rest_with_commas = "," + rest[-2:] + rest_with_commas
                rest = rest[:-2]
            rest_with_commas = rest + rest_with_commas
            integer_part = rest_with_commas + "," + last3
        return integer_part + "." + parts[1]

    def export_csv(self):
        if not self.data:
            messagebox.showwarning("No data", "Please calculate first before exporting.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not path:
            return
        df = pd.DataFrame(self.data)
        df.to_csv(path, index=False)
        messagebox.showinfo("Exported", f"Data exported to {path}")

    def export_excel(self):
        if not self.data:
            messagebox.showwarning("No data", "Please calculate first before exporting.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if not path:
            return
        df = pd.DataFrame(self.data)
        df.to_excel(path, index=False)
        messagebox.showinfo("Exported", f"Data exported to {path}")

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        style = ttk.Style()

        if self.dark_mode:
            self.root.configure(bg="#2E2E2E")
            style.theme_use('clam')
            style.configure('.', background='#2E2E2E', foreground='white')
            style.configure('Treeview', background='#424242', foreground='white', fieldbackground='#424242')
            style.map('Treeview', background=[('selected', '#6A9FB5')], foreground=[('selected', 'white')])
        else:
            self.root.configure(bg="SystemButtonFace")
            style.theme_use('default')
            style.configure('.', background='SystemButtonFace', foreground='black')
            style.configure('Treeview', background='white', foreground='black', fieldbackground='white')
            style.map('Treeview', background=[('selected', '#347083')], foreground=[('selected', 'white')])

        # Refresh widgets background if needed
        for widget in self.frame.winfo_children():
            try:
                widget.configure(background=self.root['bg'])
            except:
                pass

if __name__ == "__main__":
    root = tk.Tk()
    app = LoanCalculatorApp(root)
    root.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd

class LoanCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Loan Calculator")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        self.dark_mode = False

        # Main frame
        self.frame = ttk.Frame(root, padding=10)
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Configure root and frame for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        for col in range(5):
            self.frame.columnconfigure(col, weight=1)
        self.frame.rowconfigure(5, weight=1)  # Treeview row
        self.frame.rowconfigure(6, weight=1)  # Graph row

        # Inputs
        ttk.Label(self.frame, text="Loan Amount:").grid(row=0, column=0, sticky="w")
        self.loan_amount_var = tk.StringVar()
        self.loan_amount_entry = ttk.Entry(self.frame, textvariable=self.loan_amount_var)
        self.loan_amount_entry.grid(row=0, column=1, sticky="ew")

        ttk.Label(self.frame, text="Term (months):").grid(row=1, column=0, sticky="w")
        self.term_var = tk.StringVar()
        self.term_entry = ttk.Entry(self.frame, textvariable=self.term_var)
        self.term_entry.grid(row=1, column=1, sticky="ew")

        ttk.Label(self.frame, text="Annual Interest Rate (%):").grid(row=2, column=0, sticky="w")
        self.interest_var = tk.StringVar()
        self.interest_entry = ttk.Entry(self.frame, textvariable=self.interest_var)
        self.interest_entry.grid(row=2, column=1, sticky="ew")

        # Buttons
        self.calc_btn = ttk.Button(self.frame, text="Calculate", command=self.calculate)
        self.calc_btn.grid(row=3, column=0, columnspan=2, pady=10)

        self.export_csv_btn = ttk.Button(self.frame, text="Export CSV", command=self.export_csv)
        self.export_csv_btn.grid(row=3, column=2, pady=10)

        self.export_excel_btn = ttk.Button(self.frame, text="Export Excel", command=self.export_excel)
        self.export_excel_btn.grid(row=3, column=3, pady=10)

        self.darkmode_btn = ttk.Button(self.frame, text="Toggle Dark Mode", command=self.toggle_dark_mode)
        self.darkmode_btn.grid(row=3, column=4, pady=10)

        # Table (Treeview)
        columns = ("Inst.No", "Principal", "Interest", "Total", "Balance")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="e")
        self.tree.grid(row=5, column=0, columnspan=5, pady=10, sticky="nsew")

        # Matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(7,3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=6, column=0, columnspan=5, sticky="nsew")

        # Data container for export and chart
        self.data = []

    def calculate(self):
        # Clear previous data
        self.tree.delete(*self.tree.get_children())
        self.ax.clear()
        self.data.clear()

        # Validate inputs
        try:
            loan_amount = float(self.loan_amount_var.get().replace(',', ''))
            term_months = int(self.term_var.get())
            annual_rate = float(self.interest_var.get())
            if loan_amount <= 0 or term_months <= 0 or annual_rate < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid positive numbers.")
            return

        principal_per_installment = loan_amount / term_months
        balance = loan_amount
        monthly_rate = annual_rate / 100 / 12

        total_principal = 0
        total_interest = 0
        total_payment = 0

        for i in range(1, term_months + 1):
            interest = balance * monthly_rate
            total = principal_per_installment + interest
            balance -= principal_per_installment
            if balance < 0:
                balance = 0.0

            # Round values and format INR style (Indian numbering)
            p = round(principal_per_installment, 2)
            it = round(interest, 2)
            tot = round(total, 2)
            bal = round(balance, 2)

            # Store for export/chart
            self.data.append({
                "Inst.No": i,
                "Principal": p,
                "Interest": it,
                "Total": tot,
                "Balance": bal,
            })

            self.tree.insert("", "end", values=(
                i,
                self.format_inr(p),
                self.format_inr(it),
                self.format_inr(tot),
                self.format_inr(bal),
            ))

            total_principal += p
            total_interest += it
            total_payment += tot

        # Insert totals row
        self.tree.insert("", "end", values=(
            "Total",
            self.format_inr(total_principal),
            self.format_inr(total_interest),
            self.format_inr(total_payment),
            ""
        ))

        # Plot graph: Principal and Interest over installments
        installments = [row["Inst.No"] for row in self.data]
        principals = [row["Principal"] for row in self.data]
        interests = [row["Interest"] for row in self.data]

        self.ax.plot(installments, principals, label="Principal")
        self.ax.plot(installments, interests, label="Interest")
        self.ax.set_xlabel("Installment No")
        self.ax.set_ylabel("Amount (₹)")
        self.ax.set_title("Principal and Interest over time")
        self.ax.legend()
        self.ax.grid(True)

        self.canvas.draw()

    def format_inr(self, amount):
        # Format number with commas in Indian style e.g. 1,23,456.78
        s = f"{amount:,.2f}"
        # Fix for Indian comma style:
        # swap first comma to last occurrence of comma in first 3 digits
        parts = s.split(".")
        integer_part = parts[0].replace(",", "")
        if len(integer_part) > 3:
            # Last 3 digits
            last3 = integer_part[-3:]
            rest = integer_part[:-3]
            # Insert commas every 2 digits in 'rest'
            rest_with_commas = ""
            while len(rest) > 2:
                rest_with_commas = "," + rest[-2:] + rest_with_commas
                rest = rest[:-2]
            rest_with_commas = rest + rest_with_commas
            integer_part = rest_with_commas + "," + last3
        return integer_part + "." + parts[1]

    def export_csv(self):
        if not self.data:
            messagebox.showwarning("No data", "Please calculate first before exporting.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not path:
            return
        df = pd.DataFrame(self.data)
        df.to_csv(path, index=False)
        messagebox.showinfo("Exported", f"Data exported to {path}")

    def export_excel(self):
        if not self.data:
            messagebox.showwarning("No data", "Please calculate first before exporting.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if not path:
            return
        df = pd.DataFrame(self.data)
        df.to_excel(path, index=False)
        messagebox.showinfo("Exported", f"Data exported to {path}")

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        style = ttk.Style()

        if self.dark_mode:
            self.root.configure(bg="#2E2E2E")
            style.theme_use('clam')
            style.configure('.', background='#2E2E2E', foreground='white')
            style.configure('Treeview', background='#424242', foreground='white', fieldbackground='#424242')
            style.map('Treeview', background=[('selected', '#6A9FB5')], foreground=[('selected', 'white')])
        else:
            self.root.configure(bg="SystemButtonFace")
            style.theme_use('default')
            style.configure('.', background='SystemButtonFace', foreground='black')
            style.configure('Treeview', background='white', foreground='black', fieldbackground='white')
            style.map('Treeview', background=[('selected', '#347083')], foreground=[('selected', 'white')])

        # Refresh widgets background if needed
        for widget in self.frame.winfo_children():
            try:
                widget.configure(background=self.root['bg'])
            except:
                pass

if __name__ == "__main__":
    root = tk.Tk()
    app = LoanCalculatorApp(root)
    root.mainloop()
