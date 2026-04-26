import osmnx as ox

center_lat = 30.3165
center_lon = 78.0322

graph = ox.graph_from_point(
    (center_lat, center_lon),
    dist=10000,
    network_type="drive"
)

ox.save_graphml(graph, "dehradun.graphml")

print("Graph saved successfully")