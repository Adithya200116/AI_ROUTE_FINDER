from flask import Flask, render_template, request
import pickle
import osmnx as ox
import folium

from algorithms.astar import astar_path
from algorithms.dijkstra import dijkstra_path
from algorithms.bfs import bfs_path

app = Flask(__name__)

# Load saved graph
with open("data/graph_data.pkl", "rb") as f:
    graph = pickle.load(f)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/find_route', methods=['POST'])
def find_route():

    try:
        # Get form data
        source = request.form['source']
        destination = request.form['destination']
        algorithm = request.form['algorithm']

        # Convert place names to coordinates
        source_coords = ox.geocode(source)
        dest_coords = ox.geocode(destination)

        # Find nearest nodes
        source_node = ox.distance.nearest_nodes(
            graph,
            source_coords[1],
            source_coords[0]
        )

        dest_node = ox.distance.nearest_nodes(
            graph,
            dest_coords[1],
            dest_coords[0]
        )

        # Select algorithm
        if algorithm == 'astar':

            path = astar_path(
                graph,
                source_node,
                dest_node
            )

        elif algorithm == 'dijkstra':

            path = dijkstra_path(
                graph,
                source_node,
                dest_node
            )

        else:

            path = bfs_path(
                graph,
                source_node,
                dest_node
            )

        # Extract coordinates from path
        route_coords = []

        for node in path:

            lat = graph.nodes[node]['y']
            lon = graph.nodes[node]['x']

            route_coords.append((lat, lon))

        # Create map
        route_map = folium.Map(
            location=route_coords[0],
            zoom_start=13
        )

        # Draw route
        folium.PolyLine(
            route_coords,
            color='red',
            weight=6,
            opacity=0.8
        ).add_to(route_map)

        # Source marker
        folium.Marker(
            route_coords[0],
            popup="Source",
            tooltip="Source",
            icon=folium.Icon(color='green')
        ).add_to(route_map)

        # Destination marker
        folium.Marker(
            route_coords[-1],
            popup="Destination",
            tooltip="Destination",
            icon=folium.Icon(color='red')
        ).add_to(route_map)

        # Save map
        route_map.save("templates/route_map.html")

        return render_template("route_map.html")

    except Exception as e:

        return f"""
        <h1>Error Occurred</h1>
        <p>{str(e)}</p>
        <a href="/">Go Back</a>
        """


if __name__ == "__main__":
    app.run(debug=True)