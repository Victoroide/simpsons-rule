import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from scipy.integrate import quad
from sympy import symbols, lambdify, sympify

def simpson_3_8(f_lambda, a, b, n=40):
    if n % 3 != 0:
        n += 3 - (n % 3)  # Adjust n to be a multiple of 3

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

        # Convert the function to a lambda expression
        x = symbols('x')
        func = sympify(func_str.replace('^', '**'))
        f_lambda = lambdify(x, func, 'numpy')

        # Convert the limits to floats
        a, b = float(sympify(a_str)), float(sympify(b_str))

        # Calculate the integral
        integral_result = simpson_3_8(f_lambda, a, b)

        # Calculate the exact integral
        integral_exacta, _ = quad(f_lambda, a, b)

        # Calculate the error
        error = abs(integral_exacta - integral_result)
        if error < 0.001:
            error_str = "{:.3e}".format(error)
        else:
            error_str = str(error)

        # Clear previous plots
        ax[0].clear()
        ax[1].clear()

        # Plot the function on both subplots
        X = np.linspace(a, b, 1000)
        Y = f_lambda(X)
        ax[0].plot(X, Y, label=f'f(x) = {func_str}')
        ax[1].plot(X, Y, label=f'f(x) = {func_str}')

        # Simpson's 3/8 rule approximation
        n = 40  # This should be a multiple of 3 for Simpson's 3/8 rule
        X_simpson = np.linspace(a, b, n + 1)
        Y_simpson = f_lambda(X_simpson)
        for i in range(0, n, 3):
            xi = X_simpson[i:i+4]
            yi = Y_simpson[i:i+4]
            ax[0].fill_between(xi, 0, yi, color='gray', alpha=0.5)

        # Set the titles for subplots
        ax[0].set_title(f"Integral aproximada: {integral_result:.4f}, Error: {error_str}")
        ax[1].set_title("Zoomed View")

        # Zoom in on an area with maximal difference
        # For this, we'll need to calculate the exact integral values on the Simpson's 3/8 x points
        Y_exact = [quad(f_lambda, X_simpson[i], X_simpson[i+1])[0] for i in range(n)]
        Y_diff = np.abs(Y_simpson[:n] - Y_exact)

        # Find the interval with the largest difference
        max_diff_idx = np.argmax(Y_diff)
        zoomed_a = X_simpson[max_diff_idx]
        zoomed_b = X_simpson[max_diff_idx + 1]

        # Plot the zoomed view on the second subplot
        X_zoomed = np.linspace(zoomed_a, zoomed_b, 500)
        Y_zoomed = f_lambda(X_zoomed)
        ax[1].plot(X_zoomed, Y_zoomed, label='Zoomed f(x)')

        # Highlight the difference area on the zoomed subplot
        ax[1].fill_between(X_zoomed, 0, Y_zoomed, color='orange', alpha=0.5)

        # Adding legends and draw both canvases
        ax[0].legend()
        ax[1].legend()
        canvas.draw()
    except Exception as e:
        print(e)

# Tikinter GUI
window = tk.Tk()
window.title("Integración por Regla de Simpson 3/8")
window.geometry("800x600")  

# Create the matplotlib figure with two subplots
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
canvas = FigureCanvasTkAgg(fig, master=window)

# Set up the GUI elements
font_size = 18  
entry_width = 15  # Width of the entry fields

entry_func = tk.Entry(window, font=('Arial', font_size), width=entry_width)
entry_a = tk.Entry(window, font=('Arial', font_size), width=entry_width)
entry_b = tk.Entry(window, font=('Arial', font_size), width=entry_width)

label_func = tk.Label(window, text="Función f(x):", font=('Arial', font_size))
label_a = tk.Label(window, text="Límite inferior a:", font=('Arial', font_size))
label_b = tk.Label(window, text="Límite superior b:", font=('Arial', font_size))

# Place the GUI elements on the screen
label_func.grid(row=0, column=0, sticky="w")
entry_func.grid(row=0, column=1, sticky="ew")
label_a.grid(row=1, column=0, sticky="w")
entry_a.grid(row=1, column=1, sticky="ew")
label_b.grid(row=2, column=0, sticky="w")
entry_b.grid(row=2, column=1, sticky="ew")
canvas.get_tk_widget().grid(row=3, column=0, columnspan=2, sticky="nsew")

# Set up the grid configuration
window.grid_rowconfigure(3, weight=1)
window.grid_columnconfigure(1, weight=1)

# Bind the entry fields to the update_graph function
entry_func.bind("<KeyRelease>", update_graph)
entry_a.bind("<KeyRelease>", update_graph)
entry_b.bind("<KeyRelease>", update_graph)

window.mainloop()
