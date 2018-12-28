import function_for_connection as c4connect
import connectfour
import local_version

'''
ICS 32 Project 2
UCI_ID:16452673   Name: Zian Yang
UCI_ID:88474044   Name: Yu Zhang
'''

def manual() ->None:
    print("Hi Welcome to the connect four game!")
    print("The input should follow the format 'drop 2' or 'POP 1'.")
    print("And second number is the target column.")


def getusername() ->str:
    while True:
        name = input("Please enter a user name")
        if " " not in name:
            return name
        else:
            print("User name cannot have whitespece in it.")
            continue

def gethost() ->str:
    while True:
        host = input("Please specify a host to connect")
        if host != "":
            return host
        else:
            print("Host cannot be empty")
            continue

def inputmove() ->str:
    while True:
        rawinfo = input("Please input your move")
        move = rawinfo.lower().split()
        if move[0] in ["drop","pop"] and type(eval(move[1])) == int and len(move)==2:
            return " ".join(move).upper()
        else:
            return rawinfo

def makemove(game_state,cmdline:str):
    cmd,col = cmdline.split()[0],int(cmdline.split()[1])-1
    if cmd == "DROP":
        New_Game = connectfour.drop(game_state,col)
    elif cmd == "POP":
        New_Game = connectfour.pop(game_state,col)
    return New_Game
                
def maininterface():
    user_name = getusername()
    host = gethost()

    print("connecting user to the host")
    
    try:
        connection = c4connect.connect(host,4444)
               
        print("connection established")
        
    ###start game on server
        firstmessage = "I32CFSP_HELLO "+user_name
        c4connect.send_message(connection,firstmessage)
        response = c4connect.receive_response(connection)
        print(response.strip())
        secondmessage = "AI_GAME"
        c4connect.send_message(connection,secondmessage)
        response = c4connect.receive_response(connection)
        print(response)
        
    ###actual game start
        New_Game = connectfour.new_game()
        manual()
        local_version.printstate(New_Game.board)
        while True:###for different moves
            usermove = inputmove()
            c4connect.send_message(connection,usermove)
            k = []
            while True:###for entire message
                response = c4connect.receive_response(connection)
                if response == "":
                    break
                k.append(response)
                if response == "READY":
                    break
                elif response == "WINNER_RED":
                    break
            if len(k) == 1:
                if k[0] == "ERROR":
                    print("Your input does not conform to the protocol")
                    print("Disconnecting")
                    c4connect.close(connection)
                    break
                elif k == ["WINNER_RED"]:
                    New_Game = makemove(New_Game,usermove)
                    local_version.printstate(New_Game.board)
                    print("The winner is {}".format(k[0].split("_")[1]))
                    print("The Game ended, disconnecting...")
                    c4connect.close(connection)
                    print("Disconnected")
                    break
            else:    
                if k[1].split()[0] in ["DROP","POP"]:
                    New_Game = makemove(New_Game,usermove)
                    New_Game = makemove(New_Game,k[1])
                    print("\nYour rival's move is",k[1])
                    local_version.printstate(New_Game.board)
                    if k[2].split("_")[0] == "WINNER":
                        print("The winner is {}".format(k[2].split("_")[1]))
                        print("The Game ended, disconnecting...")
                        c4connect.close(connection)
                        print("Disconnected")
                        break
                elif len(k) == 2:
                    print("You cannot do this move,")
                    continue
    except c4connect.socket.gaierror:
        print("Cannot get connection")
        print("Byebye")
    
            
if __name__ == "__main__":
    maininterface()














    
