import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import time

cache_dnc = {}

def de_casteljau(control_points, t):
    n = len(control_points)
    if n == 1:
        return control_points[0]
    else:
        new_points = []
        for i in range(n - 1):
            new_point = (1 - t) * np.array(control_points[i]) + t * np.array(control_points[i + 1])
            new_points.append(new_point)
        return de_casteljau(new_points, t)

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
        return None

def update_plot(event=None):
    iteration = int(iteration_slider.get())
    control_points = parse_control_points_general(entry_control_points.get())
    if not control_points:
        return

    fig.clear()

    ax = fig.add_subplot(111)
    control_points_str = str(control_points)
    if control_points_str not in cache_dnc:
        cache_dnc[control_points_str] = {}
    if iteration not in cache_dnc[control_points_str]:
        start_time_dnc = time.perf_counter()
        points_dnc = bezier_general_dnc(control_points, iteration)
        dnc_time = time.perf_counter() - start_time_dnc
        cache_dnc[control_points_str][iteration] = {'points': points_dnc, 'time': dnc_time}
    else:
        points_dnc = cache_dnc[control_points_str][iteration]['points']
        dnc_time = cache_dnc[control_points_str][iteration]['time']
    ax.plot(points_dnc[:, 0], points_dnc[:, 1], 'go-', label=f"Divide & Conquer (Iter: {iteration})")
    ax.scatter(points_dnc[:, 0], points_dnc[:, 1], c='green', marker='o', s=50, linewidths=1.5)  # Atur ketebalan titik hijau di sini
    ax.plot([p[0] for p in control_points], [p[1] for p in control_points], 'ro-', label="Control Points")
    ax.legend()
    ax.set_title(f"Divide & Conquer\nExecution Time: {dnc_time:.5f} sec")

    canvas.draw()

def visualize_with_max_iteration():
    max_iterations = int(entry_iteration.get())  # Ambil nilai maksimum aktual dari entry_iteration
    iteration_slider.config(to=max_iterations)  # Setel nilai maksimum slider ke nilai maksimum aktual
    iteration_slider.set(max_iterations)  # Setel nilai slider ke nilai maksimum aktual
    update_plot()

# GUI Setup
root = tk.Tk()
root.title("Dynamic Bezier Curve Visualization")
root.geometry("1200x650")

fig = Figure(figsize=(12, 6), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
widget = canvas.get_tk_widget()
widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

input_frame = tk.Frame(root)
input_frame.pack(side=tk.TOP, fill=tk.X)  # Letakkan frame input di atas canvas

label_control_points = tk.Label(input_frame, text="Control Points (x1,y1;x2,y2;...):")
label_control_points.pack(side=tk.LEFT, padx=2)
entry_control_points = tk.Entry(input_frame, width=50)
entry_control_points.pack(side=tk.LEFT, padx=2)
entry_control_points.insert(0, "")

label_iteration = tk.Label(input_frame, text="Iteration:")
label_iteration.pack(side=tk.LEFT, padx=2)
entry_iteration = tk.Entry(input_frame)
entry_iteration.pack(side=tk.LEFT, padx=2)
entry_iteration.insert(0, "0")

button_visualize = tk.Button(input_frame, text="Visualize Bezier Curve", command=visualize_with_max_iteration)
button_visualize.pack(side=tk.LEFT, padx=4)

iteration_slider_label = tk.Label(input_frame, text="Iteration:")
iteration_slider_label.pack(side=tk.LEFT, padx=5)

iteration_slider = ttk.Scale(input_frame, from_=0, to=5, orient='horizontal', command=update_plot)
iteration_slider.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
iteration_slider.set(0)

root.mainloop()
