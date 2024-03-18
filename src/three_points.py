import numpy as np
from tkinter import messagebox
import time

cache_brute_force = {}
cache_dnc = {}

def calculate_num_points(iteration):
    return 2 ** (iteration) + 1

def bezier_quadratic_brute_force(P0, P1, P2, iteration):
    P0, P1, P2 = np.array(P0), np.array(P1), np.array(P2)
    for _ in range (10):
        num_points = calculate_num_points(iteration)
        t_values = np.linspace(0, 1, num_points)
        curve_points = []
        for t in t_values:
            x = (1 - t)**2 * P0[0] + 2 * (1 - t) * t * P1[0] + t**2 * P2[0]
            y = (1 - t)**2 * P0[1] + 2 * (1 - t) * t * P1[1] + t**2 * P2[1]
            curve_points.append([x, y])
        curve_points = np.array(curve_points)
    return curve_points

import time

def bezier_quadratic_divide_and_conquer(P0, P1, P2, iteration):
    P0, P1, P2 = np.array(P0), np.array(P1), np.array(P2)
    if iteration == 0:
        return np.array([P0, P2])
    else:
        P01 = (P0 + P1) / 2
        P12 = (P1 + P2) / 2
        P0112 = (P01 + P12) / 2
        left_points = bezier_quadratic_divide_and_conquer(P0, P01, P0112, iteration - 1)
        right_points = bezier_quadratic_divide_and_conquer(P0112, P12, P2, iteration - 1)
        return np.concatenate((left_points, right_points))

def parse_control_points(entry):
    if not entry.strip():
        return None
    try:
        x, y = map(float, entry.strip().split(','))
        return [x, y]
    except ValueError:
        messagebox.showerror("Error", "Control points are invalid or not in expected format.")
        return None

def update_plot(fig, canvas, iteration_slider, entry_P0, entry_P1, entry_P2):
    iteration = int(iteration_slider.get())
    P0 = parse_control_points(entry_P0.get())
    P1 = parse_control_points(entry_P1.get())
    P2 = parse_control_points(entry_P2.get())
    if None in (P0, P1, P2):
        return

    fig.clear()

    ax1 = fig.add_subplot(121)
    if iteration not in cache_brute_force:
        start_time_brute_force = time.perf_counter()
        points_brute_force = bezier_quadratic_brute_force(P0, P1, P2, iteration)
        brute_force_time = time.perf_counter() - start_time_brute_force
        cache_brute_force[iteration] = {'points': points_brute_force, 'time': brute_force_time}
    else:
        points_brute_force = cache_brute_force[iteration]['points']
        brute_force_time = cache_brute_force[iteration]['time']
    ax1.plot(points_brute_force[:, 0], points_brute_force[:, 1], 'go-', label=f"Brute Force (Iter: {iteration})")
    ax1.plot([P0[0], P1[0], P2[0]], [P0[1], P1[1], P2[1]], 'ro-', label="Control Points")  
    ax1.legend()
    ax1.set_title(f"Brute Force\nExecution Time: {brute_force_time:.6f} sec")

    ax2 = fig.add_subplot(122)
    if iteration not in cache_dnc:
        start_time_dnc = time.perf_counter()
        points_dnc = bezier_quadratic_divide_and_conquer(P0, P1, P2, iteration)
        dnc_time = time.perf_counter() - start_time_dnc
        cache_dnc[iteration] = {'points': points_dnc, 'time': dnc_time}
    else:
        points_dnc = cache_dnc[iteration]['points']
        dnc_time = cache_dnc[iteration]['time']
    ax2.plot(points_dnc[:, 0], points_dnc[:, 1], 'bo-', label=f"Divide & Conquer (Iter: {iteration})")
    ax2.plot([P0[0], P1[0], P2[0]], [P0[1], P1[1], P2[1]], 'ro-', label="Control Points")  
    ax2.legend()
    ax2.set_title(f"Divide & Conquer\nExecution Time: {dnc_time:.6f} sec")

    canvas.draw()

def initialize_visualization(fig, canvas, iteration_slider, entry_max_iterations, entry_P0, entry_P1, entry_P2):
    global cache_brute_force, cache_dnc
    try:
        max_iterations = int(entry_max_iterations.get())
    except ValueError:
        messagebox.showerror("Error", "Iteration must be an integer")
        return
    iteration_slider.config(to=max_iterations)
    iteration_slider.set(max_iterations)
    cache_brute_force = {}
    cache_dnc = {}
    update_plot(fig, canvas, iteration_slider, entry_P0, entry_P1, entry_P2)
