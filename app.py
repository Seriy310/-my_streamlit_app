import streamlit as st
import csv
import os
from datetime import datetime

# Заголовок програми
st.set_page_config(page_title="Інвестиція в кав'ярню", layout="centered")
st.title("Інвестиція в кав'ярню")

# Функція для збереження видатків у CSV файл
def save_expense(expense):
    file_name = 'expenses_history.csv'
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Якщо файл порожній, додаємо заголовки
            writer.writerow(["Назва", "Сума", "Дата"])
        writer.writerow([expense['name'], expense['amount'], expense['date']])

# Завантаження витрат із файлу
if 'expenses' not in st.session_state:
    st.session_state.expenses = []
    if os.path.exists("expenses_history.csv"):
        with open("expenses_history.csv", newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                st.session_state.expenses.append({
                    'name': row['Назва'],
                    'amount': float(row['Сума']),
                    'date': row['Дата']
                })

# Видатки
st.subheader("Видатки:")
total_expenses = sum(exp['amount'] for exp in st.session_state.expenses)
st.write(f"Загальна сума видатків: {total_expenses:.2f} zł" if total_expenses > 0 else "Видатків немає")

# Кнопка переходу до історії видатків
if st.button("📜 Переглянути історію видатків"):
    st.switch_page("pages/history.py")

# Форма для додавання видатків
with st.expander("➕ Додати новий видаток"):
    with st.form("add_expense_form"):
        expense_name = st.text_input("Назва видатку")
        expense_amount_str = st.text_input("Сума видатку", placeholder="Введіть суму в злотих (наприклад, 50)")

        try:
            expense_amount = float(expense_amount_str.replace("zł", "").strip()) if expense_amount_str else None
        except ValueError:
            expense_amount = None
            st.error("Будь ласка, введіть правильну суму.")

        expense_date = st.date_input("Дата видатку", min_value=datetime.today(), value=datetime.today())

        submit_button = st.form_submit_button("Зберегти видаток")
        
        if submit_button and expense_amount is not None:
            new_expense = {
                'name': expense_name,
                'amount': expense_amount,
                'date': expense_date.strftime("%Y-%m-%d")
            }
            st.session_state.expenses.append(new_expense)
            save_expense(new_expense)  # Збереження видатку
            st.success("✅ Видаток збережено!")
            st.rerun()  # Оновлюємо сторінку після додавання

# Податок
st.subheader("Податок:")
tax_percentage = st.number_input("Введіть відсоток податку:", min_value=0.0, max_value=100.0, value=5.0, step=0.5)
tax_amount = total_expenses * (tax_percentage / 100) if total_expenses > 0 else 0
st.write(f"Податок ({tax_percentage}%): {tax_amount:.2f} zł" if total_expenses > 0 else "Податок буде розраховано після додавання видатків.")

# Чистий заробіток
st.subheader("Чистий заробіток:")
income = st.number_input("Введіть щомісячний дохід (злотих):", min_value=0.0, step=100.0)

# Чистий прибуток (динамічне оновлення)
net_profit = income - total_expenses - tax_amount
st.write(f"💰 Чистий прибуток: {net_profit:.2f} zł")
