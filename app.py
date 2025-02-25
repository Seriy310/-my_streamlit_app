import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Кав'ярня: Витрати", layout="centered")
st.title("☕ Інвестиції у кав'ярню")

file_name = "expenses_history.csv"

# Перевіряємо, чи існує файл
if not os.path.exists(file_name):
    df = pd.DataFrame(columns=["Назва", "Сума", "Дата"])
    df.to_csv(file_name, index=False)
else:
    df = pd.read_csv(file_name)

df["Дата"] = pd.to_datetime(df["Дата"], errors='coerce').dt.date  # Прибираємо години
df["Сума"] = pd.to_numeric(df["Сума"], errors='coerce').fillna(0.0)  # Забезпечуємо, що це float

# 📊 Загальна сума витрат
total_expenses = df["Сума"].sum() if not df.empty else 0.0
st.subheader(f"📉 Загальна сума витрат: {total_expenses:.2f} zł")

# ➕ Форма для додавання нових витрат
st.subheader("➕ Додати витрати")
col1, col2 = st.columns([3, 2])
name = col1.text_input("Назва витрати")
amount = col2.number_input
