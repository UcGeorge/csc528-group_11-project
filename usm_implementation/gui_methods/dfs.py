"""
Depth-first Search:
The depth-first search algorithm starts at the root node and explores as far 
as possible along each branch before backtracking. 
It maintains a stack of vertices to be explored. When a vertex is explored, 
it is removed from the stack and its neighboring vertices are added to the stack 
if they have not already been visited. 
The search continues until the goal vertex is found or the stack is empty.
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

# Graph data structure
graph: Graph = {}

# Positions of the nodes on the canvas
node_positions: VertexPositionMap = {}

# Create the window
window = tk.Tk()
window.title("Depth-first search GUI demo")

# Create the canvas
canvas = tk.Canvas(window, width=500, height=500)
canvas.pack()


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def draw_graph(graph: Graph) -> None:
    for node in graph:
        # Get the position of the node
        x, y = node_positions[node]

        # Draw the nodes as circles
        canvas.create_oval(x-20, y-20, x+20, y+20, fill="black")
        canvas.create_text(x, y, text=node, fill="white")
        canvas.update()
        time.sleep(.15)

    for node in graph:
        # Get the position of the node
        x1, y1 = node_positions[node]

        # Draw the edges to its neighbors
        for neighbor in graph[node]:
            x2, y2 = node_positions[neighbor]
            # Draw the edge from the node to the neighbor
            canvas.create_line(x1, y1, x2, y2, dash=(3, 5), arrow=tk.LAST)
            canvas.update()
            time.sleep(.15)


def draw_path(path: Path, color: str, width: int) -> None:
    if not path:
        return

    start = path[0]

    for i in range(1, len(path)):
        end = path[i]

        # Get the position of the start & end node
        x1, y1 = node_positions[start]
        x2, y2 = node_positions[end]

        # Draw the edge from the start to end
        canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST,
                           width=width, fill=color)
        canvas.update()

        start = end
        time.sleep(.3)


def _compose_path(v: Vertex, paths: PathMap) -> Path:
    """
    Composes a path from the root node to a given vertex.

    Args:
    - v (Vertex): The vertex to start the path from.
    - paths (PathMap): A map that maps vertices to their direct parents after a DFS is performed.

    Returns:
        Path: A list of vertices that represents the path from the root to the goal.
    """
    path: Path = [v]

    while paths[v]:
        path.insert(0, paths[v])
        v = paths[v]

    return path


def _perform_dfs(root: Vertex, goal: Vertex, graph: Graph) -> Path:
    """
    This function performs a depth-first search on a graph starting from a given root 
    and finds a path from the root to a given goal node. It returns a set of vertices in the path.

    Args:
    - root (Vertex): A Vertex representing the starting vertex of the search.
    - goal (Vertex): A Vertex representing the goal vertex to be reached.
    - graph (Graph): A Graph representing the graph search space represented as an adjacency list.

    Returns:
        A list of vertices representing the path from the root to the goal vertex, if a path exists. 
        If no path is found, an empty set is returned.
    """
    stack: List[Vertex] = list([root])
    visited: Set[Vertex] = set()
    paths: PathMap = {v: None for v in graph}

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
                return node_path

            # Add all adjacent vertices that have not been visited to stack
            adjacent_vertices = graph[vertex] - visited - set(stack)
            stack.extend(adjacent_vertices)

            for v in adjacent_vertices:
                paths[v] = vertex

    return set()


if __name__ == "__main__":
    print("\n_-_-_-_-_-_-_-_-_-_-_-_-_-_RUNNING DFS USM SEARCH_-_-_-_-_-_-_-_-_-_-_-_-_-_\n")

    # Get graph config from file
    graph_config = read_json_file("./usm_implementation/graph-config.json")

    # Get root & goal vertices from user
    root = graph_config["root"]
    goal = graph_config["goal"]
    graph = graph_config["graph"]

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

        def perform_dfs():
            _perform_dfs(root=root, goal=goal, graph=graph)

        # Create the button to start
        button = tk.Button(window, text="Start DFS", command=perform_dfs)
        button.pack()

        # Show the window
        window.mainloop()
    except KeyboardInterrupt:
        print("[Execution interrupted by user]")
    except:
        print("[An unknown error occured]")

    # draw_graph(graph)
    # input()
    # print(f"[PATH] {perform_dfs(root=root, goal=goal, graph=graph)}")
