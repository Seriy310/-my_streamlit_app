import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Заголовок сторінки аналітики
st.set_page_config(page_title="Аналітика витрат та прибутку", layout="wide")
st.title("📊 Аналітика витрат та прибутку")

# 📅 Вибір періоду аналізу
date_range = st.date_input("Оберіть період для аналізу:", [])

# Завантаження витрат із файлу
file_name = "expenses_history.csv"
if not date_range:
    st.warning("Оберіть період для перегляду аналітики.")

try:
    df = pd.read_csv(file_name)
    df["Сума"] = df["Сума"].astype(float)  # Переконуємось, що сума числова

    # 🔹 Загальні показники
    total_expenses = df["Сума"].sum()
    total_income = 5000  # ⚡ Замінити на фактичний дохід
    net_profit = total_income - total_expenses

    # 📊 Відображення показників
    col1, col2, col3 = st.columns(3)
    col1.metric("Доходи", f"{total_income:.2f} zł")
    col2.metric("Витрати", f"{total_expenses:.2f} zł", delta=f"-{total_expenses:.2f}")
    col3.metric("Чистий прибуток", f"{net_profit:.2f} zł")

    # 🍩 Кругова діаграма витрат
    st.subheader("📊 Розподіл витрат")
    fig1, ax1 = plt.subplots()
    df.groupby("Назва")["Сума"].sum().plot(kind="pie", ax=ax1, autopct='%1.1f%%', startangle=90)
    ax1.set_ylabel("")  # Прибираємо зайвий підпис
    st.pyplot(fig1)

    # 📈 Стовпчиковий графік доходів і витрат
    st.subheader("📈 Динаміка доходів та витрат")
    fig2, ax2 = plt.subplots()
    ax2.bar(["Доходи", "Витрати", "Прибуток"], [total_income, total_expenses, net_profit], color=["green", "red", "blue"])
    st.pyplot(fig2)

except Exception as e:
    st.error(f"Помилка при завантаженні даних: {e}")
