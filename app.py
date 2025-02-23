import streamlit as st

# Заголовок програми
st.title("Аналіз інвестиції та кредиту 💰")
st.markdown(
    """
    Введіть параметри для розрахунку окупності вашої інвестиції та переплати по кредиту.
    """
)

# Ввід даних користувачем з налаштуваннями стилів
credit_amount = st.number_input("Сума кредиту (злотих):", min_value=0.0, step=100.0, value=27000.0)
loan_term_months = st.number_input("Термін кредиту (місяців):", min_value=1, step=1, value=48)
monthly_payment_loan = st.number_input("Щомісячний платіж по кредиту (злотих):", min_value=0.0, step=50.0, value=669.21)
monthly_insurance = st.number_input("Щомісячна страховка (злотих):", min_value=0.0, step=10.0, value=114.48)
royalty_percent = st.number_input("Процент роялті франчайзеру (%):", min_value=0.0, max_value=100.0, step=1.0, value=7.0)
monthly_income = st.number_input("Щомісячний дохід від інвестиції (злотих):", min_value=0.0, step=100.0, value=1500.0)

# Кнопка для розрахунку
if st.button("Розрахувати", use_container_width=True):
    try:
        # Обчислення фінансових показників
        royalty_decimal = royalty_percent / 100  # Конвертація відсотків у десяткове число
        monthly_total_payment = monthly_payment_loan + monthly_insurance  # Загальні щомісячні витрати
        total_payment_over_loan_term = monthly_total_payment * loan_term_months  # Загальна сума виплат
        overpayment = total_payment_over_loan_term - credit_amount  # Переплата по кредиту
        royalty_payment = monthly_income * royalty_decimal  # Щомісячне роялті
        net_profit = monthly_income - monthly_total_payment - royalty_payment  # Чистий прибуток
        time_to_coverage_overpayment = overpayment / net_profit if net_profit > 0 else float('inf')  # Час окупності

        # Виведення результатів з покращеним дизайном
        st.subheader("📊 Результати розрахунку:")
        st.markdown(f"✅ **Загальна переплата по кредиту:** {overpayment:.2f} злотих", unsafe_allow_html=True)
        st.markdown(f"💰 **Щомісячне роялті франчайзеру:** {royalty_payment:.2f} злотих", unsafe_allow_html=True)
        st.markdown(f"📈 **Чистий прибуток на місяць:** {net_profit:.2f} злотих", unsafe_allow_html=True)
        st.markdown(f"⌛ **Час для покриття переплати:** {time_to_coverage_overpayment:.2f} місяців", unsafe_allow_html=True)
        
        # Додавання підсвітки за допомогою кольорів
        if net_profit > 0:
            st.success("👍 Ви отримуєте чистий прибуток щомісяця!")
        else:
            st.error("⚠️ Ви не отримуєте прибуток, і ваші витрати перевищують доходи.")
    
    except ValueError:
        st.error("Помилка! Будь ласка, введіть коректні числові значення.")
