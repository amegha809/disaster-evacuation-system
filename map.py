import osmnx as ox
import networkx as nx
import folium
import os
import webbrowser


def get_turn_direction(p1, p2, p3):

    x1 = p2[1] - p1[1]
    y1 = p2[0] - p1[0]

    x2 = p3[1] - p2[1]
    y2 = p3[0] - p2[0]

    cross = x1 * y2 - y1 * x2

    if cross > 0:
        return "Turn Left"
    elif cross < 0:
        return "Turn Right"
    else:
        return "Go Straight"


def load_graph():
    graph = ox.load_graphml("dehradun.graphml")
    return graph


def show_route(user_lat, user_lon, dest_lat, dest_lon, dest_name):

    graph = load_graph()

    user_node = ox.distance.nearest_nodes(graph, user_lon, user_lat)
    dest_node = ox.distance.nearest_nodes(graph, dest_lon, dest_lat)

    route = nx.shortest_path(
        graph,
        user_node,
        dest_node,
        weight="length"
    )

    route_coords = []

    for node in route:
        lat = graph.nodes[node]["y"]
        lon = graph.nodes[node]["x"]
        route_coords.append((lat, lon))


    m = folium.Map(
        location=[user_lat, user_lon],
        zoom_start=14
    )


    # Start marker
    folium.Marker(
        [user_lat, user_lon],
        popup="User Location",
        tooltip="Start",
        icon=folium.Icon(color="green")
    ).add_to(m)


    # Destination marker with resource name
    folium.Marker(
        [dest_lat, dest_lon],
        popup=f"🏥 {dest_name}",
        tooltip=dest_name,
        icon=folium.Icon(color="red")
    ).add_to(m)


    # Route line
    folium.PolyLine(
        route_coords,
        color="blue",
        weight=5,
        opacity=0.8
    ).add_to(m)



    # -------- Waypoints --------
    if len(route) > 4:

        waypoint_nodes = [
            route[len(route)//4],
            route[len(route)//2],
            route[(3*len(route))//4]
        ]

        for i, node in enumerate(waypoint_nodes, start=1):

            lat = graph.nodes[node]["y"]
            lon = graph.nodes[node]["x"]

            road_name = f"Waypoint {i}"

            for _, _, data in graph.edges(node, data=True):

                if "name" in data:
                    road_name = data["name"]

                    if isinstance(road_name, list):
                        road_name = road_name[0]

                    break


            folium.Marker(
                [lat, lon],
                popup=f"Step {i}: Via {road_name}",
                tooltip=f"Step {i}: Via {road_name}",
                icon=folium.Icon(color="blue")
            ).add_to(m)


    # Save and open map
    file_path = os.path.abspath("route_map.html")
    m.save(file_path)

    webbrowser.open("file://" + file_path)

    return "Route map opened successfully"