# 🧮 Loan Calculator

A versatile EMI (Equated Monthly Installment) calculator built with Python, offering both a graphical user interface (GUI) and a command-line interface (CLI) for flexibility.

-----

## ✨ Features

### GUI Version:

  - 🧾 **EMI Table Generator** — See a month-by-month breakdown of payments
  - 📊 **Graphical Summary** — Visualize principal vs interest using charts
  - 🌓 **Dark Mode Toggle** — Light and dark themes available
  - 📁 **Export Options**:
      - Save EMI schedule to **Excel (.xlsx)**
      - Export printable **PDF report**
  - 🇮🇳 **INR Currency Formatting** — ₹1,00,000.00 format
  - ✅ **Summary Row** — Displays total principal, interest, and total payment

### CLI Version:

  - 🧾 **EMI Table Generator** — Provides a text-based, month-by-month breakdown of payments.
  - ✅ **Summary Output** — Displays total principal, interest, and total payment at the end of the schedule.
  - 🇮🇳 **INR Currency Formatting** — ₹1,00,000.00 format for clear readability in the terminal.
  - ⚙️ **Minimal Dependencies** — Runs with only standard Python libraries.

-----

## 📦 Requirements

  - **Python 3.10+**

### For GUI Version:

```bash
pip install matplotlib pandas openpyxl fpdf2
```

### For CLI Version:

No external dependencies are required.

-----

## 🚀 How to Use

### GUI Version:

Run the app:

```bash
python loan_calc.py
```

Fill in:

  - **Loan Amount** (e.g., ₹5,00,000)
  - **Annual Interest Rate** (e.g., 9.5%)
  - **Tenure in months** (e.g., 60)

Click **Calculate** to:

  - Generate EMI table
  - Display totals and chart

Use buttons to:

  - 💾 Export to Excel
  - 🖨️ Save as PDF
  - 🌓 Toggle dark mode

-----

### CLI Version:

Run the script:

```bash
python loan_calc_cli.py
```

The program will then prompt you to enter:

  - **Loan Amount**
  - **Term (months)**
  - **Annual Interest Rate (%)**

After inputs are provided, it will display the loan amortization schedule directly in your terminal.

-----

## 📷 Screenshots

*Light Mode* | *Dark Mode*
\---|---
 | 

*(Replace the image URLs above with actual URLs from your repo for the GUI version)*

-----

## 📊 Sample Output

| Month | EMI         | Principal   | Interest   | Balance     |
|-------|-------------|-------------|------------|-------------|
| 1     | ₹10,749.32  | ₹9,249.32   | ₹1,500.00  | ₹4,90,750.68|
| ...   | ...         | ...         | ...        | ...         |
| **Total** | ₹6,44,959.00 | ₹5,00,000.00 | ₹1,44,959.00 | ₹0.00 |

-----

## 📦 Export Formats

  - **Excel (.xlsx):** Includes detailed table + summary (GUI only)
  - **PDF:** Printable EMI schedule with total summary (GUI only)

-----

## 💻 Platform

  - 🪟 Windows (recommended for GUI)
  - 🐍 Works on any OS with Python 3.10+ (GUI requires GUI support, CLI is universal)

-----

## 🤝 Contribution

Pull requests are welcome\!
To contribute:

1.  Fork the repo
2.  Create a branch: `git checkout -b feature-name`
3.  Commit and push: `git commit -m "Add feature"` → `git push`
4.  Open a Pull Request

-----

## 🧑‍💻 Author

Akash P
🔗 [GitHub Profile](https://github.com/AkzXrated)
