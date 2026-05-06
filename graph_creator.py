import osmnx as ox
import pickle

place = "Bangalore, India"

graph = ox.graph_from_place(place, network_type='drive')

with open("data/graph_data.pkl", "wb") as f:
    pickle.dump(graph, f)

print("Graph Saved")