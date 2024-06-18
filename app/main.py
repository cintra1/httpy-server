import socket
import sys
import gzip

def handle_request(conn):
    # Receive data from the client
    data = conn.recv(1024)
    # Split received data into lines
    lines = data.splitlines()

    # If no data received, return early
    if not lines:
        return

    # Decode the first line of the request to get method, path, and HTTP version
    request_line = lines[0].decode()
    method, path, http_version = request_line.split()

    # Handle different paths and methods
    if path.startswith("/files") and method == "POST":
        handle_post_request(conn, lines, path)
    elif path.startswith("/files") and method == "GET":
        handle_get_request(conn, path)
    elif path.startswith("/user-agent"):
        handle_user_agent_request(conn, lines)
    elif path.startswith("/echo"):
        handle_echo_request(conn, lines, path)
    elif path == "/":
        # Respond with a simple 200 OK for the root path
        response = "HTTP/1.1 200 OK\r\n\r\n"
        conn.send(response.encode())
    else:
        # Respond with 404 Not Found for unknown paths
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
        conn.send(response.encode())

def handle_post_request(conn, lines, path):
    # Check if request has enough lines
    if len(lines) < 4:
        response = "HTTP/1.1 400 Bad Request\r\n\r\n"
        conn.send(response.encode())
        return

    # Decode the last line to get the text data
    text = lines[-1].decode()
    # Extract filename from the path
    filename = path[7:]
    # Get directory path from command-line arguments
    directory = sys.argv[2]

    try:
        # Write text data to the specified file in the directory
        with open(f"{directory}/{filename}", "w") as f:
            f.write(text)
        body = len(text)
        # Respond with 201 Created if successful
        response = f"HTTP/1.1 201 Created\r\nContent-Type: text/plain\r\nContent-Length: {body}\r\n\r\n{text}"
    except Exception as e:
        print(e)
        # Respond with 500 Internal Server Error on exception
        response = "HTTP/1.1 500 Internal Server Error\r\n\r\n"
    conn.send(response.encode())

def handle_get_request(conn, path):
    # Extract filename from the path
    filename = path[7:]
    # Get directory path from command-line arguments
    directory = sys.argv[2]
    try:
        # Read content of the specified file
        with open(f"{directory}/{filename}", "r") as f:
            body = f.read()
        # Respond with file content and 200 OK if file exists
        response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}"
    except Exception as e:
        print(e)
        # Respond with 404 Not Found if file does not exist
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
    conn.send(response.encode())

def handle_user_agent_request(conn, lines):
    headers = {}
    header_value = "Unknown"
    try:
        # Parse headers to retrieve User-Agent information
        for line in lines[1:]:
            if ': ' in line.decode():
                header_key, header_value = line.decode().split(': ', 1)
                headers[header_key] = header_value
        header_value = headers.get("User-Agent", "Unknown")
    except Exception as e:
        print(e)
    
    # Respond with User-Agent information and 200 OK
    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(header_value)}\r\n\r\n{header_value}"
    conn.send(response.encode())

def handle_echo_request(conn, lines, path):
    # Extract content to echo from the path
    echo_str = path[6:]
    response_headers = [
        "HTTP/1.1 200 OK",
        "Content-Type: text/plain",
    ]

    if len(lines) >= 4:
        # Extract additional text data from the request
        text = lines[2].decode()
        if ': ' in text:
            # Parse headers to check for gzip encoding
            header_key, header_value = text.split(': ', 1)
            encoding = header_value.split(', ')

            for value in encoding:
                if value.strip() == "gzip":
                    # Compress echo content if gzip encoding is requested
                    response_headers.append("Content-Encoding: gzip") 
                    body = gzip.compress(echo_str.encode("utf-8"))
                    response_headers.append(f"Content-Length: {len(body)}")
                    response = "\r\n".join(response_headers) + "\r\n\r\n"
                    conn.send(response.encode() + body)
                    return

    # Respond with echo content and its length
    body = echo_str.encode("utf-8")
    response_headers.append(f"Content-Length: {len(body)}")
    response = "\r\n".join(response_headers) + "\r\n\r\n"
    conn.send(response.encode() + body)

def main():
    # Server configuration (localhost and port 4221)
    config = ("localhost", 4221)
    # Create server socket
    server_socket = socket.create_server(config, reuse_port=True)

    try:
        while True:
            print("Waiting for a connection...")

            # Accept incoming connection
            conn, addr = server_socket.accept()
            print('Connected by', addr)

            with conn:
                # Handle the incoming request
                handle_request(conn)
    except KeyboardInterrupt:
        print("\nServer is shutting down.")
    finally:
        # Close the server socket
        server_socket.close()
        print("Server has been closed")

if __name__ == "__main__":
    main()
