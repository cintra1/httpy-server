import socket
import sys
import gzip

def handle_request(conn):
    data = conn.recv(1024)
    lines = data.splitlines()
    print("LINES:: ", lines)

    if not lines:
        return

    request_line = lines[0].decode()
    method, path, http_version = request_line.split()

    if path.startswith("/files") and method == "POST":
        handle_post_request(conn, lines, path)
    elif path.startswith("/files") and method == "GET":
        handle_get_request(conn, path)
    elif path.startswith("/user-agent"):
        handle_user_agent_request(conn, lines)
    elif path.startswith("/echo"):
        handle_echo_request(conn, lines, path)
    elif path == "/":
        response = "HTTP/1.1 200 OK\r\n\r\n"
        conn.send(response.encode())
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
        conn.send(response.encode())

def handle_post_request(conn, lines, path):
    if len(lines) < 4:
        response = "HTTP/1.1 400 Bad Request\r\n\r\n"
        conn.send(response.encode())
        return

    text = lines[-1].decode()
    filename = path[7:]
    directory = sys.argv[2]
    print(directory, filename)

    try:
        with open(f"{directory}/{filename}", "w") as f:
            f.write(text)
        body = len(text)
        response = f"HTTP/1.1 201 Created\r\nContent-Type: text/plain\r\nContent-Length: {body}\r\n\r\n{text}"
    except Exception as e:
        print(e)
        response = "HTTP/1.1 500 Internal Server Error\r\n\r\n"
    conn.send(response.encode())

def handle_get_request(conn, path):
    filename = path[7:]
    directory = sys.argv[2]
    print(directory, filename)
    try:
        with open(f"{directory}/{filename}", "r") as f:
            body = f.read()
        response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}"
    except Exception as e:
        print(e)
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
    conn.send(response.encode())

def handle_user_agent_request(conn, lines):
    headers = {}
    header_value = "Unknown"
    try:
        for line in lines[1:]:
            if ': ' in line.decode():
                header_key, header_value = line.decode().split(': ', 1)
                headers[header_key] = header_value
        header_value = headers.get("User-Agent", "Unknown")
    except Exception as e:
        print(e)
    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(header_value)}\r\n\r\n{header_value}"
    conn.send(response.encode())

def handle_echo_request(conn, lines, path):
    echo_str = path[6:]
    if len(lines) >= 4:
        text = lines[2].decode()
        print(text)
        if ': ' in text:
            header_key, header_value = text.split(': ', 1)
            encoding = header_value.split(', ')

            response_headers = [
                "HTTP/1.1 200 OK",
                "Content-Type: text/plain",
                f"Content-Length: {len(echo_str)}"
            ]
            body = gzip.compress(echo_str.encode("utf-8"))
            for value in encoding:
                print("TIPO:" + value.strip())
                if value.strip() == "gzip":
                    response_headers.append("Content-Encoding: gzip")
                    break

            response = "\r\n".join(response_headers) + f"\r\n\r\n{echo_str}" + body
        else:
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(echo_str)}\r\n\r\n{echo_str}"
    else:
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(echo_str)}\r\n\r\n{echo_str}"
    conn.send(response.encode())

def main():
    config = ("localhost", 4221)
    server_socket = socket.create_server(config, reuse_port=True)

    try:
        while True:
            print("Waiting for a connection...")

            conn, addr = server_socket.accept()
            print('Connected by', addr)

            with conn:
                handle_request(conn)
    except KeyboardInterrupt:
        print("\nServer is shutting down.")
    finally:
        server_socket.close()
        print("Server has been closed")

if __name__ == "__main__":
    main()
