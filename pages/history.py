import streamlit as st
import csv
import os

st.set_page_config(page_title="Історія видатків", layout="centered")
st.title("📜 Історія видатків (Редагування)")

file_name = "expenses_history.csv"

# Завантажуємо дані з файлу
expenses = []
if os.path.exists(file_name):
    with open(file_name, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            expenses.append({
                'Назва': row['Назва'],
                'Сума': round(float(row['Сума']) / 10) * 10,  # Ensure float values and round to tens
                'Дата': row['Дата']
            })

# Видалення видатку
if "delete_index" not in st.session_state:
    st.session_state.delete_index = None

# Відображення редагованої таблиці
edited_expenses = []
if expenses:
    st.write("Редагуйте дані або видаліть позиції натиснувши на ❌.")
    
    for i, exp in enumerate(expenses):
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        name = col1.text_input(f"Назва {i+1}", value=exp["Назва"], key=f"name_{i}")
        amount = col2.number_input(f"Сума {i+1}", value=float(exp["Сума"]), step=10.0, key=f"amount_{i}")
        date = col3.text_input(f"Дата {i+1}", value=exp["Дата"], key=f"date_{i}")
        delete_button = col4.button("❌", key=f"delete_{i}")

        if delete_button:
            st.session_state.delete_index = i  # Store index of the item to delete

        edited_expenses.append({'name': name, 'amount': round(amount / 10) * 10, 'date': date})

    # Видалення обраного запису
    if st.session_state.delete_index is not None:
        del edited_expenses[st.session_state.delete_index]
        st.session_state.delete_index = None  # Reset index
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Назва", "Сума", "Дата"])
            for exp in edited_expenses:
                writer.writerow([exp['name'], exp['amount'], exp['date']])
        st.success("✅ Видаток видалено!")
        st.rerun()  # Перезапуск сторінки для оновлення

    if st.button("💾 Зберегти зміни"):
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Назва", "Сума", "Дата"])
            for exp in edited_expenses:
                writer.writerow([exp['name'], exp['amount'], exp['date']])
        st.success("✅ Зміни збережено!")
        st.rerun()  # Перезапуск сторінки для оновлення

else:
    st.write("Наразі історія видатків порожня.")

# Кнопка для повернення на головну сторінку
if st.button("⬅️ Назад до головної"):
    st.switch_page("app.py")
