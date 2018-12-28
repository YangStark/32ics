import socket

'''
ICS 32 Project 2
UCI_ID:16452673   Name: Zian Yang
UCI_ID:88474044   Name: Yu Zhang
'''

def read_host() ->str:
    while True:
        host = input("Host").strip()

        if len(host) == 0:
            print("Invalid host, Please re-enter.")
        else:
            return host

def read_port() ->int:
    while True:
        try:
            port = int(input("Port:").strip())

            if 0 < port < 65535:
                return port
            else:
                print("Please enter port between 0 and 65535")
        except ValueError:
            print("Please enter port between 0 and 65535")

def connect(host: str, port: int) -> 'connection':
    c4_socket = socket.socket()
    c4_socket.connect((host, port))
    c4_socket_input = c4_socket.makefile('r')
    c4_socket_output = c4_socket.makefile('w')

    return c4_socket, c4_socket_input, c4_socket_output



def close(connection: 'connection') -> None:
    c4_socket, c4_socket_input, c4_socket_output = connection
    c4_socket_input.close()
    c4_socket_output.close()
    c4_socket.close()



def send_message(connection: 'connection', message: str) -> None:
    c4_socket, c4_socket_input, c4_socket_output = connection
    c4_socket_output.write(message + '\r\n')
    c4_socket_output.flush()



def receive_response(connection: 'connection') -> str:
    c4_socket, c4_socket_input, c4_socket_output = connection
    return c4_socket_input.readline()[:-1]
