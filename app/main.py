import socket

def handle_request(conn):
    data = conn.recv(1024)

    lines = data.splitlines()
    print("LINES:: ",lines)

    if lines:
        request_line = lines[0].decode()
        method, path, http_version = request_line.split()

        headers = {}

        try:
            for line in lines[1:]:
                header_key, header_value = line.decode().split(': ')
                headers[header_key] = header_value
        except Exception as e:
            print(e)

    print(f"Metodo {method}, path: {path}, version: {http_version}, hkey: {header_key}, hvalue {header_value}") 

    if path.startswith("/files"):
        str = path[7:]
        print(str)
        try:
            with open(f"/str", "r") as f:
                body = f.read()
            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}"
        except Exception as e:
            response = f"HTTP/1.1 404 Not Found\r\n\r\n"
    elif path.startswith("/user-agent"):
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(header_value)}\r\n\r\n{header_value}"
    elif path.startswith("/echo"):
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
