import streamlit as st
import matplotlib.pyplot as plt

# Заголовок
st.set_page_config(page_title="Інвестиція в кав'ярню", layout="wide")
st.title("Інвестиція в кав'ярню")

# Видатки
st.subheader("Видатки:")
expense_type = st.multiselect(
    "Оберіть типи витрат:",
    ["Закупки товару", "Інші кампанії", "Інтернет", "Додаткові витрати", "Податок"]
)

# Виведення суми видатків
st.write(f"Загальна сума видатків: 5000 злотих")

# Кнопка для додавання витрат
add_expense = st.button("Додати видаток")

if add_expense:
    with st.expander("Додати видаток"):
        expense_name = st.text_input("Назва видатку")
        expense_amount = st.number_input("Сума видатку (злотих)", min_value=0.0, step=50.0)
        expense_date = st.date_input("Дата видатку")

        if st.button("Зберегти видаток"):
            st.write("Видаток збережено!")
            # Тут зберігаємо видаток в базу або історію

# Графік для візуалізації витрат
st.subheader("Графік витрат:")
fig, ax = plt.subplots()
ax.bar(["Закупки товару", "Інші кампанії", "Інтернет"], [1000, 1500, 2500])
ax.set_ylabel('Сума (злотих)')
ax.set_title('Витрати по категоріях')
st.pyplot(fig)

# Дохід
st.subheader("Дохід:")
income = st.number_input("Введіть щомісячний дохід (злотих):", min_value=0.0, step=100.0)

if st.button("Розрахувати"):
    st.write(f"Доход: {income} злотих")
