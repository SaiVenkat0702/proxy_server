import socket

# Define server host and port
SERVER_HOST = 'localhost'
SERVER_PORT = 8888 # Replace with your PROXY_PORT

# Define the URL to send the request to
url = 'http://www.neverssl.com'  # Replace with your desired URL

# Define the GET request
request = f"GET {url} HTTP/1.1\r\nHost: {url}\r\n\r\n"

# Connect to the proxy server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Send the GET request to the proxy server
    client_socket.sendall(request.encode())

    # Receive and print the response from the proxy server
    response = client_socket.recv(4096)
    while response:
        print("Received response from proxy server:")
        print(response.decode())
        response = client_socket.recv(4096)
