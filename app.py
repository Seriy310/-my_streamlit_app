import streamlit as st
import csv
from datetime import datetime

# Заголовок програми
st.set_page_config(page_title="Інвестиція в кав'ярню", layout="centered")
st.title("Інвестиція в кав'ярню")

# Видатки
st.subheader("Видатки:")

# Перевірка наявності видатків
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# Показуємо суму видатків або повідомлення про їх відсутність
if st.session_state.expenses:
    total_expenses = sum([exp['amount'] for exp in st.session_state.expenses])
    st.write(f"Загальна сума видатків: {total_expenses} злотих")
else:
    st.write("Видатків немає")

# Кнопка для додавання видатків
if st.button("Додати видаток"):
    with st.form("add_expense_form"):
        expense_name = st.text_input("Назва видатку")
        
        # Введення суми з "zł" на кінці
        expense_amount_str = st.text_input("Сума видатку", placeholder="Введіть суму в злотих")
        if expense_amount_str:
            # Перевірка введеного числа
            try:
                expense_amount = float(expense_amount_str.replace("zł", "").strip())  # Видаляємо "zł" і пробіли
            except ValueError:
                expense_amount = None
                st.error("Будь ласка, введіть правильну суму без символу 'zł' або з символом після суми.")
        else:
            expense_amount = None

        expense_date = st.date_input("Дата видатку", min_value=datetime.today(), value=datetime.today())

        # Додавання видатку за натисканням кнопки
        submit_button = st.form_submit_button("Зберегти видаток")
        
        if submit_button and expense_amount is not None:
            new_expense = {
                'name': expense_name,
                'amount': expense_amount,
                'date': expense_date
            }
            st.session_state.expenses.append(new_expense)
            save_expense(new_expense)  # Зберігаємо видаток у історію
            st.success("Видаток збережено!")
        elif submit_button and expense_amount is None:
            st.error("Сума видатку має бути введена коректно.")

# Виведення списку всіх видатків з можливістю редагування
st.subheader("Історія видатків:")
if st.session_state.expenses:
    for i, expense in enumerate(st.session_state.expenses):
        with st.expander(f"Видаток: {expense['name']} - {expense['amount']} злотих"):
            st.write(f"**Дата:** {expense['date']}")
            st.write(f"**Сума:** {expense['amount']} злотих")
            if st.button(f"Редагувати {expense['name']}", key=f"edit_{i}"):
                # Форма для редагування видатку
                new_name = st.text_input("Назва видатку", value=expense['name'])
                new_amount = st.number_input("Сума видатку (злотих)", min_value=0.0, step=50.0, value=expense['amount'])
                new_date = st.date_input("Дата видатку", value=expense['date'])

                if st.button("Оновити видаток", key=f"update_{i}"):
                    expense['name'] = new_name
                    expense['amount'] = new_amount
                    expense['date'] = new_date
                    save_expense(expense, update=True)  # Оновлюємо видаток в історії
                    st.success("Видаток оновлено!")

# Функція для збереження видатків у CSV файл
def save_expense(expense, update=False):
    file_name = 'expenses_history.csv'
    if update:
        # Оновлення запису в файлі (заміна всіх записів)
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Назва", "Сума", "Дата"])
            for exp in st.session_state.expenses:
                writer.writerow([exp['name'], exp['amount'], exp['date']])
    else:
        # Додавання нового видатку до файлу
        with open(file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # Якщо файл порожній, додаємо заголовки
                writer.writerow(["Назва", "Сума", "Дата"])
            writer.writerow([expense['name'], expense['amount'], expense['date']])
