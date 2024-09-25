import numpy as np
import matplotlib.pyplot as plt

# Вихідні дані
L = 1  # Товщина стінки (м)
T1_initial = 400  # Початкова температура гарячої поверхні (К)
T2_initial = 300  # Початкова температура холодної поверхні (К)
alpha = 1.172e-5  # Температуропровідність (м²/с)

# Налаштування сітки
nx = 20  # Кількість просторових вузлів
dx = L / (nx - 1)  # Крок по простору
dt = 1  # Крок по часу
T = np.linspace(T1_initial, T2_initial, nx)  # Початкова температура вздовж стінки

# Масив для результатів
T_history = [T.copy()]

# Задаємо точність для зупинки процесу
tolerance = 0.1  # Поріг різниці температур
step = 0
equilibrium_time = None  # Час досягнення рівноваги

# Основний цикл по часу
while True:
    T_new = T.copy()

    # Обчислення температур у внутрішніх точках
    for i in range(1, nx - 1):
        T_new[i] = T[i] + alpha * dt / dx ** 2 * (T[i + 1] - 2 * T[i] + T[i - 1])

    # Оновлення температури на поверхнях
    T_new[0] = T_new[1]  # Гаряча поверхня
    T_new[-1] = T_new[-2]  # Холодна поверхня

    # Перевірка на досягнення рівноважного стану
    if abs(T_new[0] - T_new[-1]) < tolerance:
        equilibrium_time = step * dt
        final_temperature = T_new[0]  # Температура при рівновазі
        print(
            f"Рівноважний стан досягнуто на кроці {step}, час: {equilibrium_time} с, температура: {final_temperature} К")
        break

    # Оновлення температури
    T = T_new.copy()
    T_history.append(T.copy())

    step += 1

# Побудова графіка для крапок
T_history = np.array(T_history)
time_points = np.arange(0, len(T_history)) * dt

# Температури поверхонь
cold_surface_temps = T_history[:, -1]  # Температура на холодній поверхні
hot_surface_temps = T_history[:, 0]  # Температура на гарячій поверхні

# Побудова графіка крапок
plt.figure(figsize=(10, 6))

# Блакитні крапки для холодної поверхні (по осі Y - температура, по осі X - час)
plt.scatter(time_points, cold_surface_temps, color='blue', label='Cold Surface (T2)', s=20)

# Помаранчеві крапки для гарячої поверхні (по осі Y - температура, по осі X - час)
plt.scatter(time_points, hot_surface_temps, color='orange', label='Hot Surface (T1)', s=20)

# Додаємо вертикальну лінію для часу досягнення рівноважного стану
if equilibrium_time is not None:
    plt.axvline(x=equilibrium_time, color='green', linestyle='--', label=f'Equilibrium Time: {equilibrium_time:.2f} s')
    plt.text(equilibrium_time + 0.1, (T1_initial + T2_initial) / 2, f'{equilibrium_time:.2f} с', color='green')

# Додаємо підпис про кінцевий час і рівну температуру під графіком
if equilibrium_time is not None:
    plt.figtext(0.5, -0.1,
                f"Кінцевий час досягнення рівноваги: {equilibrium_time:.2f} с, Кінцева температура: {final_temperature:.2f} К",
                ha="center", fontsize=12, bbox={"facecolor": "lightgray", "alpha": 0.5, "pad": 5})

# Налаштування графіка
plt.ylabel('Температура (К)')
plt.title('Зміна температури поверхонь стінки з часом')
plt.legend()
plt.grid(True)
plt.tight_layout()  # Автоматична оптимізація розташування елементів
plt.show()
