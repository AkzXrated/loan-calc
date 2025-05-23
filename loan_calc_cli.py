def format_inr(amount):
    """
    Formats a number with commas in Indian style (e.g., 1,23,456.78).
    """
    s = f"{amount:,.2f}"
    parts = s.split(".")
    integer_part = parts[0].replace(",", "")

    if len(integer_part) > 3:
        last_three = integer_part[-3:]
        rest = integer_part[:-3]
        rest_with_commas = ""
        while len(rest) > 2:
            rest_with_commas = "," + rest[-2:] + rest_with_commas
            rest = rest[:-2]
        integer_part = rest + rest_with_commas + "," + last_three
    return integer_part + "." + parts[1]

def calculate_loan():
    """
    Calculates loan amortization and prints the schedule.
    """
    while True:
        try:
            loan_amount_str = input("Enter Loan Amount: ")
            loan_amount = float(loan_amount_str.replace(',', ''))
            if loan_amount <= 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid loan amount. Please enter a positive number.")

    while True:
        try:
            term_months = int(input("Enter Term (months): "))
            if term_months <= 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid term. Please enter a positive integer.")

    while True:
        try:
            annual_rate = float(input("Enter Annual Interest Rate (%): "))
            if annual_rate < 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid interest rate. Please enter a non-negative number.")

    principal_per_installment = loan_amount / term_months
    balance = loan_amount
    monthly_rate = annual_rate / 100 / 12

    print("\n--- Loan Amortization Schedule ---")
    print(f"{'Inst.No':<10}{'Principal':>15}{'Interest':>15}{'Total':>15}{'Balance':>15}")
    print("-" * 70)

    total_principal_paid = 0
    total_interest_paid = 0
    total_payment_made = 0

    for i in range(1, term_months + 1):
        interest = balance * monthly_rate
        total = principal_per_installment + interest
        balance -= principal_per_installment
        if balance < 0:
            balance = 0.0

        principal_rounded = round(principal_per_installment, 2)
        interest_rounded = round(interest, 2)
        total_rounded = round(total, 2)
        balance_rounded = round(balance, 2)

        print(f"{i:<10}{format_inr(principal_rounded):>15}{format_inr(interest_rounded):>15}{format_inr(total_rounded):>15}{format_inr(balance_rounded):>15}")

        total_principal_paid += principal_rounded
        total_interest_paid += interest_rounded
        total_payment_made += total_rounded

    print("-" * 70)
    print(f"{'Total':<10}{format_inr(total_principal_paid):>15}{format_inr(total_interest_paid):>15}{format_inr(total_payment_made):>15}{'':>15}")
    print("---------------------------------\n")

if __name__ == "__main__":
    calculate_loan()
