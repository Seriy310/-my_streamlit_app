import streamlit as st

# Заголовок програми
st.title("Аналіз інвестиції та кредиту 💰")

# Створення вибору сторінки
page = st.selectbox("Виберіть сторінку", ["Основна сторінка", "Облік сплати кредиту"])

if page == "Основна сторінка":
    # Ввід даних користувачем
    credit_enabled = st.checkbox("Включити інформацію про кредит?", value=True)

    if credit_enabled:
        credit_amount = st.number_input("Сума кредиту (злотих):", min_value=0.0, step=100.0, value=27000.0)
        loan_term_months = st.number_input("Термін кредиту (місяців):", min_value=1, step=1, value=48)
        monthly_payment_loan = st.number_input("Щомісячний платіж по кредиту (злотих):", min_value=0.0, step=50.0, value=669.21)
        monthly_insurance = st.number_input("Щомісячна страховка (злотих):", min_value=0.0, step=10.0, value=114.48)

    # Інші параметри, що не залежать від вибору про кредит
    royalty_percent = st.number_input("Процент роялті франчайзеру (%):", min_value=0.0, max_value=100.0, step=1.0, value=7.0)
    monthly_income = st.number_input("Щомісячний дохід від інвестиції (злотих):", min_value=0.0, step=100.0, value=1500.0)

    # Кнопка для розрахунку
    if st.button("Розрахувати", use_container_width=True):
        try:
            # Обчислення фінансових показників
            royalty_decimal = royalty_percent / 100  # Конвертація відсотків у десяткове число
            if credit_enabled:
                # Загальні щомісячні витрати, якщо кредит активний
                monthly_total_payment = monthly_payment_loan + monthly_insurance  # Загальні витрати по кредиту
                total_payment_over_loan_term = monthly_total_payment * loan_term_months  # Загальна сума виплат
                overpayment = total_payment_over_loan_term - credit_amount  # Переплата по кредиту
            else:
                # Якщо кредит відключено, лише рахуємо роялті та дохід
                overpayment = 0
                monthly_total_payment = 0  # Без кредиту
                total_payment_over_loan_term = 0

            royalty_payment = monthly_income * royalty_decimal  # Щомісячне роялті
            net_profit = monthly_income - monthly_total_payment - royalty_payment  # Чистий прибуток
            time_to_coverage_overpayment = overpayment / net_profit if net_profit > 0 else float('inf')  # Час окупності

            # Виведення результатів з покращеним дизайном
            st.subheader("📊 Результати розрахунку:")
            if credit_enabled:
                st.markdown(f"✅ **Загальна переплата по кредиту:** {overpayment:.2f} злотих", unsafe_allow_html=True)
                st.markdown(f"💰 **Щомісячне роялті франчайзеру:** {royalty_payment:.2f} злотих", unsafe_allow_html=True)
                st.markdown(f"📈 **Чистий прибуток на місяць:** {net_profit:.2f} злотих", unsafe_allow_html=True)
                st.markdown(f"⌛ **Час для покриття переплати:** {time_to_coverage_overpayment:.2f} місяців", unsafe_allow_html=True)
            else:
                st.markdown(f"💰 **Щомісячне роялті франчайзеру:** {royalty_payment:.2f} злотих", unsafe_allow_html=True)
                st.markdown(f"📈 **Чистий прибуток на місяць (без кредиту):** {net_profit:.2f} злотих", unsafe_allow_html=True)

            # Додавання підсвітки за допомогою кольорів
            if net_profit > 0:
                st.success("👍 Ви отримуєте чистий прибуток щомісяця!")
            else:
                st.error("⚠️ Ви не отримуєте прибуток, і ваші витрати перевищують доходи.")
        
        except ValueError:
            st.error("Помилка! Будь ласка, введіть коректні числові значення.")
    
elif page == "Облік сплати кредиту":
    st.subheader("Облік сплати кредиту")

    # Введення даних для обліку кредиту
    loan_balance = st.number_input("Початковий баланс кредиту (злотих):", min_value=0.0, step=100.0, value=27000.0)
    monthly_payment = st.number_input("Щомісячний платіж по кредиту:", min_value=0.0, step=50.0, value=669.21)
    
    # Ведення обліку сплати
    months_paid = st.number_input("Кількість місяців, протягом яких вже сплачено кредит:", min_value=0, step=1, value=0)
    current_balance = loan_balance - (monthly_payment * months_paid)
    
    st.write(f"**Залишок по кредиту після сплати:** {current_balance:.2f} злотих")
    
    # Додавання можливості зберігати дані (псевдозбереження для прикладу)
    st.write("Це простий облік, якщо потрібно зберігати дані, рекомендуємо використовувати базу даних або CSV файл.")
