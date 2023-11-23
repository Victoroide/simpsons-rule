import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
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

def update_graph(*args):
    try:
        func_str = entry_func.get()
        a_str = entry_a.get()
        b_str = entry_b.get()

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

        # Actualizar la gráfica
        ax.clear()
        X = np.linspace(a, b, 1000)
        Y = f_lambda(X)
        ax.plot(X, Y, label=f'f(x) = {func_str}')
        ax.set_title(f"Integral aproximada por la Regla de Simpson 3/8: {integral_result:.4f}, Error: {error_str}")
        ax.legend()
        canvas.draw()
    except Exception as e:
        print(e)

# Configuración de la ventana de Tkinter
window = tk.Tk()
window.title("Integración por Regla de Simpson 3/8")
window.geometry("800x600")  # Tamaño inicial de la ventana

# Crear figura y ejes para la gráfica
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=window)

# Configuración de las cajas de texto y etiquetas
font_size = 18  # Tamaño de la fuente
entry_width = 15  # Ancho de las cajas de texto

entry_func = tk.Entry(window, font=('Arial', font_size), width=entry_width)
entry_a = tk.Entry(window, font=('Arial', font_size), width=entry_width)
entry_b = tk.Entry(window, font=('Arial', font_size), width=entry_width)

label_func = tk.Label(window, text="Función f(x):", font=('Arial', font_size))
label_a = tk.Label(window, text="Límite inferior a:", font=('Arial', font_size))
label_b = tk.Label(window, text="Límite superior b:", font=('Arial', font_size))

# Posicionar los elementos en la ventana
label_func.grid(row=0, column=0, sticky="w")
entry_func.grid(row=0, column=1, sticky="ew")
label_a.grid(row=1, column=0, sticky="w")
entry_a.grid(row=1, column=1, sticky="ew")
label_b.grid(row=2, column=0, sticky="w")
entry_b.grid(row=2, column=1, sticky="ew")
canvas.get_tk_widget().grid(row=3, column=0, columnspan=2, sticky="nsew")

# Configurar el redimensionamiento
window.grid_rowconfigure(3, weight=1)
window.grid_columnconfigure(1, weight=1)

# Enlazar cambios en los campos de entrada a la función de actualización
entry_func.bind("<KeyRelease>", update_graph)
entry_a.bind("<KeyRelease>", update_graph)
entry_b.bind("<KeyRelease>", update_graph)

# Ejecutar la aplicación
window.mainloop()
