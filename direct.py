import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from scipy.spatial import ConvexHull
import math

vertices = []

# Distance between two points
def calculate_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)





def calculate_area(vertices):
    x, y = zip(*vertices)
    return 0.5 * abs(sum(x[i] * y[(i+1) % len(vertices)] - x[(i+1) % len(vertices)] * y[i] for i in range(len(vertices))))

def calculate_perimeter(vertices):
    return sum(calculate_distance(vertices[i], vertices[(i+1) % len(vertices)]) for i in range(len(vertices)))

def calculate_inradius(vertices):
    area = calculate_area(vertices)
    perimeter = calculate_perimeter(vertices)
    if perimeter <= 0 or area <= 0:
        return 0
    return 2 * area / perimeter

def calculate_incenter(vertices):
    cx, cy = 0, 0
    perimeter = calculate_perimeter(vertices)
    if perimeter <= 0:
        return (0, 0)

    for i in range(len(vertices)):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i+1) % len(vertices)]
        edge_length = calculate_distance((x1, y1), (x2, y2))
        cx += (x1 + x2) * edge_length
        cy += (y1 + y2) * edge_length

    cx /= (2 * perimeter)
    cy /= (2 * perimeter)
    return (cx, cy)

def calculate_circumcircle(vertices):
    max_distance = 0
    p1, p2 = None, None

    # Find the furthest pair of points (diameter of convex polygon)
    for i in range(len(vertices)):
        for j in range(i+1, len(vertices)):
            dist = calculate_distance(vertices[i], vertices[j])
            if dist > max_distance:
                max_distance = dist
                p1, p2 = vertices[i], vertices[j]

    circumcenter = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    circumradius = max_distance / 2

    return circumcenter, circumradius












# GUI handlers
def add_vertex():
    vertices.append((float(x_entry.get()), float(y_entry.get())))
    update_vertex_list()
    x_entry.delete(0, tk.END)
    y_entry.delete(0, tk.END)

def update_vertex_list():
    vertex_list.delete(0, tk.END)
    for v in vertices:
        vertex_list.insert(tk.END, f"({v[0]}, {v[1]})")

def clear_vertices():
    vertices.clear()
    update_vertex_list()
    result_label.config(text="")

def calculate_and_draw():
    if len(vertices) < 3:
        result_label.config(text="A polygon must have at least 3 vertices.")
        return

    points = np.array(vertices)

    # Calculate convex hull to ensure only outermost points form polygon
    hull = ConvexHull(points)
    hull_vertices = points[hull.vertices]

    # Close polygon for plotting
    hull_vertices_closed = np.vstack([hull_vertices, hull_vertices[0]])

    # Geometry calculations based on convex hull vertices
    area = calculate_area(hull_vertices)
    perimeter = calculate_perimeter(hull_vertices)
    inradius = calculate_inradius(hull_vertices)
    incenter = calculate_incenter(hull_vertices)
    circumcenter, circumradius = calculate_circumcircle(hull_vertices)

    # Display properties in Tkinter window
    result_label.config(text=f"Convex Hull Area: {area:.6f}\n"
                             f"Convex Hull Perimeter: {perimeter:.6f}\n"
                             f"Inradius: {inradius:.6f}\n"
                             f"Incenter: ({incenter[0]:.2f}, {incenter[1]:.2f})\n"
                             f"Circumradius: {circumradius:.6f}\n"
                             f"Circumcenter: ({circumcenter[0]:.2f}, {circumcenter[1]:.2f})")

    # Plot the convex polygon with incircle and circumcircle
    plt.figure()

    # Plot all points
    plt.scatter(points[:, 0], points[:, 1], color='blue', label='All Points')

    # Convex hull boundary
    plt.plot(hull_vertices_closed[:, 0], hull_vertices_closed[:, 1], 'r-', linewidth=2, label='Convex Hull')

    # Incircle (green)
    incircle = patches.Circle(incenter, inradius, fill=None, edgecolor='green', linewidth=1.5, label='Incircle')
    plt.gca().add_patch(incircle)

    # Circumcircle (red dashed)
    circumcircle = patches.Circle(circumcenter, circumradius, fill=None, edgecolor='red', linestyle='--', linewidth=1.5, label='Circumcircle')
    plt.gca().add_patch(circumcircle)

    # Mark incenter and circumcenter
    plt.scatter(*incenter, color='green', marker='x', s=100, label='Incenter')
    plt.scatter(*circumcenter, color='red', marker='x', s=100, label='Circumcenter')

    # Label convex hull vertices
    for x, y in hull_vertices:
        plt.text(x, y, f'({x},{y})', fontsize=8, ha='right')

    plt.axis('equal')
    plt.grid(True)
    plt.legend()
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.title('Convex Hull Polygon with Incircle and Circumcircle')
    plt.show()

# GUI Setup
app = tk.Tk()
app.title("Convex Hull Polygon Calculator")

tk.Label(app, text="X-coordinate:").pack()
x_entry = tk.Entry(app)
x_entry.pack()

tk.Label(app, text="Y-coordinate:").pack()
y_entry = tk.Entry(app)
y_entry.pack()

tk.Button(app, text="Add Vertex", command=add_vertex).pack()

vertex_list = tk.Listbox(app, height=8, width=40)
vertex_list.pack()

tk.Button(app, text="Calculate & Draw", command=calculate_and_draw).pack()
tk.Button(app, text="Clear Vertices", command=clear_vertices).pack()

result_label = tk.Label(app, text="", justify='left')
result_label.pack()

app.mainloop()
