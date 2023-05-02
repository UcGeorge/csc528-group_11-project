"""
Depth-first Search:
The depth-first search algorithm starts at the root node and explores as far 
as possible along each branch before backtracking. 
It maintains a stack of vertices to be explored. When a vertex is explored, 
it is removed from the stack and its neighboring vertices are added to the stack 
if they have not already been visited. 
The search continues until the goal vertex is found or the stack is empty.
"""

from usm_implementation.types import Vertex, Path, Graph

def perform_dfs(root: Vertex, goal: Vertex, graph: Graph) -> Path:
    """
    Description:
    This function performs a depth-first search on a graph starting from a given root 
    and finds a path from the root to a given goal node. It returns a set of vertices in the path.
    
    Parameters:
    root: A [Vertex] representing the starting vertex of the search.
    goal: A [Vertex] representing the goal vertex to be reached.

    Return Value:
    A set of [Vertex] representing the path from the root to the goal vertex, if a path exists. 
    If no path is found, an empty set is returned.
    """
    path = list({})
    stack = list({root})
    memory: Path = set({})

    focus: Vertex = stack.pop(-1)
    path.append(focus)
    memory.add(focus)

    # while stack:
    #     vertex = stack.pop()
    #     if vertex not in visited:
    #         visited.add(vertex)
    #         if vertex == goal:
    #             return visited
    #         stack.extend(graph[vertex] - visited)

    while focus and focus != goal:
        # This Vertex has been explored
        if focus in memory:
            # Remove from the path
            path.pop()
            continue

        # This Vertex is a leaf node
        if len(graph[focus]) == 0:
            # Remove from the path
            path.pop()
            continue



    pass