import socket
import time


def time_client(host, port):
    client_socket = socket.socket()
    client_socket.connect((host, port))

    request = (
        "GET / HTTP1.1\r\n"
        f"Host {host}\r\n"
        "Connection: close\r\n"
        "\r\n\r\n"
    )

    time.sleep(2)  # Prevent NIST refusals
    client_socket.sendall(request.encode())

    response = b"" + client_socket.recv(4)
    client_socket.close()

    nist_time = int.from_bytes(response, "big")

    print(f"NIST time  : {nist_time}")
    print(f"System time: {int(time.time()) + 2208988800}")  # Add offset from 1900 to 1970


host = "time.nist.gov"
port = 37
time_client(host, port)