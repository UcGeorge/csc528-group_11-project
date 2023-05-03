"""
Bi-Directional Search:
The bi-directional search algorithm is a variant of the breadth-first search 
algorithm that simultaneously performs two breadth-first searches from the source 
vertex and the target vertex towards each other. It maintains two sets of visited 
vertices, one for the vertices visited from the source vertex and one for the 
vertices visited from the target vertex.

The search starts with both sets containing only the source vertex and the target 
vertex, respectively. At each step of the search, the algorithm expands the set 
of vertices that can be reached from the source vertex and the target vertex 
simultaneously by exploring their neighboring vertices.

The bi-directional search algorithm continues until a vertex is found that exists 
in both sets of visited vertices. This vertex is the intersection point of the two 
search trees and represents the shortest path from the source vertex to the target vertex.
"""

import json
from typing import Dict, Union, Set, List, Tuple

# The various data types used in this module
Vertex = Union[int, str]
Graph = Dict[Vertex, Set[Vertex]]
Path = List[Vertex]
VertexPositionMap = Dict[Vertex, Tuple[float, float]]
PathMap = Dict[Vertex, Union[Vertex, None]]

# Graph data structure
graph: Graph = {}


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def _compose_path(v: Vertex, paths: PathMap) -> Path:
    """
    Composes a path from the root node to a given vertex.

    Args:
    - v (Vertex): The vertex to start the path from.
    - paths (PathMap): A map that maps vertices to their direct parents after a BIDI is performed.

    Returns:
        Path: A list of vertices that represents the path from the root to the goal.
    """
    path: Path = [v]

    while paths[v]:
        path.insert(0, paths[v])
        v = paths[v]

    return path


def perform_bidi(root: Vertex, goal: Vertex, graph: Graph) -> Path:
    """
    This function performs a bi-directional search on a graph starting from a given root 
    and finds a path from the root to a given goal node. It returns a set of vertices in the path.

    Args:
    - root (Vertex): A Vertex representing the starting vertex of the search.
    - goal (Vertex): A Vertex representing the goal vertex to be reached.
    - graph (Graph): A Graph representing the graph search space represented as an adjacency list.

    Returns:
        A list of vertices representing the path from the root to the goal vertex, if a path exists. 
        If no path is found, an empty set is returned.
    """
    root_queue: List[Vertex] = list([root])
    goal_queue: List[Vertex] = list([goal])

    root_visited: Set[Vertex] = set()
    goal_visited: Set[Vertex] = set()

    paths: PathMap = {v: None for v in graph}

    while root_queue or goal_queue:
        if root_queue:
            # Remove Vertex from the queue
            vertex = root_queue.pop(0)

            # This Vertex has not been explored
            if vertex not in root_visited:
                # Add Vertex to the list of root_visited vertices
                root_visited.add(vertex)

                # # Vertex is the goal
                # if vertex == goal:
                #     # Return the path to the vertex
                #     return _compose_path(vertex, paths)

                # Add all adjacent vertices that have not been root_visited to root_queue
                adjacent_vertices = graph[vertex] - \
                    root_visited - set(root_queue)
                root_queue.extend(adjacent_vertices)

                for v in adjacent_vertices:
                    # # Vertex has been seen
                    if paths[v]:
                        path_to_goal = _compose_path(v, paths)[::-1]
                        path_from_root = _compose_path(vertex, paths)

                        # Return the path to the vertex
                        path_from_root.extend(path_to_goal)
                        return path_from_root

                    # Vertex has not been seen
                    paths[v] = vertex

        if goal_queue:
            # Remove Vertex from the queue
            vertex = goal_queue.pop(0)

            # This Vertex has not been explored
            if vertex not in goal_visited:
                # Add Vertex to the list of goal_visited vertices
                goal_visited.add(vertex)

                # # Vertex is the root
                # if vertex == root:
                #     # Return the path to the vertex
                #     return _compose_path(vertex, paths)

                # Add all adjacent vertices that have not been goal_visited to goal_queue
                adjacent_vertices = graph[vertex] - \
                    goal_visited - set(goal_queue)
                goal_queue.extend(adjacent_vertices)

                for v in adjacent_vertices:
                    # Vertex has been seen
                    if paths[v]:
                        path_to_goal = _compose_path(vertex, paths)[::-1]
                        path_from_root = _compose_path(v, paths)

                        # Return the path to the vertex
                        path_from_root.extend(path_to_goal)
                        return path_from_root

                    # Vertex has not been seen
                    paths[v] = vertex

    return set()


if __name__ == "__main__":
    print("\n_-_-_-_-_-_-_-_-_-_-_-_-_-_RUNNING BIDI USM SEARCH_-_-_-_-_-_-_-_-_-_-_-_-_-_\n")

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

    # try:
    #     # Perform BIDI and print the result
    #     print(f"[PATH] {perform_bidi(root=root, goal=goal, graph=graph)}")
    # except KeyboardInterrupt:
    #     print("[Execution interrupted by user]")
    # except:
    #     print("[An unknown error occured]")

    print(f"[PATH] {perform_bidi(root=root, goal=goal, graph=graph)}")
