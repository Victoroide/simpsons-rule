# Numerical Integration with Simpson's 3/8 Rule

This project implements Simpson's 3/8 Rule for numerical integration of functions in Python, providing a Graphical User Interface (GUI) for easy interaction.

## Features

- **Integral Calculation**: Uses Simpson's 3/8 Rule to calculate definite integrals.
- **Graphical User Interface**: Intuitive interface for entering functions and integration limits.
- **Result Visualization**: Graphically displays the function in real-time.
- **Error Estimation**: Calculates and displays the error in the integral approximation in real-time.

## Getting Started

### Prerequisites

Ensure you have Python 3.x installed on your system. Additionally, you will need the following libraries:

- NumPy
- Matplotlib
- SciPy
- SymPy

### Create a virtual enviroment:
python -m venv "simpson-rule-venv"                                                                                                            
### Once you got a venv, you can install these libraries using pip:
pip install -r requirements.txt

### To generate the executable:
pyinstaller --noconsole main.py

You can find it here: ./dist/main/main.exe