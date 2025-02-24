import streamlit as st
import csv
from datetime import datetime

# Заголовок програми
st.set_page_config(page_title="Інвестиція в кав'ярню", layout="centered")
st.title("Інвестиція в кав'ярню")

# Видатки
st.subheader("Видатки:")

# Перевірка наявності видатків
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# Показуємо суму видатків або повідомлення про їх відсутність
if st.session_state.expenses:
    total_expenses = sum([exp['amount'] for exp in st.session_state.expenses])
    st.write(f"Загальна сума видатків: {total_expenses} злотих")
else:
    st.write("Видатків немає")

# Кнопка для додавання видатків
if st.button("Додати видаток"):
    with st.form("add_expense_form"):
        expense_name = st.text_input("Назва видатку")
        # Введення суми з "zł" на кінці
        expense_amount_str = st.text_input("Сума видатку", placeholder="Введіть суму в злотих")
        if expense_amount_str:
            # Перевірка введеного числа
            try:
                expense_amount = float(expense_amount_str.replace("zł", "").strip())  # Видаляємо "zł" і пробіли
            except ValueError:
                expense_amount = None
                st.error("Будь ласка, введіть правильну суму без символу 'zł' або з символом після суми.")
        else:
            expense_amount = None

        expense_date = st.date_input("Дата видатку", min_value=datetime.today(), value=datetime.today())

        # Додавання видатку за натисканням кнопки
        submit_button = st.form_submit_button("Зберегти видаток")
        
        if submit_button and expense_amount is not None:
            new_expense = {
                'name': expense_name,
                'amount': expense_amount,
                'date': expense_date
            }
            st.session_state.expenses.append(new_expense)
            save_expense(new_expense)  # Зберігаємо видаток у історію
            st.success("Видаток збережено!")
        elif submit_button and expense_amount is None:
            st.error("Сума видатку має бути введена коректно.")

# Податок
st.subheader("Податок:")
tax_percentage = st.slider("Оберіть відсоток податку:", 0, 100, 5)

# Перевірка наявності видатків перед обчисленням податку
if total_expenses > 0:
    tax_amount = total_expenses * (tax_percentage / 100)
    st.write(f"Податок ({tax_percentage}%): {tax_amount} злотих")
else:
    st.write("Податок буде розраховано після додавання видатків.")

# Чистий заробіток
st.subheader("Чистий заробіток:")
income = st.number_input("Введіть щомісячний дохід (злотих):", min_value=0.0, step=100.0)

# Чистий прибуток
net_profit = income - total_expenses - tax_amount
st.write(f"Чистий прибуток: {net_profit} злотих")

# Функція для збереження видатків у CSV файл
def save_expense(expense, update=False):
    file_name = 'expenses_history.csv'
    if update:
        # Оновлення запису в файлі (заміна всіх записів)
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Назва", "Сума", "Дата"])
            for exp in st.session_state.expenses:
                writer.writerow([exp['name'], exp['amount'], exp['date']])
    else:
        # Додавання нового видатку до файлу
        with open(file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # Якщо файл порожній, додаємо заголовки
                writer.writerow(["Назва", "Сума", "Дата"])
            writer.writerow([expense['name'], expense['amount'], expense['date']])
