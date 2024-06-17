import socket
import sys

def handle_request(conn):
    data = conn.recv(1024)

    lines = data.splitlines()
    print("LINES:: ",lines)

    if lines:
        request_line = lines[0].decode()
        method, path, http_version = request_line.split()

   # print(f"Metodo {method}, path: {path}, version: {http_version}, hkey: {header_key}, hvalue {header_value}") 

    if path.startswith("/files") and method == "POST":
        if len(lines) >= 4:
            request_line = lines[0].decode()
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
                response = "HTTP/1.1 404 Not Found\r\n\r\n"
    elif path.startswith("/files") and method == "GET":
        str = path[7:]
        directory = sys.argv[2]
        print(directory, str)
        try:
            with open(f"/{directory}/{str}", "r") as f:
                body = f.read()
            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}"
        except Exception as e:
            response = f"HTTP/1.1 404 Not Found\r\n\r\n"
    elif path.startswith("/user-agent"):
        if lines:
            headers = {}
            try:
                for line in lines[1:]:
                    header_key, header_value = line.decode().split(': ')
                    headers[header_key] = header_value
            except Exception as e:
                print(e)
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(header_value)}\r\n\r\n{header_value}"
    elif path.startswith("/echo"):
        str = path[6:]
        if len(lines) >= 4:
            text = lines[-1].decode()
            print(text)
            header_key, header_value = text.split(': ')
        
            if header_value == "gzip":
                response = f"HTTP/1.1 200 OK\r\nContent-Encoding: gzip\r\nContent-Type: text/plain\r\nContent-Length: {len(str)}\r\n\r\n{str}"
        else:
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
