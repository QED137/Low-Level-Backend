# tcp_server.py
import socket  # Low-level networking module for TCP/IP communication

HOST = '127.0.0.1'  # Localhost address
PORT = 8000         # Port number to listen on

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))  # Bind the socket to host and port
    s.listen()  # Start listening for incoming connections
    print(f"Listening on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()  # Accept a new client connection
        with conn:
            request = conn.recv(1024).decode()  # Read raw HTTP request from client
            print("Received:\n", request)
            # 🧠 Manual HTTP parsing:
            # Here we check if the raw request string contains 'GET /ask'
            if "GET /ask" in request:
                # Craft raw HTTP response manually
                response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello from raw TCP!"
            else:
                # Return 404 if route not matched
                response = "HTTP/1.1 404 Not Found\r\n\r\nNot Found"
            conn.sendall(response.encode())  # Send encoded response to client
