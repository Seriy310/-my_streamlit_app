import streamlit as st
import os
import pandas as pd
from datetime import datetime

# Налаштування сторінки
st.set_page_config(page_title="Інвестиція в кав'ярню", layout="centered")
st.title("☕ Інвестиція в кав'ярню")

# 🔹 Завантажуємо дані
file_name = "expenses_history.csv"
if not os.path.exists(file_name):
    df = pd.DataFrame(columns=["Назва", "Сума", "Дата"])
    df.to_csv(file_name, index=False)
else:
    df = pd.read_csv(file_name)

df["Дата"] = pd.to_datetime(df["Дата"], errors='coerce').dt.date  # Видаляємо години

# 📊 Загальна сума витрат
total_expenses = df["Сума"].sum() if not df.empty else 0
st.subheader(f"📉 Загальна сума видатків: {total_expenses:.2f} zł")

# 📜 Кнопки для переходу на сторінки
col1, col2 = st.columns(2)
with col1:
    if st.button("📜 Переглянути історію витрат"):
        st.switch_page("pages/history.py")

with col2:
    if st.button("📈 Переглянути аналітику"):
        st.switch_page("pages/analytics.py")

# ➕ Форма для додавання нових видатків
st.subheader("➕ Додати нові видатки")

if "new_expenses" not in st.session_state:
    st.session_state.new_expenses = [{"name": "", "amount": "", "date": datetime.today().strftime("%Y-%m-%d")}]

to_remove = []

for i, exp in enumerate(st.session_state.new_expenses):
    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
    name = col1.text_input(f"Назва {i+1}", value=exp["name"], key=f"new_name_{i}")
    amount = col2.text_input(f"Сума {i+1} (zł)", value=str(exp["amount"]), key=f"new_amount_{i}")
    date = col3.date_input(f"Дата {i+1}", value=datetime.strptime(exp["date"], "%Y-%m-%d"), key=f"new_date_{i}")
    
    if name.strip() and amount.strip():  # Якщо поле заповнене, додаємо новий рядок
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
        df_new = pd.DataFrame(valid_expenses)
        df_new["Сума"] = df_new["amount"]
        df_new["Дата"] = df_new["date"]
        df_new = df_new.drop(columns=["amount", "date"])
        
        df = pd.concat([df, df_new], ignore_index=True)
        df.to_csv(file_name, index=False)
        
        st.session_state.new_expenses = [{"name": "", "amount": "", "date": datetime.today().strftime("%Y-%m-%d")}]
        st.success("✅ Видатки збережено!")
        st.rerun()

# 📉 Податковий розрахунок
st.subheader("📉 Податок")
tax_percentage = st.number_input("Введіть відсоток податку:", min_value=0.0, max_value=100.0, value=5.0, step=0.5)
tax_amount = total_expenses * (tax_percentage / 100) if total_expenses > 0 else 0
st.write(f"Податок ({tax_percentage}%): {tax_amount:.2f} zł" if total_expenses > 0 else "Податок буде розраховано після додавання видатків.")

# 💰 Чистий прибуток
st.subheader("💰 Чистий прибуток")
income = st.number_input("Введіть щомісячний дохід (злотих):", min_value=0.0, step=100.0)
net_profit = income - total_expenses - tax_amount
st.write(f"💰 Чистий прибуток: {net_profit:.2f} zł")
