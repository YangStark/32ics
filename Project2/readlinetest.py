openf = open("asdf.txt","r")
k = []
while True:
    n = openf.readline()
    k.append(n)
    if n == "":
        print("end")
        print(k)
        break
