import networkx as nx

def astar_path(graph, source, target):
    path = nx.astar_path(
        graph,
        source,
        target,
        weight='length'
    )

    return path