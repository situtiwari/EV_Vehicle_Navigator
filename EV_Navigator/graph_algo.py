import heapq
from data.nodes import edges
from data.charging_stations import charging_stations


def battery_dijkstra(start, end, battery, mileage_per_percent):
    """
    Finds path from start to end using current battery.
    No recharge logic here.
    """

    D = {node: float('inf') for node in edges}
    battery_left = {node: 0 for node in edges}
    previous = {node: None for node in edges}

    D[start] = 0
    battery_left[start] = battery

    pq = [(0, start, battery)]

    while pq:

        dist_so_far, current, current_battery = heapq.heappop(pq)

        if current == end:
            break

        for neighbor, distance in edges[current]:

            battery_needed = distance / mileage_per_percent

            if battery_needed > current_battery:
                continue

            new_battery = current_battery - battery_needed
            new_dist = dist_so_far + distance

            if new_dist < D[neighbor]:

                D[neighbor] = new_dist
                battery_left[neighbor] = new_battery
                previous[neighbor] = current

                heapq.heappush(
                    pq,
                    (new_dist, neighbor, new_battery)
                )

    if D[end] == float('inf'):
        return None, None, None

    path = []

    node = end

    while node is not None:
        path.append(node)
        node = previous[node]

    path.reverse()

    return path, D[end], battery_left[end]


def find_ev_route(
        source,
        destination,
        battery,
        mileage_per_percent,
        max_battery_percent=100):

    # ----------------------------
    # CASE 1
    # Directly reachable
    # ----------------------------

    path, distance, remaining_battery = battery_dijkstra(
        source,
        destination,
        battery,
        mileage_per_percent
    )

    if path is not None:

        return {
            "status": "DIRECT",
            "path": path,
            "distance": distance,
            "battery": remaining_battery
        }

    # ----------------------------
    # CASE 2
    # Route via charging station
    # ----------------------------

    best_path = None
    best_station = None
    best_distance = float('inf')
    best_remaining_battery = 0

    for station in charging_stations:

        if station == source:
            continue

        # Can we reach charging station?

        path1, dist1, battery_after_station = battery_dijkstra(
            source,
            station,
            battery,
            mileage_per_percent
        )

        if path1 is None:
            continue

        # Recharge to full battery

        path2, dist2, battery_after_destination = battery_dijkstra(
            station,
            destination,
            max_battery_percent,
            mileage_per_percent
        )

        if path2 is None:
            continue

        total_distance = dist1 + dist2

        if total_distance < best_distance:

            best_distance = total_distance
            best_station = station

            # avoid duplicate station node
            best_path = path1[:-1] + path2

            best_remaining_battery = battery_after_destination

    if best_path is not None:

        return {
            "status": "CHARGING_REQUIRED",
            "path": best_path,
            "distance": best_distance,
            "battery": best_remaining_battery,
            "charging_station": best_station
        }

    # ----------------------------
    # CASE 3
    # No route possible
    # ----------------------------

    return {
        "status": "NO_ROUTE",
        "path": None,
        "distance": None,
        "battery": None
    }