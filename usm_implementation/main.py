import json
import time
import tkinter as tk

from methods.ids import perform_ids
from methods.dls import perform_dls
from methods.bidi import perform_bidi
from methods.bfs import perform_bfs
from methods.dfs import perform_dfs
from typing import Dict, Union, Set, List, Tuple

# The various data types used in this module
Vertex = Union[int, str]
Graph = Dict[Vertex, Set[Vertex]]
Path = List[Vertex]
VertexPositionMap = Dict[Vertex, Tuple[float, float]]
PathMap = Dict[Vertex, Union[Vertex, None]]

algo_index = 0

# Graph configurations
root = None
goal = None
depth_limit = 0
max_depth = 0
graph: Graph = {}
node_positions: VertexPositionMap = {}

# UI elements drawn on the graph
ui_elements: List[int] = [-1]

# Create the window
window = tk.Tk()
window.title("Breadth-first search GUI demo")

# Create the canvas
canvas = tk.Canvas(window, width=500, height=500)
canvas.pack()


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def draw_graph(graph: Graph) -> None:
    for node in graph:

        # Draw the edges to its neighbors
        for neighbor in graph[node]:
            draw_path([node, neighbor], "black", 1, "white")


def draw_path(path: Path, color: str, width: int, text_color: str = "black",) -> List[int]:
    if not path:
        return

    elements = []

    start = path[0]

    for i in range(1, len(path)):
        end = path[i]

        # Get the position of the start & end node
        x1, y1 = node_positions[start]
        X1, Y1 = x1, y1

        x2, y2 = node_positions[end]
        X2, Y2 = x2, y2

        if X1 < X2:
            X1, X2 = X1+20, X2-20
        elif X1 > X2:
            X1, X2 = X1-20, X2+20

        if Y1 < Y2:
            Y1, Y2 = Y1+20, Y2-20
        elif Y1 > Y2:
            Y1, Y2 = Y1-20, Y2+20

        # Draw the edge from the start to end
        id1 = canvas.create_line(X1, Y1, X2, Y2, arrow=tk.LAST,
                                 width=width, fill=color, capstyle=tk.ROUND)

        # Draw the nodes as circles
        id2 = canvas.create_oval(x1-20, y1-20, x1+20, y1+20, fill=color)
        id3 = canvas.create_text(x1, y1, text=start, fill=text_color)
        canvas.update()

        elements.extend([id1, id2, id3])

        start = end
    time.sleep(.3)

    # Get the position of the start node
    x1, y1 = node_positions[start]

    # Draw the node as a circle
    elements.append(canvas.create_oval(x1-20, y1-20, x1+20, y1+20, fill=color))
    elements.append(canvas.create_text(x1, y1, text=start, fill=text_color))

    return elements


def main(ui_elements: List):
    # Clear all UI elements
    for e in ui_elements:
        canvas.delete(e)

    ui_elements.clear()
    ui_elements.append(-1)

    time.sleep(.3)

    result = None

    if algo_index == 0:
        result = perform_dfs(
            root=root,
            goal=goal,
            graph=graph,
            draw_path=draw_path,
            ui_elements=ui_elements)

    elif algo_index == 1:
        result = perform_bfs(
            root=root,
            goal=goal,
            graph=graph,
            draw_path=draw_path,
            ui_elements=ui_elements)

    elif algo_index == 2:
        result = perform_dls(
            root=root,
            goal=goal,
            graph=graph,
            depth_limit=depth_limit,
            draw_path=draw_path,
            ui_elements=ui_elements)

    elif algo_index == 3:
        result = perform_ids(
            root=root,
            goal=goal,
            graph=graph,
            max_depth=max_depth,
            draw_path=draw_path,
            ui_elements=ui_elements)

    elif algo_index == 4:
        result = perform_bidi(
            root=root,
            goal=goal,
            graph=graph,
            draw_path=draw_path,
            ui_elements=ui_elements)

    elif algo_index == 5:
        pass

    else:
        raise("[INVALID CHOICE]")

    print(f"[PATH] {result}")


if __name__ == "__main__":
    # Get graph config from file
    graph_config = read_json_file(
        f"./usm_implementation\
/graph-config-v\
{int(input('[ENTER GRAPH INDEX] (1 - 2) > '))}\
.json")

    # Get root & goal vertices from user
    root = graph_config["root"]
    goal = graph_config["goal"]
    graph = graph_config["graph"]
    depth_limit = graph_config["depth_limit"]
    max_depth = graph_config["max_depth"]
    node_positions = graph_config["node_positions"]

    # Get the adjacency list for each vertex from user
    for v in graph:
        graph[v] = set(map(
            lambda e: e.strip(),
            graph[v]))

    # Draw the graph
    draw_graph(graph)

    # Create the button to start
    button = tk.Button(window, text="Start", command=lambda: main(ui_elements))
    button.pack()

    print(f"Searching from [{root}] to [{goal}]:\
\n[0] Depth-first Search (DFS)\
\n[1] Breadth-first Search (BFS)\
\n[2] Depth-limited Search (DLS)\
\n[3] Iterative Depening Search (IDS)\
\n[4] Bi-directional Search (BIDI)\
\n[5] Uniform-cost Search (UCS)\
\n[6] Quit\
\n\n----\n\n")

    while True:
        try:
            algo_index = int(input())

            if algo_index == 6:
                print("\n[PROCESS ENDED BY USER]")
                break

        except KeyboardInterrupt:
            print("\n[PROCESS ENDED BY USER]")
            break
        except:
            print("\n[AN UNKNOWN ERROR OCCURED]\n")
            continue
