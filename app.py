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
total_expenses = sum(float(exp['amount']) for exp in st.session_state.expenses)  # Ensure correct summation
st.write(f"Загальна сума видатків: {total_expenses:.2f} zł" if total_expenses > 0 else "Видатків немає")

# Кнопка переходу до історії видатків
if st.button("📜 Переглянути / Редагувати історію видатків"):
    st.switch_page("pages/history.py")

# Форма для додавання видатків (динамічна таблиця)
st.subheader("➕ Додати нові видатки")

if "new_expenses" not in st.session_state:
    st.session_state.new_expenses = [{"name": "", "amount": "", "date": datetime.today().strftime("%Y-%m-%d")}]

to_remove = []

for i, exp in enumerate(st.session_state.new_expenses):
    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
    name = col1.text_input(f"Назва {i+1}", value=exp["name"], key=f"new_name_{i}")
    amount = col2.text_input(f"Сума {i+1} (zł)", value=str(exp["amount"]), key=f"new_amount_{i}")
    date = col3.date_input(f"Дата {i+1}", value=datetime.strptime(exp["date"], "%Y-%m-%d"), key=f"new_date_{i}")
    
    if name.strip() and amount.strip():  # If filled, prepare for the next entry
        if i == len(st.session_state.new_expenses) - 1:
            st.session_state.new_expenses.append({"name": "", "amount": "", "date": datetime.today().strftime("%Y-%m-%d")})

    try:
        amount = round(float(amount.replace("zł", "").strip()) / 10) * 10
    except ValueError:
        amount = None
        st.error(f"Помилка у рядку {i+1}: Сума повинна бути числом.")

    st.session_state.new_expenses[i] = {"name": name, "amount": amount, "date": date.strftime("%Y-%m-%d")}

    delete_button = col4.button("❌", key=f"remove_{i}")
    if delete_button:
        to_remove.append(i)

# Видалення порожніх записів
for index in sorted(to_remove, reverse=True):
    del st.session_state.new_expenses[index]

# Кнопка для збереження видатків
if st.button("💾 Зберегти видатки"):
    valid_expenses = [exp for exp in st.session_state.new_expenses if exp["name"] and exp["amount"]]
    
    if valid_expenses:
        st.session_state.expenses.extend(valid_expenses)
        save_expenses(valid_expenses)
        st.session_state.new_expenses = [{"name": "", "amount": "", "date": datetime.today().strftime("%Y-%m-%d")}]
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
