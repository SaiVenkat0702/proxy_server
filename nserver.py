import socket
import threading

def handle_client(client_socket):
    s = None
    try:
        request = client_socket.recv(1024)
        print(f"Received Request:\n{request.decode('utf-8')}")

        # Parse the first line of the request to get the URL
        first_line = request.decode('utf-8').split('\n')[0]
        url = first_line.split(' ')[1]

        # Find the webserver and port
        http_pos = url.find("://")
        if (http_pos == -1):
            temp = url
        else:
            temp = url[(http_pos+3):]

        port_pos = temp.find(":")
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)

        webserver = ""
        port = -1
        if (port_pos == -1 or webserver_pos < port_pos):
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
            webserver = temp[:port_pos]

        # Create a socket to connect to the web server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1000)  # Set a timeout on socket operations
        s.connect((webserver, port))
        s.sendall(request)

        while True:
            # Receive data from web server
            data = s.recv(4096)
            if len(data) > 0:
                # Send to browser
                client_socket.send(data)
            else:
                break
    except ConnectionResetError as e:
        print(f"Connection was reset: {e}")
    except socket.timeout as e:
        print(f"Socket operation timed out: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if s is not None:
            s.shutdown(socket.SHUT_RDWR)  # Graceful shutdown
            s.close()
        client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('127.0.0.1', 8888))
    server_socket.listen(5)
    print("Proxy Server Running on port 8888...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Received connection from {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == '__main__':
    main()
