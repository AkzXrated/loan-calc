
# 🧮 Loan Calculator

A modern, easy-to-use EMI (Equated Monthly Installment) calculator built with Python and Tkinter.  
Supports exporting to Excel/PDF, dark mode, summary statistics, and visual charts.

---

## ✨ Features

- 🧾 **EMI Table Generator** — See a month-by-month breakdown of payments  
- 📊 **Graphical Summary** — Visualize principal vs interest using charts  
- 🌓 **Dark Mode Toggle** — Light and dark themes available  
- 📁 **Export Options**:  
  - Save EMI schedule to **Excel (.xlsx)**  
  - Export printable **PDF report**  
- 🇮🇳 **INR Currency Formatting** — ₹1,00,000.00 format  
- ✅ **Summary Row** — Displays total principal, interest, and total payment  

---

## 📦 Requirements

- Python 3.10+  
- Dependencies:

```bash
pip install matplotlib pandas openpyxl fpdf2
```

---

## 🚀 How to Use

Run the app:

```bash
python loan_calc.py
```

Fill in:

- Loan Amount (e.g., ₹5,00,000)  
- Annual Interest Rate (e.g., 9.5%)  
- Tenure in months (e.g., 60)  

Click **Calculate** to:

- Generate EMI table  
- Display totals and chart  

Use buttons to:

- 💾 Export to Excel  
- 🖨️ Save as PDF  
- 🌓 Toggle dark mode  

---

## 📷 Screenshots

*Light Mode* | *Dark Mode*  
---|---  
![Light Mode](https://your-image-url-light.png) | ![Dark Mode](https://your-image-url-dark.png)  

*(Replace the image URLs above with actual URLs from your repo)*

---

## 📊 Sample Output

| Month | EMI        | Principal   | Interest   | Balance     |
|-------|------------|-------------|------------|-------------|
| 1     | ₹10,749.32 | ₹9,249.32   | ₹1,500.00  | ₹4,90,750.68|
| ...   | ...        | ...         | ...        | ...         |
| **Total** | ₹6,44,959.00 | ₹5,00,000.00 | ₹1,44,959.00 | ₹0.00 |

---

## 📦 Export Formats

- **Excel (.xlsx):** Includes detailed table + summary  
- **PDF:** Printable EMI schedule with total summary  

---

## 💻 Platform

- 🪟 Windows (recommended)  
- 🐍 Works on any OS with Python 3.10+ and GUI support  

---

## 🤝 Contribution

Pull requests are welcome!  
To contribute:

1. Fork the repo  
2. Create a branch: `git checkout -b feature-name`  
3. Commit and push: `git commit -m "Add feature"` → `git push`  
4. Open a Pull Request  

---

## 🧑‍💻 Author

Akash P  
🔗 [GitHub Profile](https://github.com/AkzXrated)
