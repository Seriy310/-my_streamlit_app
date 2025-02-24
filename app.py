import streamlit as st
import csv
import os
from datetime import datetime

# Заголовок програми
st.set_page_config(page_title="Інвестиція в кав'ярню", layout="centered")
st.title("Інвестиція в кав'ярню")

# Функція для збереження видатків у CSV файл
def save_expenses(expenses):
    file_name = 'expenses_history.csv'
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Якщо файл порожній, додаємо заголовки
            writer.writerow(["Назва", "Сума", "Дата"])
        for expense in expenses:
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
                    'amount': round(float(row['Сума']) / 10) * 10,  # Округлення до десятків
                    'date': row['Дата']
                })

# Видатки
st.subheader("Видатки:")
total_expenses = sum(exp['amount'] for exp in st.session_state.expenses)
st.write(f"Загальна сума видатків: {total_expenses:.2f} zł" if total_expenses > 0 else "Видатків немає")

# Кнопка переходу до історії видатків
if st.button("📜 Переглянути / Редагувати історію видатків"):
    st.switch_page("pages/history.py")

# Форма для додавання видатків (Список)
with st.expander("➕ Додати нові видатки"):
    with st.form("add_expense_form"):
        expense_list = st.text_area(
            "Введіть список видатків у форматі: Назва - Сума (кожен рядок окремий)",
            placeholder="Кава - 50\nОренда - 1200\nЗакупівля - 300"
        )
        expense_date = st.date_input("Дата видатків", min_value=datetime.today(), value=datetime.today())

        submit_button = st.form_submit_button("Зберегти видатки")
        
        if submit_button and expense_list.strip():
            new_expenses = []
            for line in expense_list.split("\n"):
                parts = line.split("-")
                if len(parts) == 2:
                    name, amount_str = parts[0].strip(), parts[1].strip()
                    try:
                        amount = round(float(amount_str.replace("zł", "").strip()) / 10) * 10  # Округлення до десятків
                        new_expenses.append({'name': name, 'amount': amount, 'date': expense_date.strftime("%Y-%m-%d")})
                    except ValueError:
                        st.error(f"Помилка у рядку: {line}")
            
            if new_expenses:
                st.session_state.expenses.extend(new_expenses)
                save_expenses(new_expenses)
                st.success("✅ Видатки збережено!")
                st.rerun()  # Оновлення сторінки після додавання

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
