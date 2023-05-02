"""
Breadth-First Search:
The breadth-first search algorithm starts at the root node and explores all 
the vertices at the current depth before moving on to the vertices at the next breadth level.
It maintains a queue of vertices to be explored. When a vertex is explored,
it is removed from the queue and its neighboring vertices are added to the end of the queue
if they have not already been visited.
The search continues until the goal vertex is found or the queue is empty.
"""

from typing import Dict, Union, Set, List, Tuple

# The various data types used in this module
Vertex = Union[int, str]
Graph = Dict[Vertex, Set[Vertex]]
Path = List[Vertex]
VertexPositionMap = Dict[Vertex, Tuple[float, float]]
PathMap = Dict[Vertex, Union[Vertex, None]]

# Graph data structure
graph: Graph = {}


def _compose_path(v: Vertex, paths: PathMap) -> Path:
    """
    Composes a path from the root node to a given vertex.

    Args:
    - v (Vertex): The vertex to start the path from.
    - paths (PathMap): A map that maps vertices to their direct parents after a BFS is performed.

    Returns:
        Path: A list of vertices that represents the path from the root to the goal.
    """
    path: Path = [v]

    while paths[v]:
        path.insert(0, paths[v])
        v = paths[v]

    return path


def perform_bfs(root: Vertex, goal: Vertex, graph: Graph) -> Path:
    """
    This function performs a breadth-first search on a graph starting from a given root 
    and finds a path from the root to a given goal node. It returns a set of vertices in the path.

    Args:
    - root (Vertex): A Vertex representing the starting vertex of the search.
    - goal (Vertex): A Vertex representing the goal vertex to be reached.
    - graph (Graph): A Graph representing the graph search space represented as an adjacency list.

    Returns:
        A list of vertices representing the path from the root to the goal vertex, if a path exists. 
        If no path is found, an empty set is returned.
    """
    queue: List[Vertex] = list([root])
    visited: Set[Vertex] = set()
    paths: PathMap = {v: None for v in graph}

    while queue:
        # Remove Vertex from the queue
        vertex = queue.pop(0)

        # This Vertex has not been explored
        if vertex not in visited:
            # Add Vertex to the list of visited vertices
            visited.add(vertex)

            # Vertex is the goal
            if vertex == goal:
                # Return the path to the vertex
                return _compose_path(vertex, paths)

            # Add all adjacent vertices that have not been visited to queue
            adjacent_vertices = graph[vertex] - visited - set(queue)
            queue.extend(adjacent_vertices)

            for v in adjacent_vertices:
                paths[v] = vertex

    return set()


if __name__ == "__main__":
    print("\n_-_-_-_-_-_-_-_-_-_-_-_-_-_RUNNING BFS USM SEARCH_-_-_-_-_-_-_-_-_-_-_-_-_-_\n")

    # Get a list of vertices from user
    vertices: "list[str]" = list(map(
        lambda e: e.strip(),
        input("Input graph verticies: ").split(",")))

    # Get root & goal vertices from user
    root = input("Input root vertex: ")
    goal = input("Input goal vertex: ")

    print()

    # Get the adjacency list for each vertex from user
    for v in vertices:
        graph[v] = set(map(
            lambda e: e.strip(),
            input(f"Input verticies connected to the vertex [{v}]: ").split(",")))

    print("\n_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-\n")

    try:
        # Perform BFS and print the result
        print(f"[PATH] {perform_bfs(root=root, goal=goal, graph=graph)}")
    except KeyboardInterrupt:
        print("[Execution interrupted by user]")
    except:
        print("[An unknown error occured]")

    # print(f"[PATH] {perform_bfs(root=root, goal=goal, graph=graph)}")
