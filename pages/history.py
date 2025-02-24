import streamlit as st
import csv
import os

st.set_page_config(page_title="Історія видатків", layout="centered")
st.title("📜 Історія видатків")

file_name = "expenses_history.csv"

# Завантажуємо дані з файлу
expenses = []
if os.path.exists(file_name):
    with open(file_name, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            expenses.append({
                'Назва': row['Назва'],
                'Сума': float(row['Сума']),
                'Дата': row['Дата']
            })

# Відображення таблиці витрат
if expenses:
    st.table(expenses)
else:
    st.write("Наразі історія видатків порожня.")

# Кнопка для повернення на головну сторінку
if st.button("⬅️ Назад до головної"):
    st.switch_page("app.py")
