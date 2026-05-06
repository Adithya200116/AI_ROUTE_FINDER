import networkx as nx

def bfs_path(graph, source, target):

    path = nx.shortest_path(
        graph,
        source,
        target
    )

    return path