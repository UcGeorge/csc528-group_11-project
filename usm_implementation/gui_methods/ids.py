"""
Iterative Deepening Search:
The iterative deepening search algorithm is a variant of the depth-first search 
algorithm that systematically increases the maximum depth limit on each iteration 
until a solution is found. It starts by limiting the maximum depth to 1 and 
performs a depth-limited search. If the goal vertex is not found at that depth 
limit, the algorithm increases the maximum depth limit by 1 and performs another 
depth-limited search until the goal vertex is found.

The iterative deepening search algorithm maintains a stack of vertices to be explored, 
similar to the depth-first search algorithm. When a vertex is explored, it is removed 
from the stack, and its neighboring vertices are added to the stack if they have not 
already been visited and the maximum depth limit has not been reached.

The search continues until the goal vertex is found, or the maximum depth limit is reached. 
The iterative deepening search algorithm ensures that all nodes at a given depth 
limit are explored before increasing the depth limit, guaranteeing that the solution 
found is the shortest possible path.
"""

import json
import time
import tkinter as tk
from typing import Dict, Union, Set, List, Tuple

# The various data types used in this module
Vertex = Union[int, str]
Graph = Dict[Vertex, Set[Vertex]]
Path = List[Vertex]
VertexPositionMap = Dict[Vertex, Tuple[float, float]]
PathMap = Dict[Vertex, Union[Vertex, None]]
DepthMap = Dict[Vertex, int]

# Graph data structure
graph: Graph = {}

# Positions of the nodes on the canvas
node_positions: VertexPositionMap = {}

# Create the window
window = tk.Tk()
window.title("Iterative deepening search GUI demo")

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


def draw_path(path: Path, color: str, width: int, text_color: str = "black",) -> None:
    if not path:
        return

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
        canvas.create_line(X1, Y1, X2, Y2, arrow=tk.LAST,
                           width=width, fill=color, capstyle=tk.ROUND)

        # Draw the nodes as circles
        canvas.create_oval(x1-20, y1-20, x1+20, y1+20, fill=color)
        canvas.create_text(x1, y1, text=start, fill=text_color)
        canvas.update()

        start = end
        time.sleep(.3)

    # Get the position of the start node
    x1, y1 = node_positions[start]

    # Draw the node as a circle
    canvas.create_oval(x1-20, y1-20, x1+20, y1+20, fill=color)
    canvas.create_text(x1, y1, text=start, fill=text_color)


def _compose_path(v: Vertex, paths: PathMap) -> Path:
    """
    Composes a path from the root node to a given vertex.

    Args:
    - v (Vertex): The vertex to start the path from.
    - paths (PathMap): A map that maps vertices to their direct parents after a DLS is performed.

    Returns:
        Path: A list of vertices that represents the path from the root to the goal.
    """
    path: Path = [v]

    while paths[v]:
        path.insert(0, paths[v])
        v = paths[v]

    return path


def _perform_dls(root: Vertex, goal: Vertex, graph: Graph, depth_limit: int) -> Path:
    """
    This function performs a depth-limited search on a graph starting from a given root 
    and finds a path from the root to a given goal node. It returns a set of vertices in the path.

    Args:
    - root (Vertex): A Vertex representing the starting vertex of the search.
    - goal (Vertex): A Vertex representing the goal vertex to be reached.
    - graph (Graph): A Graph representing the graph search space represented as an adjacency list.
    - depth_limit (int): An integer representing the maximum depth the algorithm can search.

    Returns:
        A list of vertices representing the path from the root to the goal vertex, if a path exists. 
        If no path is found, an empty set is returned.
    """
    stack: List[Vertex] = list([root])
    visited: Set[Vertex] = set()
    paths: PathMap = {v: None for v in graph}
    depths: DepthMap = {v: -1 for v in graph}

    # The depth of the root node is 0
    depths[root] = 0

    while stack:
        # Remove Vertex from the stack
        vertex = stack.pop(-1)

        # This Vertex has not been explored
        if vertex not in visited:
            # Add Vertex to the list of visited vertices
            visited.add(vertex)

            node_path = _compose_path(vertex, paths)

            # Draw the path
            draw_path(node_path, color="orange", width=4)

            # Vertex is the goal
            if vertex == goal:
                # Draw the path
                draw_path(node_path, color="green", width=8)

                # Return the path to the vertex
                return _compose_path(vertex, paths)

            # Vertex is at the depth limit
            if depths[vertex] >= depth_limit:
                continue

            # Add all adjacent vertices that have not been visited to stack
            adjacent_vertices = graph[vertex] - visited - set(stack)
            stack.extend(adjacent_vertices)

            for v in adjacent_vertices:
                paths[v] = vertex
                depths[v] = depths[vertex] + 1

    return set()


def _perform_ids(root: Vertex, goal: Vertex, graph: Graph, max_depth: int) -> Path:
    """
    This function performs an iterative deepening search on a graph starting from a given root 
    and finds a path from the root to a given goal node. It returns a set of vertices in the path.

    Args:
    - root (Vertex): A Vertex representing the starting vertex of the search.
    - goal (Vertex): A Vertex representing the goal vertex to be reached.
    - graph (Graph): A Graph representing the graph search space represented as an adjacency list.
    - max_depth (int): An integer representing the maximum depth the algorithm can search.

    Returns:
        A list of vertices representing the path from the root to the goal vertex, if a path exists. 
        If no path is found, an empty set is returned.
    """
    # Loop until the max depth is reached or the path is found
    for i in range(max_depth):
        # Perform DLS at depth i
        path = _perform_dls(root, goal, graph, i+1)

        # If path is found, return the path
        if path:
            return path


if __name__ == "__main__":
    print("\n_-_-_-_-_-_-_-_-_-_-_-_-_-_RUNNING IDS USM SEARCH_-_-_-_-_-_-_-_-_-_-_-_-_-_\n")

    # Get graph config from file
    graph_config = read_json_file("./usm_implementation/graph-config-v2.json")

    # Get root & goal vertices from user
    root = graph_config["root"]
    goal = graph_config["goal"]
    graph = graph_config["graph"]
    max_depth = graph_config["max_depth"]

    # Get the adjacency list for each vertex from user
    for v in graph:
        node_positions[v] = tuple(map(
            lambda e: float(e),
            graph_config["node_positions"][v]))

        graph[v] = set(map(
            lambda e: e.strip(),
            graph[v]))

    input(
        "\n_-_-_-_-_-_-_-_-_-_-_-_-_-_[PRESS ENTER TO START]_-_-_-_-_-_-_-_-_-_-_-_-_-_\n")

    try:
        # Draw the graph
        draw_graph(graph)

        def perform_ids():
            _perform_ids(root=root, goal=goal,
                         graph=graph, max_depth=max_depth)

        # Create the button to start
        button = tk.Button(window, text="Start IDS", command=perform_ids)
        button.pack()

        # Show the window
        window.mainloop()
    except KeyboardInterrupt:
        print("[Execution interrupted by user]")
    except:
        print("[An unknown error occured]")

    # print(f"[PATH] {perform_ids(root=root, goal=goal, graph=graph)}")
