import numpy as np
import matplotlib.pyplot as plt

# Параметри
T_gas = 1000  # Температура газу (K)
h = 50  # Коефіцієнт тепловіддачі (Вт/м²·К)
L = 0.5  # Товщина стінки (м)
area = 1  # Площа поверхні стінки, яку контактує з газом (м²)
alpha = 1.172e-5  # Температуропровідність (м²/с)
dt = 10  # Часовий крок (с)
nx = 20  # Кількість просторових вузлів у пластині
dx = L / (nx - 1)  # Крок по простору

# Фізичні властивості матеріалу стінки
rho = 7800  # Густина матеріалу стінки (кг/м³)
c = 500  # Питома теплоємність матеріалу (Дж/кг·К)

# Початкові температури
T_wall_hot = 20  # Температура гарячої стінки (К)
T_wall_cold = 20  # Температура холодної стінки (К)
T = np.linspace(T_wall_hot, T_wall_cold, nx)  # Початкова температура вздовж пластини

# Історія температур
T_history = [T.copy()]

# Параметри для зупинки процесу
tolerance = 0.1  # Поріг різниці температур
step = 0
equilibrium_time = None  # Час досягнення рівноваги

# Основний цикл по часу
while True:
    T_new = T.copy()

    # Конвекція: нагрівання гарячої стінки газом
    delta_T = T_gas - T_new[0]
    if delta_T > 0:  # Якщо газ гарячіший
        # Об'єм елементу, що нагрівається (м³)
        volume = dx * area
        # Кількість тепла, переданого газом до стінки (Дж)
        Q = h * delta_T * area * dt
        # Зміна температури стінки в результаті передачі тепла (К)
        delta_T_wall = Q / (rho * c * volume)
        T_new[0] += delta_T_wall

    # Теплопровідність у пластині
    for i in range(1, nx - 1):
        T_new[i] = T[i] + alpha * dt / dx ** 2 * (T[i + 1] - 2 * T[i] + T[i - 1])

    # Оновлення температури на холодній стороні
    T_new[-1] = T_new[-2]  # Задаємо умову для заізольованої холодної сторони

    # Перевірка на досягнення рівноважного стану
    if abs(T_new[-1] - T_gas) < tolerance:
        equilibrium_time = step * dt
        final_temperature = T_new[-1]  # Температура при рівновазі
        print(f"Рівноважний стан досягнуто на кроці {step}, час: {equilibrium_time} с, температура: {final_temperature} К")
        break

    # Оновлення температури для наступного кроку
    T = T_new.copy()
    T_history.append(T.copy())

    step += 1

# Побудова графіку зміни температур вздовж пластини
T_history = np.array(T_history)
time_points = np.arange(0, len(T_history)) * dt

plt.figure(figsize=(10, 6))
for i in range(0, len(T_history), max(1, len(T_history)//10)):
    plt.plot(np.linspace(0, L, nx), T_history[i], label=f'Time {i*dt:.0f} s')

plt.xlabel('Відстань вздовж пластини (м)')
plt.ylabel('Температура (К)')
plt.title('Розподіл температури вздовж пластини у різні моменти часу')
plt.legend()
plt.grid(True)
plt.show()

# Побудова графіку температури гарячої і холодної поверхонь
plt.figure(figsize=(10, 6))
plt.plot(time_points, T_history[:, 0], label='Гаряча поверхня')
plt.plot(time_points, T_history[:, -1], label='Холодна поверхня')
plt.xlabel('Час (с)')
plt.ylabel('Температура (К)')
plt.title('Зміна температури поверхонь пластини з часом')
plt.legend()
plt.grid(True)
plt.show()
