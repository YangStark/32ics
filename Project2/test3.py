import connectfour

k = connectfour.new_game()
k = connectfour.drop(k,6)
k = connectfour.drop(k,3)
def printstate(gameboard):
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
    
printstate(k[0])

while True:
    k = connectfour.drop(k,int(input("put a column number"))-1)
    printstate(k[0])
            
        
