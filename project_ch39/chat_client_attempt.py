import socket
import sys
import json
import select

from chatui import init_windows, read_command, print_message, end_windows


def start_client(nickname, host, port):
    client_socket = socket.socket()
    client_socket.connect((host, port))

    init_windows()
    print(f"Connected to server at {host}:{port}")

    send_hello_packet(client_socket, nickname)

    buffer = b""

    while True:
        read_sockets, write_sockets, exception_sockets = select.select({client_socket, sys.stdin}, {}, {})
        for read_socket in read_sockets:
            if read_socket == client_socket:
                buffer, packets = receive_packet(client_socket, buffer)
                if packets is None:
                    # print_message("Disconnected from server")
                    return
                for packet in packets:
                    process_server_message(packet)
            elif read_socket == sys.stdin:
                user_input = read_command(f"{nickname}> ")
                if user_input.startswith("/"):
                    if user_input == "/q":
                        send_packet(client_socket, json.dumps({"type": "leave"}))
                        end_windows()
                        return
                else:
                    chat_packet = json.dumps({"type": "chat", "message": user_input})
                    send_packet(client_socket, chat_packet)
                    # print(f"Sent chat message: {chat_packet}")


def receive_packet(client_socket, buffer):
    try:
        data = client_socket.recv(4096)
        if not data:
            return buffer, None
        buffer += data
        # print(f"Received data: {data}")
        packets = []
        while len(buffer) >= 2:
            length = int.from_bytes(buffer[:2], "big")
            if len(buffer) < (2 + length):
                break
            payload = buffer[2:2 + length]
            buffer = buffer[2 + length:]
            message = json.loads(payload.decode("utf-8"))
            packets.append(message)
            # print(f"Received packet: {message}")
        return buffer, packets
    except Exception as e:
        # print(f"Error receiving packet: {e}")
        return buffer, None


def process_server_message(message):
    message_type = message["type"]
    
    if message_type == "join":
        print_message(f"*** {message["nick"]} has joined the chat")
    elif message_type == "chat":
        print_message(f"{message["nick"]}: {message["message"]}")
    elif message_type == "leave":
        print_message(f"*** {message["nick"]} has left the chat")


def send_hello_packet(client_socket, nickname):
    send_packet(client_socket, json.dumps({"type": "hello", "nick": nickname}))
    # print(f"Sent hello packet: {hello_packet}")


def send_packet(client_socket, packet):
    packet_bytes = packet.encode("utf-8")
    packet_length = len(packet_bytes)
    client_socket.send(packet_length.to_bytes(2, "big") + packet_bytes)
    # print(f"Sent packet: {packet}")


def usage():
    print("usage: chat_client.py nickname host port", file=sys.stderr)


def main(argv):
    try:
        nickname = argv[1]
        host = argv[2]
        port = int(argv[3])
    except:
        usage()
        return 1
    
    start_client(nickname, host, port)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
