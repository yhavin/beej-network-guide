import select
import sys
import socket
import json


connected_clients = set()
client_buffers = {}
client_nicknames = {}


def start_server(port):
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", port))
    server_socket.listen(10)

    while True:
        read_sockets, write_sockets, exception_sockets = select.select(connected_clients, {}, {})

        for read_socket in read_sockets:
            if read_socket == server_socket:
                handle_new_connection(server_socket)
            else:
                handle_client_message(read_socket, server_socket)


def handle_new_connection(server_socket):
    client_socket, client_address = server_socket.accept()
    connected_clients.add(client_socket)
    client_buffers[client_socket] = b""
    client_nicknames[client_socket] = None


def handle_client_message(client_socket, server_socket):
    try:
        data = client_socket.recv(4096)
        if data:
            client_buffers[client_socket] += data
            while len(client_buffers[client_socket]) >= 2:
                packet_length = int.from_bytes(client_buffers[client_socket][:2], "big")
                if len(client_buffers[client_socket]) < (2 + packet_length):
                    break
                payload = client_buffers[client_socket][2:2 + packet_length]
                client_buffers[client_socket] = client_buffers[client_socket][2 + packet_length:]
                message = json.loads(payload.decode("utf-8"))
                process_message(client_socket, message, server_socket)
        else:
            raise Exception()
    except:
        nickname = client_nicknames[client_socket]
        handle_client_leave(client_socket, nickname, server_socket)


def process_message(client_socket, message, server_socket):
    message_type = message["type"]
    
    if message_type == "hello":
        client_nicknames[client_socket] = message["nick"]
        broadcast(client_socket, json.dumps(message), server_socket)
    elif message_type == "chat":
        broadcast(client_socket, json.dumps(message), server_socket)
    elif message_type == "leave":
        nickname = client_nicknames[client_socket]
        handle_client_leave(client_socket, nickname, server_socket)


def handle_client_leave(client_socket, nickname, server_socket):
    leave_payload = {
        "type": "leave",
        "nick": nickname
    }
    broadcast(client_socket, json.dumps(leave_payload), server_socket)
    client_socket.close()
    connected_clients.remove(client_socket)
    del client_buffers[client_socket]
    del client_nicknames[client_socket]


def broadcast(sender_socket, message, server_socket):
    for client_socket in connected_clients:
        if client_socket != server_socket and client_socket != sender_socket:
            try:
                client_socket.send(message.encode())
            except:
                client_socket.close()
                connected_clients.remove(client_socket)


def usage():
    print("usage: chat_server.py port", file=sys.stderr)


def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1
    
    start_server(port)


if __name__ == "__main__":
    sys.exit(main(sys.argv))