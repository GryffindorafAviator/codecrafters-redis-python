import socket
import threading
import time

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
            value = data_arr[6]
            if len(data_arr) > 7:
                expiry = int(data_arr[10])
                database[data_arr[4]] = (value, time.time() + expiry / 1000)
            response = "+OK\r\n"
        elif cmd == "GET":
            key = data_arr[4]
            if key in database:
                value, expire = database[data_arr[4]]
                if time.time() < expire:
                    response = f"${len(value)}\r\n{value}\r\n"
                else:
                    del database[key]
                    response = "$-1\r\n"
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
