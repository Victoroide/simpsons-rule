import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, lambdify, sympify

def simpson_3_8(f_lambda, a, b, n=100):
    x = np.linspace(a, b, n+1)
    h = (b - a) / n
    integral = (3 * h / 8) * (f_lambda(a) + 2 * sum(f_lambda(x[3:-1:3])) + 3 * sum(f_lambda(x[1:-1:3])) + 3 * sum(f_lambda(x[2:-1:3])) + f_lambda(b))
    return integral

func_str = input("Ingrese la función en términos de 'x': ")
a_str = input("Ingrese el límite inferior 'a' de la integral: ")
b_str = input("Ingrese el límite superior 'b' de la integral: ")

# Convert the function to a lambda function
x = symbols('x')
func = sympify(func_str.replace('^', '**'))
f_lambda = lambdify(x, func, 'numpy')

# Convert the limits to floats
a, b = float(sympify(a_str)), float(sympify(b_str))

# Calculate the integral
integral_result = simpson_3_8(f_lambda, a, b)

# Create a plot
fig, ax = plt.subplots()
X = np.linspace(a, b, 1000)
Y = f_lambda(X)
ax.plot(X, Y, label=f'f(x) = {func_str}')
ax.set_title(f"Integral aproximada por la Regla de Simpson 3/8: {integral_result:.4f}")
ax.legend()
plt.show()
