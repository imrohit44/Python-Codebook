'''
# GUI Mathematical Function Plotter

This program uses Tkinter to create a graphical user interface (GUI) and Matplotlib to plot mathematical functions. The user can type a Python-compatible mathematical expression (using x), and the application will render the corresponding graph.

**Concepts:**  

GUI programming, event handling, data visualization.

**How to Run**

**1. Save the code and execute it:**

```
python Program_4.py
```
'''


import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_function():
    """Plots the mathematical function entered by the user."""
    expression = entry.get()
    try:
        # Generate x values
        x = np.linspace(-10, 10, 400)
        
        # Safely evaluate the expression
        # IMPORTANT: eval() can be dangerous with untrusted input.
        # Here, it's used in a controlled environment.
        y = eval(expression, {"np": np, "x": x})
        
        # Clear the previous plot
        ax.clear()
        
        # Plot the new function
        ax.plot(x, y)
        ax.set_title(f"Plot of y = {expression}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True)
        
        # Redraw the canvas
        canvas.draw()
    except Exception as e:
        messagebox.showerror("Invalid Expression", f"Error: {e}\nPlease enter a valid Python expression using 'x'.\nExamples: x**2, np.sin(x), x**3 - 2*x")

# --- GUI Setup ---
# Create the main window
root = tk.Tk()
root.title("Mathematical Function Plotter")

# Create a Matplotlib figure and axis
fig, ax = plt.subplots()

# Create a canvas to embed the plot in Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Create a frame for user input
input_frame = tk.Frame(root)
input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

# Create a label and entry widget
label = tk.Label(input_frame, text="Enter a function of x (e.g., np.cos(x)):")
label.pack(side=tk.LEFT)
entry = tk.Entry(input_frame, width=40)
entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
entry.bind("<Return>", lambda event: plot_function()) # Plot on Enter key

# Create a plot button
plot_button = tk.Button(input_frame, text="Plot", command=plot_function)
plot_button.pack(side=tk.LEFT, padx=5)

# Start the GUI event loop
root.mainloop()