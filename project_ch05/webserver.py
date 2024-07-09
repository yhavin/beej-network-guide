import socket


def http_server(address, port):
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((address, port))
    server_socket.listen(5)

    while True:
        new_socket, client_address = server_socket.accept()

        request = b""
        while True:
            data = new_socket.recv(1024)
            if b"\r\n\r\n" in data:
                break
            request += data

        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            "Connection: close\r\n"
            "\r\n"
            f"""
            <html>
                <body>
                    <h1>Hello, world!</h1>
                    <h3>Responding to {client_address}</h3>
                    <p>Request: {request.decode("ISO-8859-1")}</p>
                </body>
            </html>
            """
        )

        new_socket.sendall(response.encode())
        
        new_socket.close()


address = ""
port = 20123
http_server(address, port)