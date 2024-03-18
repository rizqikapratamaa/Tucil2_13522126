import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import three_points, n_points


def setup_three_points_tab(tab):
    fig = Figure(figsize=(12, 6), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=tab)
    widget = canvas.get_tk_widget()
    widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    controls_frame = tk.Frame(tab)
    controls_frame.pack(side=tk.TOP, fill=tk.X)

    label_P0 = tk.Label(controls_frame, text="P0 (x,y):")
    label_P0.pack(side=tk.LEFT, padx=5)
    entry_P0 = tk.Entry(controls_frame)
    entry_P0.pack(side=tk.LEFT, padx=5)
    entry_P0.insert(0, "")

    label_P1 = tk.Label(controls_frame, text="P1 (x,y):")
    label_P1.pack(side=tk.LEFT, padx=5)
    entry_P1 = tk.Entry(controls_frame)
    entry_P1.pack(side=tk.LEFT, padx=5)
    entry_P1.insert(0, "")

    label_P2 = tk.Label(controls_frame, text="P2 (x,y):")
    label_P2.pack(side=tk.LEFT, padx=5)
    entry_P2 = tk.Entry(controls_frame)
    entry_P2.pack(side=tk.LEFT, padx=5)
    entry_P2.insert(0, "")

    label_max_iterations = tk.Label(controls_frame, text="No of Iterations:")
    label_max_iterations.pack(side=tk.LEFT, padx=5)

    entry_max_iterations = tk.Entry(controls_frame, width=5)
    entry_max_iterations.pack(side=tk.LEFT, padx=5)
    entry_max_iterations.insert(0, "0")

    button_init = tk.Button(controls_frame, text="Visualize", command=lambda: three_points.initialize_visualization(fig, canvas, iteration_slider, entry_max_iterations, entry_P0, entry_P1, entry_P2))
    button_init.pack(side=tk.LEFT, padx=5)

    iteration_slider_label = tk.Label(controls_frame, text="Iteration:")
    iteration_slider_label.pack(side=tk.LEFT, padx=5)

    iteration_slider = ttk.Scale(controls_frame, from_=0, to=5, orient='horizontal', command=lambda event=None: three_points.update_plot(fig, canvas, iteration_slider, entry_P0, entry_P1, entry_P2))
    iteration_slider.pack(side=tk.LEFT, padx=5, fill='x', expand=True)
    iteration_slider.set(0)

    pass

def setup_n_points_tab(tab):
    fig = Figure(figsize=(12, 6), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=tab)
    widget = canvas.get_tk_widget()
    widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    input_frame = tk.Frame(tab)
    input_frame.pack(side=tk.TOP, fill=tk.X)

    label_control_points = tk.Label(input_frame, text="Control Points (x1,y1;x2,y2;...):")
    label_control_points.pack(side=tk.LEFT, padx=2)
    entry_control_points = tk.Entry(input_frame, width=50)
    entry_control_points.pack(side=tk.LEFT, padx=2)
    entry_control_points.insert(0, "")

    label_iteration = tk.Label(input_frame, text="No of Iteration:")
    label_iteration.pack(side=tk.LEFT, padx=2)
    entry_iteration = tk.Entry(input_frame)
    entry_iteration.pack(side=tk.LEFT, padx=2)
    entry_iteration.insert(0, "0")


    button_visualize = tk.Button(input_frame, text="Visualize", command=lambda: n_points.visualize_with_max_iteration(entry_iteration, iteration_slider, entry_control_points, fig, canvas))
    button_visualize.pack(side=tk.LEFT, padx=4)

    iteration_slider_label = tk.Label(input_frame, text="Iteration:")
    iteration_slider_label.pack(side=tk.LEFT, padx=5)

    iteration_slider = ttk.Scale(input_frame, from_=0, to=5, orient='horizontal', command=lambda event=None: n_points.update_plot(entry_control_points, fig, canvas, iteration_slider))
    iteration_slider.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    iteration_slider.set(0)
    pass

def main():
    root = tk.Tk()
    root.title("BJier: Bezier Curve Visualization")

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    tab_three_points = ttk.Frame(notebook)
    tab_n_points = ttk.Frame(notebook)

    notebook.add(tab_three_points, text='Three Points')
    notebook.add(tab_n_points, text='N Points')

    setup_three_points_tab(tab_three_points)
    setup_n_points_tab(tab_n_points)

    root.mainloop()

if __name__ == "__main__":
    main()
