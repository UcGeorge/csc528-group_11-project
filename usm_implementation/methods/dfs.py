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
from typing import Dict, Union, Set, List, Tuple

# The various data types used in this module
Vertex = Union[int, str]
Graph = Dict[Vertex, Set[Vertex]]
Path = List[Vertex]
VertexPositionMap = Dict[Vertex, Tuple[float, float]]
PathMap = Dict[Vertex, Union[Vertex, None]]

# Graph configurations
root = None
goal = None
graph: Graph = {}


def _draw_path(path: Path, color: str, width: int, draw_path, ui_elements):
    # Draw the path
    if draw_path:
        drawn_elements = draw_path(path, color=color, width=width)
        if ui_elements:
            ui_elements.extend(drawn_elements)


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


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


def perform_dfs(
        root: Vertex,
        goal: Vertex,
        graph: Graph,
        draw_path=None,
        ui_elements: List[int] = None) -> Path:
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
            _draw_path(node_path, "orange", 4, draw_path, ui_elements)

            # Vertex is the goal
            if vertex == goal:
                # Draw the path
                _draw_path(node_path, "green", 8, draw_path, ui_elements)

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
    graph_config = read_json_file("./usm_implementation/graph-config-v2.json")

    # Get root & goal vertices from user
    root = graph_config["root"]
    goal = graph_config["goal"]
    graph = graph_config["graph"]

    # Get the adjacency list for each vertex from user
    for v in graph:
        graph[v] = set(map(
            lambda e: e.strip(),
            graph[v]))

    print("\n_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-\n")

    try:
        # Perform DFS and print the result
        print(f"[PATH] {perform_dfs(root=root, goal=goal, graph=graph)}")
    except KeyboardInterrupt:
        print("[Execution interrupted by user]")
    except:
        print("[An unknown error occured]")

    # print(f"[PATH] {perform_dfs(root=root, goal=goal, graph=graph)}")
