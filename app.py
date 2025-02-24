# Re-import necessary libraries after execution state reset
import matplotlib.pyplot as plt

# Create a mock-up layout of the interactive analytics dashboard
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis("off")

# Title
ax.text(5, 9.5, "📊 Аналітика витрат та прибутку", fontsize=14, fontweight="bold", ha="center")

# Dropdown for selecting date range
ax.text(1, 8.8, "📅 Виберіть період:", fontsize=12, fontweight="bold")
ax.add_patch(plt.Rectangle((3, 8.6), 4, 0.5, fill=True, color="lightgray", alpha=0.3))
ax.text(5, 8.85, "[Dropdown - вибір періоду]", fontsize=10, ha="center")

# Section: Pie Chart (Expense Distribution)
ax.text(1, 7.8, "🍩 Розподіл витрат", fontsize=12, fontweight="bold")
ax.add_patch(plt.Rectangle((1, 5.8), 4, 1.8, fill=True, color="lightgray", alpha=0.3))  # Placeholder for pie chart
ax.text(3, 6.7, "[Кругова діаграма]", fontsize=10, ha="center")

# Section: Bar Chart (Income vs Expenses)
ax.text(6, 7.8, "📈 Динаміка доходів та витрат", fontsize=12, fontweight="bold")
ax.add_patch(plt.Rectangle((5.5, 5.8), 4, 1.8, fill=True, color="lightgray", alpha=0.3))  # Placeholder for bar chart
ax.text(7.5, 6.7, "[Стовпчиковий графік]", fontsize=10, ha="center")

# Section: Net Profit Trend
ax.text(1, 5, "📉 Чистий прибуток по місяцях", fontsize=12, fontweight="bold")
ax.add_patch(plt.Rectangle((1, 3.2), 8, 1.5, fill=True, color="lightgray", alpha=0.3))  # Placeholder for line chart
ax.text(5, 4, "[Графік чистого прибутку]", fontsize=10, ha="center")

# Summary Section
ax.text(1, 2.2, "📊 Загальні показники:", fontsize=12, fontweight="bold")
ax.text(1, 1.8, "Доходи: [5000 zł]", fontsize=10, bbox=dict(facecolor="lightgray", edgecolor="black"))
ax.text(4, 1.8, "Витрати: [3500 zł]", fontsize=10, bbox=dict(facecolor="lightgray", edgecolor="black"))
ax.text(7, 1.8, "Прибуток: [1500 zł]", fontsize=10, bbox=dict(facecolor="lightgray", edgecolor="black"))

plt.show()
