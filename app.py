import streamlit as st

# Заголовок програми
st.set_page_config(page_title="Інвестиція в кав'ярню", layout="centered")
st.title("Інвестиція в кав'ярню")

# Вибір витрат
st.subheader("Видатки:")
expense_type = st.multiselect(
    "Оберіть типи витрат:",
    ["Закупки товару", "Інші кампанії", "Інтернет", "Додаткові витрати", "Податок"]
)

# Вибір або введення даних про кредит
st.subheader("Кредит:")
credit = st.checkbox("Маєте кредит?")
if credit:
    credit_amount = st.number_input("Сума кредиту (злотих):", min_value=0.0, step=100.0)
    credit_term = st.number_input("Термін кредиту (місяців):", min_value=1, step=1)

# Введення доходу
st.subheader("Дохід:")
income = st.number_input("Введіть щомісячний дохід (злотих):", min_value=0.0, step=100.0)

# Додавання кнопки для розрахунку (наприклад, для обчислення чистого прибутку)
if st.button("Розрахувати"):
    # Можна додати розрахунки на основі введених даних
    st.write(f"Витрати: {', '.join(expense_type)}")
    if credit:
        st.write(f"Сума кредиту: {credit_amount} злотих")
        st.write(f"Термін кредиту: {credit_term} місяців")
    st.write(f"Доход: {income} злотих")
