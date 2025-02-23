import tkinter as tk
from tkinter import messagebox

def calculate():
    try:
        # Зчитуємо значення з полів вводу
        credit_amount = float(entry_credit.get())
        loan_term_months = int(entry_term.get())
        monthly_payment_loan = float(entry_monthly_payment.get())
        monthly_insurance = float(entry_insurance.get())
        royalty_percent = float(entry_royalty.get()) / 100  # Перетворюємо процент у десяткову дробу
        monthly_income = float(entry_income.get())
        
        # Загальні витрати по кредиту (кредит + страховка)
        monthly_total_payment = monthly_payment_loan + monthly_insurance
        total_payment_over_loan_term = monthly_total_payment * loan_term_months  # Загальна сума, яку сплатимо за кредит за весь термін

        # Переплата по кредиту
        overpayment = total_payment_over_loan_term - credit_amount

        # Роялті франчайзеру
        royalty_payment = monthly_income * royalty_percent  # Щомісячне роялті

        # Чистий прибуток
        net_profit = monthly_income - monthly_total_payment - royalty_payment  # Чистий прибуток після виплат

        # Оцінка окупності
        time_to_coverage_overpayment = overpayment / net_profit if net_profit > 0 else float('inf')  # Скільки місяців потрібно для покриття переплати

        # Виведення результатів
        result_text = (
            f"Загальна переплата по кредиту: {overpayment:.2f} злотих\n"
            f"Щомісячне роялті франчайзеру: {royalty_payment:.2f} злотих\n"
            f"Чистий прибуток на місяць: {net_profit:.2f} злотих\n"
            f"Час для покриття переплати (місяців): {time_to_coverage_overpayment:.2f} місяців"
        )
        label_result.config(text=result_text)
        
    except ValueError:
        messagebox.showerror("Помилка введення", "Будь ласка, введіть коректні числові значення.")

# Створення основного вікна
root = tk.Tk()
root.title("Аналіз інвестиції та кредиту")

# Створення елементів інтерфейсу
label_credit = tk.Label(root, text="Сума кредиту (злотих):")
label_credit.grid(row=0, column=0, sticky="w")
entry_credit = tk.Entry(root)
entry_credit.grid(row=0, column=1)

label_term = tk.Label(root, text="Термін кредиту (місяців):")
label_term.grid(row=1, column=0, sticky="w")
entry_term = tk.Entry(root)
entry_term.grid(row=1, column=1)

label_monthly_payment = tk.Label(root, text="Щомісячний платіж по кредиту (злотих):")
label_monthly_payment.grid(row=2, column=0, sticky="w")
entry_monthly_payment = tk.Entry(root)
entry_monthly_payment.grid(row=2, column=1)

label_insurance = tk.Label(root, text="Щомісячна страховка (злотих):")
label_insurance.grid(row=3, column=0, sticky="w")
entry_insurance = tk.Entry(root)
entry_insurance.grid(row=3, column=1)

label_royalty = tk.Label(root, text="Процент роялті франчайзеру (%):")
label_royalty.grid(row=4, column=0, sticky="w")
entry_royalty = tk.Entry(root)
entry_royalty.grid(row=4, column=1)

label_income = tk.Label(root, text="Щомісячний дохід від інвестиції (злотих):")
label_income.grid(row=5, column=0, sticky="w")
entry_income = tk.Entry(root)
entry_income.grid(row=5, column=1)

# Кнопка для запуску розрахунку
button_calculate = tk.Button(root, text="Розрахувати", command=calculate)
button_calculate.grid(row=6, column=0, columnspan=2)

# Місце для результатів
label_result = tk.Label(root, text="Результати будуть тут", justify="left")
label_result.grid(row=7, column=0, columnspan=2)

# Запуск програми
root.mainloop()
