import connectfour

'''
ICS 32 Project 2
UCI_ID:16452673   Name: Zian Yang
UCI_ID:88474044   Name: Yu Zhang
'''


def manual():
    print("Hi Welcome to the connect four game!")
    print("The input should follow the format 'D 2' or 'p 1'.")
    print("'D' for drop and 'P' for move and second number is the target column.")

def printstate(gameboard):
    print()
    printrow = []
    for i in range(len(gameboard[0])):
        printrow.append([])
    for columns in gameboard:
        for i in range(len(columns)):
            if columns[i] == 0:
                printrow[i].append(".")
            elif columns[i] == 1:
                printrow[i].append("R")
            elif columns[i] == 2:
                printrow[i].append("Y")
    headerint = list(range(1,8))
    b = [str(i) for i in headerint]
    printrow.insert(0,b)
    for row in printrow:
        print("  ".join(row))
    print()

def maininterface():
    New_Game = connectfour.new_game()
    manual()
    printstate(New_Game.board)
    while True:###for the different moves
        while True: ###for invalid input
            ipt = input("Now is {}'s turn, please type in the move:".format("Red" if New_Game.turn == 1 else "Yellow"))
            try:
                mov,col = ipt.split()
                if mov.lower() == "d":
                    try:
                        New_Game = connectfour.drop(New_Game,int(col)-1)
                        break
                    except connectfour.InvalidMoveError:
                        print("Entered move is invalid, please try again.")
                        continue
                elif mov.lower() == "p":
                    try:
                        New_Game = connectfour.pop(New_Game,int(col)-1)
                        break
                    except connectfour.InvalidMoveError:
                        print("Entered move is invalid, please try again.")
                        continue
                else:
                    print("Entered move is invalid, please try again.")
            except connectfour.InvalidMoveError and ValueError:
                print("Entered move is invalid, please try again.")
        printstate(New_Game.board)
        winplayer = connectfour.winner(New_Game)
        if winplayer != 0:
            print("Player {} is the winner! Game Ends.".format("Yellow" if New_Game.turn == 1 else "Red"))
            break
        else:
            continue
        
if __name__ == "__main__":
    maininterface()
