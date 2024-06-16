import socket

def handle_request(conn):
    data = conn.recv(1024)

    lines = data.splitlines()
    print("LINES:: ",lines)

    if lines:
        request_line = lines[0]
        method, path, http_version = request_line.split()

        request_line = lines[2]
        header_key, header_value = request_line.split()

    method = method.decode()
    path = path.decode()
    http_version = http_version.decode()
    header_key = header_key.decode() 
    header_value = header_value.decode()

    print(f"Metodo {method}, path: {path}, version: {http_version}, hkey: {header_key}, hvalue {header_value}")

    if path.startswith("/user-agent"):
        str = path[12:]
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(str)}\r\n\r\n{header_value}"
    if path.startswith("/echo"):
        str = path[6:]
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(str)}\r\n\r\n{str}"
    elif path == "/":
        response = "HTTP/1.1 200 OK\r\n\r\n"
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
        
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
                
    

   

    cli.sendall()

if __name__ == "__main__":
    main()
