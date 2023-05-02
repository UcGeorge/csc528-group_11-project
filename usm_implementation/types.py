"""
This module defines the various data types used throughout the software
"""

from typing import Dict, Union, Set

Vertex = Union[int, str]
Graph = Dict[Vertex, Set[Vertex]]
Path = Set[Vertex]
