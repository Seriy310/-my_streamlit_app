import streamlit as st
import csv
import plotly.graph_objects as go

# Заголовок програми
st.set_page_config(page_title="Аналіз інвестиції та кредиту 💰", layout="centered", initial_sidebar_state="expanded")
st.title("Аналіз інвестиції та кредиту 💰")

# Опис програми
st.markdown(
    """
    Введіть параметри для розрахунку окупності вашої інвестиції та переплати по кредиту.
    """
)

# Додавання бокової панелі з інтерактивними елементами
st.sidebar.title("Меню")
st.sidebar.markdown("[🏠 Головна сторінка](#)")

# Вибір типу кредиту (якщо потрібно)
credit_type = st.sidebar.selectbox("Тип кредиту", ["Іпотечний", "Автокредит", "Кредитна картка"])

# Виведення позиції для "Кредит" у правій частині
credit_section = st.empty()  # Окрема зона для відображення іконки або кнопки

credit_section.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <h3 style="color: #007BFF; cursor: pointer;">Кредит</h3>
        <span style="color: #007BFF; font-size: 24px;">🔑</span>
    </div>
    """, unsafe_allow_html=True
)

# Вибір чекбокса для відображення кредитної інформації
credit_enabled = st.checkbox("Включити інформацію про кредит?", value=False)

if credit_enabled:
    # Виведення даних для введення кредиту
    credit_amount = st.number_input("Сума кредиту (злотих):", min_value=0.0, step=100.0, value=27000.0)
    loan_term_months = st.number_input("Термін кредиту (місяців):", min_value=1, step=1, value=48)
    monthly_payment_loan = st.number_input("Щомісячний платіж по кредиту (злотих):", min_value=0.0, step=50.0, value=669.21)
    monthly_insurance = st.number_input("Щомісячна страховка (злотих):", min_value=0.0, step=10.0, value=114.48)

    # Кнопка для переходу до історії оплат
    if st.button("Перейти до історії оплат"):
        st.sidebar.markdown("### Історія оплат")
        
        # Введення даних для обліку платежів
        payment_date = st.date_input("Дата оплати")
        payment_amount = st.number_input("Сума оплати (злотих)", min_value=0.0, step=50.0)

        # Можливість додавати платіж
        if st.button("Додати оплату"):
            save_payment(payment_date, payment_amount)  # Зберігаємо платіж
            st.write(f"Оплата на суму {payment_amount} злотих була додана на {payment_date}.")
else:
    # Якщо не натискають на "Кредит", відображається основний вміст
    royalty_percent = st.slider("Процент роялті франчайзеру (%)", 0, 100, 7)
    monthly_income = st.number_input("Щомісячний дохід від інвестиції (злотих):", min_value=0.0, step=100.0, value=1500.0)

    # Кнопка для розрахунку
    if st.button("Розрахувати", use_container_width=True):
        try:
            # Обчислення фінансових показників
            royalty_decimal = royalty_percent / 100  # Конвертація відсотків у десяткове число
            monthly_total_payment = monthly_payment_loan + monthly_insurance  # Загальні витрати по кредиту
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

# Збереження даних про платіж
def save_payment(payment_date, payment_amount):
    with open('payments_history.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([payment_date, payment_amount])

# Графік для візуалізації окупності
x_data = [i for i in range(loan_term_months)]
y_data = [credit_amount - (monthly_payment_loan + monthly_insurance) * i for i in range(loan_term_months)]

fig = go.Figure(data=[go.Scatter(x=x_data, y=y_data, mode='lines', name="Залишок по кредиту")])
fig.update_layout(title='Залишок по кредиту з часом', xaxis_title='Місяці', yaxis_title='Залишок по кредиту (злотих)')
st.plotly_chart(fig)

