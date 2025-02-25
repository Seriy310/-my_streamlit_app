import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Історія видатків", layout="centered")
st.title("📜 Історія видатків")

file_name = "expenses_history.csv"

# Завантажуємо дані з файлу
if os.path.exists(file_name):
    df = pd.read_csv(file_name)
    df["Дата"] = pd.to_datetime(df["Дата"]).dt.date  # Приховуємо години
else:
    st.write("Наразі історія видатків порожня.")
    df = pd.DataFrame(columns=["Назва", "Сума", "Дата"])

# 🔹 Фільтрація за датою
st.subheader("📅 Фільтрація за датою")
col1, col2 = st.columns(2)
min_date = col1.date_input("Виберіть початкову дату", df["Дата"].min() if not df.empty else None)
max_date = col2.date_input("Виберіть кінцеву дату", df["Дата"].max() if not df.empty else None)

# 🔹 Фільтрація за сумою
st.subheader("💰 Фільтрація за сумою")
col3, col4 = st.columns(2)
min_amount = col3.number_input("Мінімальна сума", min_value=0.0, value=df["Сума"].min() if not df.empty else 0.0)
max_amount = col4.number_input("Максимальна сума", min_value=0.0, value=df["Сума"].max() if not df.empty else 10000.0)

# 🔹 Застосування фільтрів
if not df.empty:
    df_filtered = df[
        (df["Дата"] >= min_date) & (df["Дата"] <= max_date) &
        (df["Сума"] >= min_amount) & (df["Сума"] <= max_amount)
    ]
    st.write(f"Знайдено {len(df_filtered)} записів")
    st.dataframe(df_filtered)
else:
    st.write("Немає записів для відображення.")

# 🔹 Кнопка для повернення на головну сторінку
if st.button("⬅️ Назад до головної"):
    st.switch_page("app.py")
