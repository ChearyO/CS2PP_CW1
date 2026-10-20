import csv


def file_to_edge_list(*, file_path):
    edges = []
    with open(file_path, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            u = int(row[0])
            v = int(row[1])
            edge = [u, v]
            edges.append(edge)

    return edges


def inspect_node(*, network, node):
    return [edge for edge in network
             if edge[0] == node or edge[1] == node]