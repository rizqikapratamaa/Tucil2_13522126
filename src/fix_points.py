import numpy as np
import tkinter as tk
from tkinter import messagebox, ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Cache untuk kedua metode
cache_brute_force = {}
cache_dnc = {}

def calculate_num_points(iteration):
    return 2 ** (iteration + 1) - 1

def bezier_quadratic_brute_force(P0, P1, P2, iteration):
    P0, P1, P2 = np.array(P0), np.array(P1), np.array(P2)  # Pastikan ini numpy arrays
    if iteration == 0:
        # Untuk iterasi = 0, hanya menghitung dan menampilkan garis antara titik tengah
        Q0 = (P0 + P1) / 2.0
        Q1 = (P1 + P2) / 2.0
        return np.array([Q0, Q1])
    
    if iteration in cache_brute_force:
        return cache_brute_force[iteration]
    
    num_points = calculate_num_points(iteration)
    t_values = np.linspace(0, 1, num_points)
    curve_points = []
    for t in t_values:
        x = (1 - t)**2 * P0[0] + 2 * (1 - t) * t * P1[0] + t**2 * P2[0]
        y = (1 - t)**2 * P0[1] + 2 * (1 - t) * t * P1[1] + t**2 * P2[1]
        curve_points.append([x, y])
    curve_points = np.array(curve_points)
    cache_brute_force[iteration] = curve_points
    return curve_points

def bezier_quadratic_divide_and_conquer(P0, P1, P2, iteration):
    P0, P1, P2 = np.array(P0), np.array(P1), np.array(P2)
    if iteration == 0:
        Q0 = (P0 + P1) / 2.0
        Q1 = (P1 + P2) / 2.0
        return np.array([Q0, Q1])

    if iteration in cache_dnc:
        return cache_dnc[iteration]

    def divide(P0, P1, P2, iteration):
        if iteration <= 0:
            return [P0, P2]
        Q0 = (P0 + P1) / 2.0
        Q1 = (P1 + P2) / 2.0
        R0 = (Q0 + Q1) / 2.0
        left = divide(P0, Q0, R0, iteration - 1)[:-1]
        right = divide(R0, Q1, P2, iteration - 1)
        return left + right

    P0, P1, P2 = np.array(P0), np.array(P1), np.array(P2)
    points = np.array(divide(P0, P1, P2, iteration))
    cache_dnc[iteration] = points
    return points

def parse_control_points(entry):
    try:
        x, y = map(float, entry.strip().split(','))
        return [x, y]
    except ValueError:
        messagebox.showerror("Input Error", "Please enter 2 numbers separated by a comma.")
        return None

def update_plot(event=None):
    global iteration_slider, entry_P0, entry_P1, entry_P2
    iteration = int(iteration_slider.get())
    P0 = parse_control_points(entry_P0.get())
    P1 = parse_control_points(entry_P1.get())
    P2 = parse_control_points(entry_P2.get())
    if None in (P0, P1, P2):
        return

    points_brute_force = bezier_quadratic_brute_force(P0, P1, P2, iteration)
    points_dnc = bezier_quadratic_divide_and_conquer(P0, P1, P2, iteration)

    fig.clear()

    # Plot for Brute Force
    ax1 = fig.add_subplot(121)
    ax1.plot(points_brute_force[:, 0], points_brute_force[:, 1], 'g-', label=f"Brute Force (Iter: {iteration})")
    ax1.plot([P0[0], P1[0], P2[0]], [P0[1], P1[1], P2[1]], 'ro-', label="Control Points")
    ax1.legend()
    ax1.set_title("Brute Force")

    # Plot for Divide and Conquer
    ax2 = fig.add_subplot(122)
    ax2.plot(points_dnc[:, 0], points_dnc[:, 1], 'b-', label=f"Divide & Conquer (Iter: {iteration})")
    ax2.plot([P0[0], P1[0], P2[0]], [P0[1], P1[1], P2[1]], 'ro-', label="Control Points")
    ax2.legend()
    ax2.set_title("Divide & Conquer")

    canvas.draw()

def initialize_visualization():
    global iteration_slider, entry_max_iterations
    max_iterations = int(entry_max_iterations.get())
    iteration_slider.config(to=max_iterations)
    iteration_slider.set(max_iterations)
    update_plot()

# GUI setup
root = tk.Tk()
root.title("Bezier Curve Comparison with Iteration Control")

fig = Figure(figsize=(12, 6), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
widget = canvas.get_tk_widget()
widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

controls_frame = tk.Frame(root)
controls_frame.pack(side=tk.TOP, fill=tk.X)

entry_P0 = tk.Entry(controls_frame)
entry_P0.pack(side=tk.LEFT)
entry_P0.insert(0, "0,0")

entry_P1 = tk.Entry(controls_frame)
entry_P1.pack(side=tk.LEFT)
entry_P1.insert(0, "1,2")

entry_P2 = tk.Entry(controls_frame)
entry_P2.pack(side=tk.LEFT)
entry_P2.insert(0, "2,0")

label_max_iterations = tk.Label(controls_frame, text="Max Iterations:")
label_max_iterations.pack(side=tk.LEFT)

entry_max_iterations = tk.Entry(controls_frame, width=5)
entry_max_iterations.pack(side=tk.LEFT)
entry_max_iterations.insert(0, "5")

button_init = tk.Button(controls_frame, text="Visualize", command=initialize_visualization)
button_init.pack(side=tk.LEFT, padx=5)

iteration_slider_label = tk.Label(controls_frame, text="Iteration:")
iteration_slider_label.pack(side=tk.LEFT, padx=(10, 2))

iteration_slider = ttk.Scale(controls_frame, from_=0, to=5, orient='horizontal', command=update_plot)
iteration_slider.pack(side=tk.LEFT, fill='x', expand=True)
iteration_slider.set(0)

root.mainloop()
