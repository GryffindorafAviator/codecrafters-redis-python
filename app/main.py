import socket
import threading

database = {}


def handle_client(client_socket):
    print("Connected by", client_socket.getpeername())
    while True:
        data = client_socket.recv(1024).decode("utf-8").strip()
        if not data:
            break
        data_arr = data.split('\r\n')
        cmd = data_arr[2].upper()
        if cmd == "ECHO":
            msg = data_arr[4]
            response = f"${len(msg)}\r\n{msg}\r\n"
        elif cmd == "SET":
            database[data_arr[4]] = data_arr[6]
            response = "+OK\r\n"
        elif cmd == "GET":
            if data_arr[4] in database:
                value = database[data_arr[4]]
                response = f"${len(value)}\r\n{value}\r\n"
            else:
                response = "$-1\r\n"
        else:
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
