![logo-httpy-small](https://github.com/cintra1/httpy-server/assets/101955322/4f1afe8e-eaaf-4926-9bdc-ad033e4dfe82)

# httpy - HTTP Server in Python

This project focuses on understanding and implementing fundamental aspects of HTTP servers, including handling HTTP request syntax, managing TCP connections for client-server communication, and providing basic functionalities such as serving files, handling user-agent requests, and echoing client input.

## Features
- GET Requests: Serve files from a specified directory.
- POST Requests: Accept data from clients to create or update files.
- User-Agent Requests: Retrieve and respond with the User-Agent header from incoming requests.
- Echo Requests: Echo back specified content from client requests.
- Error Handling: Return appropriate HTTP status codes (e.g., 404 Not Found, 500 Internal Server Error) for different error scenarios.

## Usage
To use the HTTP server, follow these steps:

1. Clone the Repository

`git clone https://github.com/your-username/http-server-python.git`

`cd http-server-python`

2. Run the Server

`python http_server.py [directory_path]`

Replace `[directory_path]` with the absolute path to the directory where files should be stored and retrieved.

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (git checkout -b feature/improvement).
3. Make your changes.
4. Commit your changes (git commit -am 'Add new feature').
5. Push to the branch (git push origin feature/improvement).
6. Create a new Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.
