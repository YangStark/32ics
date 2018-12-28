import socket
def read_host() ->str:
    
    while True:
        host = input('Host: ').strip()

        if host == '':
            print('Please specify a host (either a name or an IP address)')
        else:
            return host

def read_port() -> int:

    while True:
        try:
            port = int(input('Port: ').strip())

            if port < 0 or port > 65535:
                print('Ports must be an integer between 0 and 65535')
            else:
                return port

        except ValueError:
            print('Ports must be an integer between 0 and 65535')

def read_message() -> str:
    return input('Message: ')



def print_response(response: str) -> None:
    print('Response: ' + response)

def connect(host: str, port: int) -> 'connection':
    echo_socket = socket.socket()
    echo_socket.connect((host, port))
    echo_socket_input = echo_socket.makefile('r')
    echo_socket_output = echo_socket.makefile('w')
    return echo_socket, echo_socket_input, echo_socket_output

def close(connection: 'connection') -> None:
    echo_socket, echo_socket_input, echo_socket_output = connection

    echo_socket_input.close()
    echo_socket_output.close()
    echo_socket.close()

def send_message(connection: 'connection', message: str) -> None:
    echo_socket, echo_socket_input, echo_socket_output = connection
    echo_socket_output.write(message + '\r\n')
    echo_socket_output.flush()



def receive_response(connection: 'connection') -> None:
    echo_socket, echo_socket_input, echo_socket_output = connection
    k = []
    while True:
        b = echo_socket_input.readline()
        k.append(b)
        if b == "":
            break
    return k


def user_interface() -> None:
    host = read_host()
    port = read_port()

    print('Connecting to {} (port {})...'.format(host, port))
    connection = connect(host, port)
    print('Connected!')

    while True:
        message = read_message()

        if message == '':
            break
        else:
            send_message(connection, message)
            response = receive_response(connection)
            print_response(response)

    print('Closing connection...')
    close(connection)
    print('Closed!')
if __name__ == '__main__':
    user_interface()

