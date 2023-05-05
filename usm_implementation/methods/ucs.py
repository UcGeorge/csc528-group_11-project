"""
Uniform-Cost Search:
The uniform-cost search algorithm is a variant of the breadth-first search 
algorithm that takes into account the cost of each path. It explores the search 
space by prioritizing the paths that have the lowest accumulated cost.

The algorithm starts by initializing a priority queue with the source vertex as 
the starting point, and the cost of the path from the source vertex to the 
current vertex is set to 0. At each step of the algorithm, the vertex with the 
lowest accumulated cost is removed from the priority queue and its neighboring 
vertices are explored.

The algorithm updates the cost of the path to each neighboring vertex by adding 
the cost of the edge that connects the current vertex to the neighboring 
vertex. If the neighboring vertex is not in the priority queue or the new cost is 
lower than the previously recorded cost, the vertex is added to the priority queue 
with the new cost.

The uniform-cost search algorithm continues until the goal vertex is found or 
the priority queue is empty. If the goal vertex is found, the algorithm returns 
the path with the lowest cost. Otherwise, it indicates that there is no path from 
the source vertex to the goal vertex.

To implement the uniform-cost search algorithm, the algorithm needs to keep track 
of the cost of the path to each vertex and the order in which the vertices are 
explored. The algorithm can be implemented using a priority queue data structure 
that prioritizes vertices based on their accumulated cost.
"""
import json
import heapq
from typing import Dict, Union, Set, List, Tuple

# The various data types used in this module
Vertex = Union[int, str]
Graph = Dict[Vertex, Set[Vertex]]
Path = List[Vertex]
Position = Tuple[Union[float, int], Union[float, int]]
VertexPositionMap = Dict[Vertex, Position]
PathMap = Dict[Vertex, Union[Vertex, None]]
CostMap = Dict[str, Union[float, int]]

# Graph configurations
root = None
goal = None
graph: Graph = {}
edge_costs: CostMap = {}


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
    - paths (PathMap): A map that maps vertices to their direct parents after a BFS is performed.

    Returns:
        Path: A list of vertices that represents the path from the root to the goal.
    """
    path: Path = [v]

    while paths[v]:
        path.insert(0, paths[v])
        v = paths[v]

    return path


def perform_ucs(
        root: Vertex,
        goal: Vertex,
        graph: Graph,
        edge_costs: CostMap,
        draw_path=None,
        ui_elements: List[int] = None) -> Path:
    """
    This function performs a uniform cost search on a graph starting from a given root 
    and finds a path with the minimum cost from the root to a given goal node. It returns a set of vertices in the path.

    Args:
    - root (Vertex): A Vertex representing the starting vertex of the search.
    - goal (Vertex): A Vertex representing the goal vertex to be reached.
    - graph (Graph): A Graph representing the graph search space represented as an adjacency list.
    - edge_costs (CostMap): A Map representing the edges and their costs.

    Returns:
        A list of vertices representing the lowest cost path from the root to the goal vertex, if a path exists. 
        If no path is found, an empty set is returned.
    """
    # Initialize the frontier queue with the root vertex and its cost
    frontier = [(0, root)]

    # Initialize the explored set
    visited: Set[Vertex] = set()

    # Initialize the path map with the root vertex and no parent
    paths: PathMap = {v: None for v in graph}

    # Keep track of the cost of each vertex from the root
    costs: CostMap = {v: float('inf') for v in graph}
    costs[root] = 0

    # Loop until the frontier is empty
    while frontier:
        # Pop the vertex with the lowest cost from the frontier
        _, current_vertex = heapq.heappop(frontier)

        # Reconstruct the path from the root to the goal
        node_path = _compose_path(current_vertex, paths)

        # Draw the path
        _draw_path(node_path, "orange", 4, draw_path, ui_elements)

        # Check if we have reached the goal vertex
        if current_vertex == goal:
            # Draw the path
            _draw_path(node_path, "green", 8, draw_path, ui_elements)

            # Return the path to the vertex
            return node_path

        # Mark the current vertex as explored
        visited.add(current_vertex)

        # Explore the neighbors of the current vertex
        for neighbor in graph[current_vertex]:
            # Compute the cost of moving from the current vertex to the neighbor
            cost = costs[current_vertex] + \
                edge_costs[f"{current_vertex}-{neighbor}"]

            # Draw the path
            _draw_path([current_vertex, neighbor],
                       "yellow", 2, draw_path, ui_elements)

            # If the neighbor is not explored or the new cost is lower than the previous cost
            if neighbor not in visited or cost < costs[neighbor]:
                # Update the cost and path of the neighbor
                costs[neighbor] = cost
                paths[neighbor] = current_vertex

                # Add the neighbor to the frontier with its cost
                heapq.heappush(frontier, (cost, neighbor))

    # If we get here, there is no path from the root to the goal
    return None


if __name__ == "__main__":
    print("\n_-_-_-_-_-_-_-_-_-_-_-_-_-_RUNNING BFS USM SEARCH_-_-_-_-_-_-_-_-_-_-_-_-_-_\n")

    # Get graph config from file
    graph_config = read_json_file("./usm_implementation/graph-config-v3.json")

    # Get root & goal vertices from user
    root = graph_config["root"]
    goal = graph_config["goal"]
    graph = graph_config["graph"]

    if "edge_costs" in graph_config:
        edge_costs = graph_config["edge_costs"]

    # Get the adjacency list for each vertex from user
    for v in graph:
        graph[v] = set(map(
            lambda e: e.strip(),
            graph[v]))

    print("\n_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-\n")

    try:
        # Perform BFS and print the result
        print(
            f"[PATH] {perform_ucs(root=root, goal=goal, graph=graph, edge_costs=edge_costs)}")
    except KeyboardInterrupt:
        print("[Execution interrupted by user]")
    except:
        print("[An unknown error occured]")

    # print(f"[PATH] {perform_bfs(root=root, goal=goal, graph=graph)}")
