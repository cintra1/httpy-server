import socket

def handle_request(conn):
    data = conn.recv(1024)

    lines = data.splitlines()
    if lines:
        request_line = lines[0]
        method, path, http_version = request_line.split()

    if path:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
    else:
        response = "HTTP/1.1 200 OK\r\n\r\n"
        
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
