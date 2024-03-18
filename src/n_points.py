import numpy as np
from tkinter import messagebox
import time

cache_n_point = {}

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
    num_segments = 2 ** (iteration - 1)
    num_points = num_segments * (len(control_points) - 1) + 1
    num_points = int(num_points)
    t_values = np.linspace(0, 1, num_points)
    curve_points = [de_casteljau(control_points, t) for t in t_values]
    return np.array(curve_points)


def parse_control_points_general(entry):
    try:
        points = entry.strip().split(';')
        control_points = [list(map(float, p.split(','))) for p in points if p.strip() != ""]
        if not control_points or any(len(p) != 2 for p in control_points):
            return None
        return control_points
    except ValueError:
        messagebox.showerror("Error", "Control points are invalid or not in expected format.")
        return None

def update_plot(entry_control_points, fig, canvas, iteration_slider):
    iteration = int(iteration_slider.get())
    control_points = parse_control_points_general(entry_control_points.get())
    if not control_points:
        return

    fig.clear()

    ax = fig.add_subplot(111)
    control_points_str = str(control_points)
    if control_points_str not in cache_n_point:
        cache_n_point[control_points_str] = {}
    
    if iteration == 0:
        points_dnc = np.array([control_points[0], control_points[-1]])
        dnc_time = 0
    else:
        if iteration not in cache_n_point[control_points_str]:
            start_time_dnc = time.perf_counter()
            points_dnc = bezier_general_dnc(control_points, iteration)
            dnc_time = time.perf_counter() - start_time_dnc
            cache_n_point[control_points_str][iteration] = {'points': points_dnc, 'time': dnc_time}
        else:
            points_dnc = cache_n_point[control_points_str][iteration]['points']
            dnc_time = cache_n_point[control_points_str][iteration]['time']
    
    ax.plot(points_dnc[:, 0], points_dnc[:, 1], 'go-', label=f"Divide & Conquer (Iter: {iteration})")
    ax.plot([p[0] for p in control_points], [p[1] for p in control_points], 'ro-', label="Control Points")
    ax.legend()
    ax.set_title(f"Divide & Conquer\nExecution Time: {dnc_time:.5f} sec")

    canvas.draw()


def visualize_with_max_iteration(entry_iteration, iteration_slider, entry_control_points, fig, canvas):
    try:
        max_iterations = int(entry_iteration.get())
    except ValueError:
        messagebox.showerror("Error", "Iteration must be an integer")
        return
    iteration_slider.config(to=max_iterations)
    iteration_slider.set(max_iterations)
    update_plot(entry_control_points, fig, canvas, iteration_slider)
