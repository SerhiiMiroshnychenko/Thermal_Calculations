"""
Початкова температура стінки становить 300 K.
Газ має температуру 600 K.
Ми моделюємо нагрівання стінки газом за рахунок конвекції на її поверхні.
На графіку відображено розподіл температури вздовж стінки для різних моментів часу.
"""

import numpy as np
import matplotlib.pyplot as plt

# Параметри
T_wall_initial = 300  # Початкова температура стінки (К)
T_gas = 600  # Температура газу (К)
h = 50  # Коефіцієнт тепловіддачі (Вт/м²·К)
dt = 0.0001  # Часовий крок (с)
tolerance = 1  # Поріг різниці температур

# Ініціалізація температури
T_wall = T_wall_initial

# Графік температури в кожен момент часу
T_history = [T_wall]

step = 0

# Основний цикл часу
while True:
    # Обчислення нової температури стінки
    delta_T = T_gas - T_wall
    if delta_T > 0:  # Якщо газ гарячіший
        T_wall += h * delta_T * dt  # Нагрівання гарячим газом

    T_history.append(T_wall)

    # Перевірка умов зупинки
    if np.abs(T_wall - T_gas) < tolerance:
        break
    step += 1

# Графік результату
plt.figure(figsize=(10, 6))
time_points = np.linspace(0, len(T_history) * dt, len(T_history))

# Додавання крапок для температури стінки
plt.scatter(time_points, T_history, color='cyan', label='Температура стінки', alpha=0.5)

# Додавання крапки для температури газу
plt.scatter(time_points, [T_gas] * len(time_points), color='orange', label='Температура газу', alpha=0.5)

# Додавання легенди та підписів
plt.xlabel("Час (с)")
plt.ylabel("Температура (К)")
plt.title("Нестаціонарний теплообмін стінки з газом до вирівнювання температур")
plt.axhline(y=T_gas, color='orange', linestyle='--', label='Температура газу')
plt.legend()
plt.grid()

# Виведення значення кінцевого часу на графіку
final_time = len(T_history) * dt
plt.figtext(0.5, 0.01, f'Кінцевий час: {final_time:.4f} с', ha='center', fontsize=12)

# Показ графіка
plt.show()
