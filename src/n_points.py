import numpy as np
import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import math

def bezier_general_brute_force(control_points, iteration):
    num_points = 2 ** iteration + 1
    t_values = np.linspace(0, 1, num_points)
    n = len(control_points) - 1
    curve_points = []
    for t in t_values:
        point = np.zeros(2)
        for i, P in enumerate(control_points):
            bernstein_poly = (math.factorial(n) / (math.factorial(i) * math.factorial(n - i))) * (t ** i) * ((1 - t) ** (n - i))
            point += np.array(P) * bernstein_poly
        curve_points.append(point)
    return np.array(curve_points)

def de_casteljau(control_points, t):
    points_tuple = tuple(map(tuple, control_points))
    if len(points_tuple) > 1:
        new_points = []
        for i in range(len(points_tuple)-1):
            new_point = (1 - t) * np.array(points_tuple[i]) + t * np.array(points_tuple[i+1])
            new_points.append(new_point)
        return de_casteljau(new_points, t)
    return points_tuple[0]

def bezier_general_dnc(control_points, iteration):
    num_points = 2 ** iteration + 1
    t_values = np.linspace(0, 1, num_points)
    curve_points = [de_casteljau(control_points, t) for t in t_values]
    return np.array(curve_points)

def parse_control_points_general(entry):
    try:
        points = entry.strip().split(';')
        control_points = [list(map(float, p.split(','))) for p in points]
        return control_points
    except ValueError:
        messagebox.showerror("Input Error", "Please enter points in the correct format.")
        return None

def visualize():
    control_points = parse_control_points_general(entry_control_points.get())
    if not control_points:
        return
    
    iteration = int(entry_iteration.get())

    start_time = time.time()
    points_brute_force = bezier_general_brute_force(control_points, iteration)
    time_brute_force = time.time() - start_time

    start_time = time.time()
    points_dnc = bezier_general_dnc(control_points, iteration)
    time_dnc = time.time() - start_time

    fig.clear()

    ax1 = fig.add_subplot(121)
    ax1.plot(points_brute_force[:, 0], points_brute_force[:, 1], 'b-', label="Brute Force")
    ax1.scatter(points_brute_force[:, 0], points_brute_force[:, 1], c='blue', marker='o', s=10)
    ax1.plot([p[0] for p in control_points], [p[1] for p in control_points], 'ro-', label="Control Points")
    ax1.legend()
    ax1.set_title(f"Brute Force\nExecution Time: {time_brute_force:.5f} sec")

    ax2 = fig.add_subplot(122)
    ax2.plot(points_dnc[:, 0], points_dnc[:, 1], 'g-', label="Divide & Conquer")
    ax2.scatter(points_dnc[:, 0], points_dnc[:, 1], c='green', marker='o', s=10)
    ax2.plot([p[0] for p in control_points], [p[1] for p in control_points], 'ro-', label="Control Points")
    ax2.legend()
    ax2.set_title(f"Divide & Conquer\nExecution Time: {time_dnc:.5f} sec")

    canvas.draw()

# GUI Setup
root = tk.Tk()
root.title("Dynamic Bezier Curve Visualization")
root.geometry("1200x600")

fig = Figure(figsize=(12, 6), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
widget = canvas.get_tk_widget()
widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

label_control_points = tk.Label(root, text="Control Points (x1,y1;x2,y2;...):")
label_control_points.pack(side=tk.TOP, pady=2)
entry_control_points = tk.Entry(root, width=50)
entry_control_points.pack(side=tk.TOP, pady=2)

label_iteration = tk.Label(root, text="Iteration:")
label_iteration.pack(side=tk.TOP, pady=2)
entry_iteration = tk.Entry(root)
entry_iteration.pack(side=tk.TOP, pady=2)
entry_iteration.insert(0, "5")  # Default iteration value

button_visualize = tk.Button(root, text="Visualize Bezier Curve", command=visualize)
button_visualize.pack(side=tk.TOP, pady=4)

root.mainloop()
