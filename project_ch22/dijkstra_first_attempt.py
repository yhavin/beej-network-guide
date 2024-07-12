import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, '..')))
import json
import math  # If you want to use math.inf for infinity

from project_ch19.netfuncs import find_router_for_ip


### PLAN
# Routers are dictionaries in routers dictionary, keyed by IP address
# Each router has connections dictionary, containing dictionaries of connection to router
# Connections also keyed by IP address, and contain netmask slash and ad (weight)

# Given a source IP and destination IP
# Run find_router_for_ip() on source IP and destination IP
# If the results are the same
    # They are the same subnet, so return []
# Else
    # We need to find the shortest path (i.e., run Dijkstra's)

# Initialisation
# Create distance dictionary keyed by IP address of all routers, set all values to math.inf
# Create parent dictionary keyed by IP address of all routers, set all to None
# Add all router objects to queue array (we will use min(queue), not a min-heap)
# Set distance[source_ip] = 0

# Algorithm
# While queue array is not empty
    # Get router with minimum distance from queue array, call this current (first time they are all math.inf)
    # Remove current from queue array (u)
    # For each connection of current (v)
    # If connection is in queue array
        # Proposed distance = current distance + weight (ad) of current to connection
        # If proposed distance < connection distance
            # Set distance[connection] = proposed distance
            # Set parent[connection] = current
# Use parent dictionary to find shortest path

# Functions
# dijkstras_shortest_path(routers, src_ip, dest_ip)
    # find_router_for_ip(routers, src_ip)
    # dijkstras_initialisation(routers)
    # find_shortest_path(parent, src_ip, dest_ip)


def dijkstras_shortest_path(routers: dict, src_ip: str, dest_ip: str) -> list[str]:
    """
    This function takes a dictionary representing the network, a source
    IP, and a destination IP, and returns a list with all the routers
    along the shortest path.

    The source and destination IPs are **not** included in this path.

    Note that the source IP and destination IP will probably not be
    routers! They will be on the same subnet as the router. You'll have
    to search the routers to find the one on the same subnet as the
    source IP. Same for the destination IP. [Hint: make use of your
    find_router_for_ip() function from the last project!]

    The dictionary keys are router IPs, and the values are dictionaries
    with a bunch of information, including the routers that are directly
    connected to the key.

    This partial example shows that router `10.31.98.1` is connected to
    three other routers: `10.34.166.1`, `10.34.194.1`, and `10.34.46.1`:

    {
        "10.34.98.1": {
            "connections": {
                "10.34.166.1": {
                    "netmask": "/24",
                    "interface": "en0",
                    "ad": 70
                },
                "10.34.194.1": {
                    "netmask": "/24",
                    "interface": "en1",
                    "ad": 93
                },
                "10.34.46.1": {
                    "netmask": "/24",
                    "interface": "en2",
                    "ad": 64
                }
            },
            "netmask": "/24",
            "if_count": 3,
            "if_prefix": "en"
        },
        ...

    The "ad" (Administrative Distance) field is the edge weight for that
    connection.

    **Strong recommendation**: make functions to do subtasks within this
    function. Having it all built as a single wall of code is a recipe
    for madness.
    """

    # TODO Write me!
    # Check if source and destination are on same subnet
    src_router_ip = find_router_for_ip(routers, src_ip)
    dest_router_ip = find_router_for_ip(routers, dest_ip)
    
    if src_router_ip == dest_router_ip:
        return []
    # Otherwise, we need to run Dijkstra's
    else:
        # Initialise Dijkstra's
        distance, parent, queue = initialise_dijkstra(routers, src_router_ip)

        # Main algorithm
        while queue:
            current_router = get_min_distance_router(queue, distance)
            queue.remove(current_router)

            for connection, connection_details in routers[current_router]["connections"].items():
                if connection in queue:
                    proposed_distance = distance[current_router] + connection_details["ad"]
                    if proposed_distance < distance[connection]:
                        distance[connection] = proposed_distance
                        parent[connection] = current_router

        # Find shortest path and remove src_ip and dest_ip
        shortest_path = find_shortest_path(parent, src_router_ip, dest_router_ip)
        shortest_path = shortest_path[1:-1]
        return shortest_path


def initialise_dijkstra(routers: dict, src_router_ip: str) -> tuple[dict, dict, list]:    
    distance = {router: math.inf for router in routers}
    distance[src_router_ip] = 0
    parent = {router: None for router in routers}
    queue = [router for router in routers]

    return distance, parent, queue


def get_min_distance_router(queue: list, distance: dict) -> str:
    min_router = None
    min_distance = math.inf
    for router in queue:
        if distance[router] < min_distance:
            min_distance = distance[router]
            min_router = router
    
    return min_router


def find_shortest_path(parent: dict, src_router_ip: str, dest_router_ip: str) -> list[str]:
    path = []
    current = dest_router_ip
    while current != src_router_ip:
        path.append(current)
        current = parent[current]

    path.reverse()
    return path


#------------------------------
# DO NOT MODIFY BELOW THIS LINE
#------------------------------
def read_routers(file_name):
    with open(file_name) as fp:
        data = fp.read()

    return json.loads(data)

def find_routes(routers, src_dest_pairs):
    for src_ip, dest_ip in src_dest_pairs:
        path = dijkstras_shortest_path(routers, src_ip, dest_ip)
        print(f"{src_ip:>15s} -> {dest_ip:<15s}  {repr(path)}")

def usage():
    print("usage: dijkstra.py infile.json", file=sys.stderr)

def main(argv):
    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)

    routers = json_data["routers"]
    routes = json_data["src-dest"]

    find_routes(routers, routes)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
