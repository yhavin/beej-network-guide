import socket
import os


def parse_request(request: bytes):
    lines = request.decode("ISO-8859-1").split("\r\n")
    request_line = lines[0]
    print("REQUEST LINE", request_line)
    path = request_line.split(" ")[1]
    print("PATH", path)
    filename = path.lstrip("/")
    return filename


def read_file(filename: str):
    try:
        print("OPENING", filename)
        with open(filename, "rb") as f:
            data = f.read()
            return data
    except FileNotFoundError:
        print(f"{filename} NOT FOUND")
        return None
    

def get_file_attributes(filename: str, data: bytes):
    content_length = len(data)

    mime_mapping = {
        ".txt": "text/plain",
        ".html": "text/html"
    }
    extension = os.path.splitext(filename)[1]
    mime_type = mime_mapping[extension]

    return content_length, mime_type


def http_server(host, port):
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)

    while True:
        new_socket, client_address = server_socket.accept()
        print(f"Responding to {client_address}")

        request = b""
        while True:
            data = new_socket.recv(1024)
            if b"\r\n\r\n" in data:
                break
            request += data

        print("REQUEST", request.decode("ISO-8859-1"))
        if not request.strip():
            print("Empty request, ignoring.")
            new_socket.close()
            continue

        requested_filename = parse_request(request)
        file_data = read_file(requested_filename)

        if file_data is not None:
            content_length, mime_type = get_file_attributes(requested_filename, file_data)
            response = (
                "HTTP/1.1 200 OK\r\n"
                f"Content-Type: {mime_type}\r\n"
                f"Content-Length: {content_length}\r\n"
                "Connection: close\r\n"
                "\r\n"
                f"{file_data.decode("ISO-8859-1")}"
            )
        else:  # 404
            response = (
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: text/plain\r\n"
                "Content-Length: 13\r\n"
                "Connection: close\r\n"
                "\r\n"
                "404 not found"
            )

        print("RESPONSE", response)

        new_socket.sendall(response.encode())

        new_socket.close()


host = ""
port = 33490
http_server(host, port)