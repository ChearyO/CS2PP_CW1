import csv


def file_to_edge_list(*, file_path):
    edges = []
    seen = set()

    with open(file_path, "r") as f:
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