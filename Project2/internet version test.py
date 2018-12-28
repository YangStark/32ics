import socket
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

def conduct_connectfour_conversation(host:str, port:int) ->None:
    c4socket = socket.socket()
    try:
        print("Connecting...")
        c4socket.connect((host,port))
        print("connection established")
        while True:
            c4message = input("your move")
            out = in_out(c4message,c4socket)
            print(out)
                
    finally:
        print('Closing connection')
        c4socket.close()

    print('Goodbye!')

def in_out(inp:str,c4socket:socket) ->str:
    bytes_to_send = (inp+"\r\n").encode(encoding="utf-8")
    c4socket.send(bytes_to_send)
    while True:
        print("enter whileloop")
        outputbytes = c4socket.recv(4096)
        output = outputbytes.decode(encoding="utf-8").rstrip().split("\n")
        print("output")
        for soutput in output:
            print("PARTICAL")
            if type(eval(soutput.strip()[-1])) == int:
                return soutput.strip()
        if output[0] == "ERROR":
            break
        elif output[-1] == "READY":
            break
        elif output[0].split()[0] == "WELCOME":
            break

if __name__ == '__main__':
    conduct_connectfour_conversation(read_host(), read_port())

                    
