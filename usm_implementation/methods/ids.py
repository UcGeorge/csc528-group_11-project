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

            # Vertex is the goal
            if vertex == goal:
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


def perform_ids(root: Vertex, goal: Vertex, graph: Graph, max_depth: int) -> Path:
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

    # Get a list of vertices from user
    vertices: "list[str]" = list(map(
        lambda e: e.strip(),
        input("Input graph verticies: ").split(",")))

    # Get root & goal vertices from user
    root = input("Input root vertex: ")
    goal = input("Input goal vertex: ")
    max_depth = int(input("Input the maximum depth: "))

    print()

    # Get the adjacency list for each vertex from user
    for v in vertices:
        graph[v] = set(map(
            lambda e: e.strip(),
            input(f"Input verticies connected to the vertex [{v}]: ").split(",")))

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
