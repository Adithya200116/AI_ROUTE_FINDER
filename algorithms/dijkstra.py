import networkx as nx

def dijkstra_path(graph, source, target):

    path = nx.dijkstra_path(
        graph,
        source,
        target,
        weight='length'
    )

    return path