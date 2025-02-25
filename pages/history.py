# Переконуємось, що стовпець "Сума" містить лише числа
df["Сума"] = pd.to_numeric(df["Сума"], errors='coerce').fillna(0.0)

# 🔹 Фільтрація за сумою
st.subheader("💰 Фільтрація за сумою")
col3, col4 = st.columns(2)
min_amount = col3.number_input("Мінімальна сума", min_value=0.0, value=float(df["Сума"].min()) if not df.empty else 0.0)
max_amount = col4.number_input("Максимальна сума", min_value=0.0, value=float(df["Сума"].max()) if not df.empty else 10000.0)
