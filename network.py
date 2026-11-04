import csv
from dataclasses import dataclass


def file_to_edge_list(*, file_path):
    edges = []
    seen = set()

    with open(file_path, "r", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            u = int(row[0])
            v = int(row[1])

            canonical_pair = (min(u, v), max(u, v))

            if canonical_pair not in seen:
                seen.add(canonical_pair)
                edges.append(canonical_pair)

    return edges


def inspect_node(*, network, node):
    if isinstance(network, dict):
        return network.get(node, set())

    return [edge for edge in network if edge[0] == node or edge[1] == node]


def edge_to_neighbour_list_my(edge_list, /):
    neighbour_dict = {}
    for u, v in edge_list:
        if u not in neighbour_dict:
            neighbour_dict[u] = set()
        if v not in neighbour_dict:
            neighbour_dict[v] = set()
        neighbour_dict[u].add(v)
        neighbour_dict[v].add(u)
    return neighbour_dict


def calculate_degree_statistics(neighbour_dict):
    degrees = []

    for node, neighbours in neighbour_dict.items():
        degree = len(neighbours)

        if node in neighbours:
            degree += 1

        degrees.append(degree)

    maximum_degree = max(degrees)
    minimum_degree = min(degrees)

    average = lambda deg_list: sum(deg_list) / len(deg_list) if deg_list else 0
    average_degree = average(degrees)

    degree_counts = {deg: degrees.count(deg) for deg in set(degrees)}

    most_common = lambda deg: degree_counts[deg]
    most_common_degree = max(degree_counts.keys(), key=most_common)

    if float(average_degree).is_integer():
        average_degree = int(average_degree)

    return (
        maximum_degree,
        minimum_degree,
        average_degree,
        most_common_degree,
    )


def calculate_clustering_coefficient(*, network, node):
    neighbours = set(network.get(node, []))

    neighbours.discard(node)

    neighbour_list = list(neighbours)

    if len(neighbour_list) < 2:
        return 0.0

    checked_pairs = 0
    connected_pairs = 0

    for i in range(len(neighbour_list)):
        neighbour_a = neighbour_list[i]

        for j in range(i + 1, len(neighbour_list)):
            neighbour_b = neighbour_list[j]

            checked_pairs += 1

            if neighbour_b in network.get(neighbour_a, []):
                connected_pairs += 1

    return connected_pairs / checked_pairs




# Candiate code for 1.5

def edge_to_neighbour_list_a(edges, /):
    """Candidate A."""
    neighbours = {}
    for edge in edges:
        neighbours.setdefault(edge[0], []).append(edge[1])
        neighbours.setdefault(edge[1], []).append(edge[0])
    return neighbours


def edge_to_neighbour_list_b(edges, /):
    """Candidate B."""
    neighbours = {}
    for left, right in edges:
        neighbours.setdefault(left, []).append(right)
        neighbours.setdefault(right, [])
    return neighbours


def edge_to_neighbour_list_c(edges, /):
    """Candidate C."""
    nodes = {node for edge in edges for node in edge}
    return {
        node: [right if left == node else left
               for left, right in edges
               if node in (left, right)]
        for node in nodes
    }


def edge_to_neighbour_list_d(edges, /):
    """Candidate D."""
    if not edges:
        return {}

    largest_node = max(max(edge) for edge in edges)
    neighbours = {node: [] for node in range(largest_node + 1)}
    for left, right in edges:
        neighbours[left].append(right)
        neighbours[right].append(left)
    return neighbours


def edge_to_neighbour_list_e(edges, /):
    """Candidate E."""
    nodes = {node for edge in edges for node in edge}
    neighbours = dict.fromkeys(nodes, [])
    for left, right in edges:
        neighbours[left].append(right)
        neighbours[right].append(left)
    return neighbours


def edge_to_neighbour_list_f(edges, /):
    """Candidate F."""
    neighbours = {}
    for left, right in edges:
        neighbours[left] = neighbours.get(left, []) + [right]
        neighbours[right] = neighbours.get(right, []) + [left]
    return neighbours


def edge_to_neighbour_list_g(edges, /):
    """Candidate G."""
    neighbours = {}
    for val in edges:
        neighbours[val[0]] = set()
        neighbours[val[1]] = set()
    
    for val in edges:
        neighbours[val[0]].add(val[1])
        neighbours[val[1]].add(val[0])
    return neighbours


def edge_to_neighbour_list_h(edges, /):
    """Candidate H."""
    neighbours = {}
    for x, y in edges: 
        if isinstance(neighbours.get(x), set):
            neighbours[x].add(y)
        else:
            neighbours[x] = {y}
    
        if isinstance(neighbours.get(y), set):
            neighbours[y].add(x)
        else:
            neighbours[y] = {x}
    return neighbours


@dataclass(frozen=True, slots=True)
class _ValidatedEdge:
    left: int
    right: int

    def __post_init__(self):
        if type(self.left) is not int or type(self.right) is not int:
            raise TypeError("Node identifiers must be integers")
        if self.left == self.right:
            raise ValueError("Self-loops are not permitted")


class _UndirectedAdjacencyBuilder:
    def __init__(self):
        self._adjacency = {}

    def ingest(self, edge):
        self._adjacency.setdefault(edge.left, set()).add(edge.right)
        self._adjacency.setdefault(edge.right, set()).add(edge.left)

    def export(self):
        return {
            node: sorted(connected_nodes)
            for node, connected_nodes in self._adjacency.items()
        }


def edge_to_neighbour_list_i(edges, /):
    """Candidate I."""
    builder = _UndirectedAdjacencyBuilder()
    for pair in edges:
        builder.ingest(_ValidatedEdge(*pair))
    return builder.export()
