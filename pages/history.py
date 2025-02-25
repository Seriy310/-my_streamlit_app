import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Історія витрат", layout="centered")
st.title("📜 Історія витрат")

file_name = "expenses_history.csv"

if not os.path.exists(file_name):
    st.write("⛔ Немає даних для відображення.")
    df = pd.DataFrame(columns=["Назва", "Сума", "Дата"])
else:
    df = pd.read_csv(file_name)

df["Дата"] = pd.to_datetime(df["Дата"], errors='coerce').dt.date
df["Сума"] = pd.to_numeric(df["Сума"], errors='coerce').fillna(0.0)

# 🔹 Фільтрація за датою
st.subheader("📅 Фільтр за датою")
col1, col2 = st.columns(2)
min_date = col1.date_input("Початкова дата", df["Дата"].min() if not df.empty else datetime.today())
max_date = col2.date_input("Кінцева дата", df["Дата"].max() if not df.empty else datetime.today())

# 🔹 Фільтрація за сумою
st.subheader("💰 Фільтр за сумою")
col3, col4 = st.columns(2)
min_amount = col3.number_input("Мінімальна сума (zł)", min_value=0.0, value=df["Сума"].min() if not df.empty else 0.0)
max_amount = col4.number_input("Максимальна сума (zł)", min_value=0.0, value=df["Сума"].max() if not df.empty else 10000.0)

# 🔹 Застосування фільтрів
df_filtered = df[
    (df["Дата"] >= min_date) & (df["Дата"] <= max_date) &
    (df["Сума"] >= min_amount) & (df["Сума"] <= max_amount)
]

st.write(f"🔍 Знайдено {len(df_filtered)} записів")
st.dataframe(df_filtered)

# 🔙 Кнопка для повернення на головну сторінку
if st.button("⬅️ Назад"):
    st.switch_page("app.py")
