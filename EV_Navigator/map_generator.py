import gmplot
from data.nodes import nodes, edges
from data.charging_stations import charging_stations

def generate_map(path=None, filename="templates/map.html"):
    first_node = nodes[path[0]] if path else list(nodes.values())[0]
    gmap = gmplot.GoogleMapPlotter(first_node[0], first_node[1], 16)

    for node_id, (lat, lng) in nodes.items():
        color = 'green' if node_id in charging_stations else 'red'
        gmap.scatter([lat], [lng], color=color, size=50, marker=True)

    for u, neighbors in edges.items():
        for v, _ in neighbors:
            latitudes = [nodes[u][0], nodes[v][0]]
            longitudes = [nodes[u][1], nodes[v][1]]
            gmap.plot(latitudes, longitudes, color='grey', edge_width=1)

    if path and len(path) > 1:
        latitudes = [nodes[node][0] for node in path]
        longitudes = [nodes[node][1] for node in path]
        gmap.plot(latitudes, longitudes, color='orange', edge_width=3)

        start_node = path[0]
        end_node = path[-1]
        start_lat, start_lng = nodes[start_node]
        end_lat, end_lng = nodes[end_node]
        start_color = 'green' if start_node in charging_stations else 'red'
        end_color = 'green' if end_node in charging_stations else 'red'
        gmap.marker(start_lat, start_lng, title="Start", color=start_color)
        gmap.marker(end_lat, end_lng, title="End", color=end_color)

    gmap.draw(filename)