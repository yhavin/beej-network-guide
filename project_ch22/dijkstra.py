import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(current_dir, '..')))
import json
import math  # If you want to use math.inf for infinity

from project_ch19.netfuncs import find_router_for_ip


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
    src_router = find_router_for_ip(routers, src_ip)
    dest_router = find_router_for_ip(routers, dest_ip)

    # Check if src and dest are in same subnet
    if src_router == dest_router:
        return []
    else:
        # Run Dijkstra's
        # Initialise data structures
        distance, parent, queue = initialise_dijkstra(routers, src_router)
    
        while queue:
            # current = u
            current_router = min(queue, key=distance.get)
            queue.remove(current_router)

            # neighbour = v
            for connection_ip, connection_details in routers[current_router]["connections"].items():
                if connection_ip in queue:
                    proposed_distance = distance[current_router] + connection_details["ad"]
                    if proposed_distance < distance[connection_ip]:
                        distance[connection_ip] = proposed_distance
                        parent[connection_ip] = current_router

        shortest_path = find_shortest_path(parent, src_router, dest_router)
        return shortest_path


def initialise_dijkstra(routers: dict, src_router: str) -> tuple[dict, dict, list]:
    distance = {router: math.inf for router in routers}
    distance[src_router] = 0
    parent = {router: 0 for router in routers}
    queue = list(routers.keys())

    return distance, parent, queue


def find_shortest_path(parent: dict, src_router: str, dest_router: str) -> list:
    path = []
    current = dest_router
    while current != src_router:
        path.append(current)
        current = parent[current]
    path.append(src_router)
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
    
