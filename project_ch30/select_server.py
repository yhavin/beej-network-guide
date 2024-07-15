# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select

def run_server(port):
    # TODO--fill this in
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("127.0.0.1", port))
    server_socket.listen(5)

    read_sockets = {server_socket}

    while True:
        read, write, exc = select.select(read_sockets, {}, {})

        for s in read:
            if s is server_socket:  # Listener socket for new connections
                client_socket, client_address = server_socket.accept()
                print(f"{client_address}: connected") 
                read_sockets.add(client_socket)
            else:  # Incoming data from read sockets
                data = s.recv(4096)
                if data:
                    print(f"{s.getpeername()} {len(data)} bytes: {data}")
                else:  # Connection closed
                    print(f"{s.getpeername()}: disconnected")
                    read_sockets.remove(s)
                    s.close()


#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: select_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
