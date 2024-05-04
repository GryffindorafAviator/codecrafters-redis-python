import socket
import threading


def handle_client(client_socket):
    print("Connected by", client_socket.getpeername())
    while True:
        data = client_socket.recv(1024).decode().strip()
        if not data:
            break
        response = "+PONG\r\n"
        client_socket.sendall(response.encode())
    client_socket.close()


def main():
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    while True:
        client_socket, _ = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()
    server_socket.close()


if __name__ == "__main__":
    main()
