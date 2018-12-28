def proj(n):
    line1()
    inbt(n)
    linee(n)

def inbt(n):
    for i in range(n):
        l1 = "  "*i+"| |"
        print(l1)
        if i== n-1:
            break
        l2 = "  "*i+"+-+-+"
        print(l2)
    
def line1():
    print("+-+")

def linee(n):
    l = "  "*(n-1)+"+-+"
    print(l)
###    print()

def main():
    k = int(input(""))
    proj(k)

main()
