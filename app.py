import streamlit as st

# Заголовок
st.title("Аналіз інвестиції та кредиту 💰")

# Ввід даних користувачем
credit_amount = st.number_input("Сума кредиту (злотих):", min_value=0.0, step=100.0)
loan_term_months = st.number_input("Термін кредиту (місяців):", min_value=1, step=1)
monthly_payment_loan = st.number_input("Щомісячний платіж по кредиту (злотих):", min_value=0.0, step=50.0)
monthly_insurance = st.number_input("Щомісячна страховка (злотих):", min_value=0.0, step=10.0)
royalty_percent = st.number_input("Процент роялті франчайзеру (%):", min_value=0.0, max_value=100.0, step=1.0)
monthly_income = st.number_input("Щомісячний дохід від інвестиції (злотих):", min_value=0.0, step=100.0)

# Кнопка для розрахунку
if st.button("Розрахувати"):
    try:
        # Обчислення фінансових показників
        royalty_decimal = royalty_percent / 100  # Конвертація відсотків у десяткове число
        monthly_total_payment = monthly_payment_loan + monthly_insurance  # Загальні щомісячні витрати
        total_payment_over_loan_term = monthly_total_payment * loan_term_months  # Загальна сума виплат
        overpayment = total_payment_over_loan_term - credit_amount  # Переплата по кредиту
        royalty_payment = monthly_income * royalty_decimal  # Щомісячне роялті
        net_profit = monthly_income - monthly_total_payment - royalty_payment  # Чистий прибуток
        time_to_coverage_overpayment = overpayment / net_profit if net_profit > 0 else float('inf')  # Час окупності

        # Виведення результатів
        st.subheader("📊 Результати розрахунку:")
        st.write(f"✅ **Загальна переплата по кредиту:** {overpayment:.2f} злотих")
        st.write(f"💰 **Щомісячне роялті франчайзеру:** {royalty_payment:.2f} злотих")
        st.write(f"📈 **Чистий прибуток на місяць:** {net_profit:.2f} злотих")
        st.write(f"⌛ **Час для покриття переплати:** {time_to_coverage_overpayment:.2f} місяців")
    
    except ValueError:
        st.error("Помилка! Будь ласка, введіть коректні числові значення.")
