from __future__ import annotations
import json
from dataclasses import dataclass
import random
from typing import Dict, List, Optional
from dataclasses import dataclass
import random


@dataclass
class Vertex:
    """
    Represents a vertex in a graph
    Args:
        key (int): The key of the vertex
        weight (int): The weight of the vertex
    """

    key: int
    weight: int

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        if isinstance(other, Vertex):
            return self.key == other.key
        return False

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, dict):
        return cls(**dict)

    def __repr__(self):
        return f"Vertex({self.key}, {self.weight})"

    def __str__(self):
        return f"Vertex({self.key}, {self.weight})"


@dataclass
class Edge:
    """
    Represents an edge in a graph
    Args:
        source (Vertex): The source vertex
        destination (Vertex): The destination vertex
        weight (int): The weight of the edge
    """

    source_vertex: Vertex
    destination_vertex: Vertex
    weight: int


class WeightedDirectedGraph:
    def __init__(self):
        self.graph: Dict[Vertex, Dict[Vertex, int]] = {}

    def add_vertex(self, vertex: Vertex):
        notExist = (vertex not in self.graph)
        if notExist:
            self.graph[vertex] = {}

    def add_edge(self, source_vertex: Vertex, destination_vertex: Vertex, weight: int):
        """"
        This method adds an edge between two vertices in the graph. 
        An edge is valid only if both the source and destination vertices exist in the graph.
        """
        bothVerticesExist = (
            source_vertex in self.graph and destination_vertex in self.graph)
        if bothVerticesExist:
            # Add the edge
            self.graph[source_vertex][destination_vertex] = weight

    def list_adjacent_vertices(self, vertex: Vertex) -> List[Vertex]:
        """
        This method returns a list of adjacent vertices to the given vertex
        """
        return list(self.graph[vertex].keys()) if vertex in self.graph else []

    def heaviest_vertex(self, vertex: Vertex) -> Optional[Vertex]:
        """
        This method returns the heaviest vertex adjacent to the given vertex using Python's max function.
        """
        validVertex = (vertex in self.graph)
        if validVertex:
            adjacent_vertices = self.graph[vertex]
            if adjacent_vertices:
                return max(adjacent_vertices, key=adjacent_vertices.get)
        return None

    def initialize_vertices(self, num_vertices: int):
        for i in range(num_vertices):
            vertex = Vertex(i, random.randint(1, 10))
            self.add_vertex(vertex)

    def initialize_edges(self, num_edges: int):
        vertices = list(self.graph.keys())
        for _ in range(num_edges):
            source_vertex = random.choice(vertices)
            destination_vertex = random.choice(vertices)
            weight = random.randint(1, 10)
            self.add_edge(source_vertex, destination_vertex, weight)

    def __str__(self):
        return str(self.graph)

    def display_results(self, vertex: Vertex):
        adjacent_vertices = self.list_adjacent_vertices(vertex)
        heaviest_vertex = self.heaviest_vertex(vertex)
        print(f"Adjacent vertices of vertex {vertex.key}: {adjacent_vertices}")
        if heaviest_vertex:
            print(
                f"Heaviest vertex adjacent to vertex {vertex.key}: Key {heaviest_vertex.key}"
            )
        else:
            print(f"No adjacent vertices found for vertex {vertex.key}")

    def print_as_json(self):
        """
        This method prints the graph as a JSON object.
        """
        graph_dict = {}
        for k, val in self.__dict__.items():
            if isinstance(k, Vertex):
                key = str(k.to_dict())
            else:
                key = str(k)
            if all(isinstance(v, Vertex) for v in val):
                value = [v.to_dict() for v in val]
            else:
                value = val
            graph_dict[key] = value
        print(json.dumps(graph_dict, indent=1))


if __name__ == "__main__":
    # Create two different graph objects
    GRAPH_1 = WeightedDirectedGraph()
    GRAPH_2 = WeightedDirectedGraph()
    GRAPH_1.initialize_vertices(8)
    GRAPH_1.initialize_edges(30)
    GRAPH_2.initialize_vertices(8)
    GRAPH_2.initialize_edges(30)
    GRAPH_1.display_results(Vertex(0, 0))
    GRAPH_2.display_results(Vertex(1, 0))

    # Print the graphs as JSON
    print("Graph 1: ")
    GRAPH_1.print_as_json()
    print("Graph 2: ")
    GRAPH_2.print_as_json()
