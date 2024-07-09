import socket


def http_client(host, port):
    client_socket = socket.socket()
    client_socket.settimeout(5)
    client_socket.connect((host, port))

    request = (
        "GET / HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "Connection: close\r\n"
        "\r\n\r\n"
    )
    
    client_socket.sendall(request.encode())

    response = b""
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        response += data

    client_socket.close()

    print(response.decode("ISO-8859-1"))


host = "example.com"
port = 80
http_client(host, port)