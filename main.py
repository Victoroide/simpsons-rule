import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from sympy import symbols, lambdify, sympify

def simpson_3_8(f_lambda, a, b, n=40):
    if n % 3 != 0:
        n += 3 - (n % 3)  # Ajusta n para que sea múltiplo de 3

    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    f_x = f_lambda(x)

    integral_approx = (3 * h / 8) * (f_x[0] + f_x[-1] + 3 * np.sum(f_x[1:-1:3]) + 3 * np.sum(f_x[2:-1:3]) + 2 * np.sum(f_x[3:-1:3]))
    return integral_approx

func_str = input("Ingrese la función en términos de 'x': ")
a_str = input("Ingrese el límite inferior 'a' de la integral: ")
b_str = input("Ingrese el límite superior 'b' de la integral: ")

# Convertir la función a una función lambda
x = symbols('x')
func = sympify(func_str.replace('^', '**'))
f_lambda = lambdify(x, func, 'numpy')

# Convertir los límites a flotantes
a, b = float(sympify(a_str)), float(sympify(b_str))

# Calcular la integral aproximada
integral_result = simpson_3_8(f_lambda, a, b)

# Calcular la integral exacta
integral_exacta, _ = quad(f_lambda, a, b)

# Calcular el error
error = abs(integral_exacta - integral_result)
if error < 0.001:
    error_str = "{:.3e}".format(error)
else:
    error_str = str(error)

# Crea la gráfica
fig, ax = plt.subplots()
X = np.linspace(a, b, 1000)
Y = f_lambda(X)
ax.plot(X, Y, label=f'f(x) = {func_str}')
ax.set_title(f"Integral aproximada por la Regla de Simpson 3/8: {integral_result:.4f}, Error: {error_str}")
ax.legend()
plt.show()
