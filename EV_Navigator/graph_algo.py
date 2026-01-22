import heapq
from data.nodes import edges
from data.charging_stations import charging_stations

def battery_dijkstra(start, end, battery, mileage_per_percent, max_battery_percent=100):
    D = {node: float('inf') for node in edges}
    battery_left = {node: 0 for node in edges}
    previous = {node: None for node in edges}

    D[start] = 0
    battery_left[start] = battery
    pq = [(0, start, battery)]
    visited = set()

    while pq:
        dist_so_far, current, current_battery = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)

        if current_battery <= 0:
            continue

        if current == end:
            break

        for neighbor, distance in edges[current]:
            battery_needed = distance / mileage_per_percent
            if battery_needed > current_battery:
                continue
            new_battery = current_battery - battery_needed
            if neighbor in charging_stations:
                new_battery = current_battery - battery_needed #max_battery_percent
            new_dist = dist_so_far + distance
            if new_dist < D[neighbor]:
                D[neighbor] = new_dist
                battery_left[neighbor] = new_battery
                previous[neighbor] = current
                heapq.heappush(pq, (new_dist, neighbor, new_battery))

    if D[end] == float('inf'):
        return None, None, None

    path = []
    node = end
    while node is not None:
        path.append(node)
        node = previous[node]
    path.reverse()
    return path, D[end], battery_left[end]