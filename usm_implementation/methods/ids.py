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
from .dls import perform_dls
from typing import Dict, Union, Set, List, Tuple

# The various data types used in this module
Vertex = Union[int, str]
Graph = Dict[Vertex, Set[Vertex]]
Path = List[Vertex]
VertexPositionMap = Dict[Vertex, Tuple[float, float]]
PathMap = Dict[Vertex, Union[Vertex, None]]
DepthMap = Dict[Vertex, int]

# Graph configurations
root = None
goal = None
max_depth = 0
graph: Graph = {}


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def perform_ids(
        root: Vertex,
        goal: Vertex,
        graph: Graph,
        max_depth: int,
        draw_path=None,
        ui_elements: List[int] = None) -> Path:
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
        path = perform_dls(root, goal, graph, i+1, draw_path, ui_elements)

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
        graph[v] = set(map(
            lambda e: e.strip(),
            graph[v]))

    print("\n_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-\n")

    try:
        # Perform IDS and print the result
        print(
            f"[PATH] {perform_ids(root=root, goal=goal, graph=graph, max_depth=max_depth)}")
    except KeyboardInterrupt:
        print("[Execution interrupted by user]")
    except:
        print("[An unknown error occured]")

    # print(f"[PATH] {perform_ids(root=root, goal=goal, graph=graph)}")
