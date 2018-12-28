from pathlib import Path
import os
import shutil

def sortlbd(flist:list): ###return the sorted input list
    return sorted(flist,key = lambda x:(str(x).count("\\"),str(x).count("/"),str(x)))

def printa(flist:[Path]): ###print all the files in the list
    for address in flist:
        print(address)
    

def iteronlyfile(k:Path): ###iterate the file only under the input directory and put the path of the files into a list and return the list
    d = Path(k)
    flist = [] ###flist stands for "file list" I use this for the rest of the notation 
    for element in d.iterdir():
        if element.is_file():
            flist.append(Path(element))
        else:
            pass
    return sortlbd(flist)

def iterfile(dirc:Path):###iterate the all the files under the input directory and its subdirectories and put the path of the files into a list and return the list
    d = Path(dirc)
    flist = []
    for element in d.iterdir():
        if element.is_file():
            flist.append(Path(element))
        else:
            flist += iterfile(element)
    return sortlbd(flist)

def A(flist): ###return the original list
    return flist

def N(flist:list,filename:str): ###narrower the file list to the files which has file name match to the input text
    rlist = [] ###rlist stands for "return list" i used the notation through out rest of the program
    for address in flist:
        fname = str(address).split("\\")[-1]
        if fname == filename:
            rlist.append(address)
    return rlist

def E(flist:list,ext:str): ### narrower the file list to the files which has extension wich match to the input text
    rlist =[]
    if ext[0]==".":
        ext = ext[1:]
    for address in flist:
        fext = str(address).split(".")[-1]
        if fext == ext:
            rlist.append(address)
    return rlist

def T(flist:list,txt:str): ### narrower the file list to the files to the files which include the input text
    rlist = []
    for address in flist:
        try:
            openf = open(address,"r")
            for line in openf:
                if txt in line:
                    rlist.append(address)
            openf.close()
        except UnicodeDecodeError:
            pass
    return rlist

def gt(flist:list,size:int): ### narrower the file list to the files the files which size is greater than the input integer
    rlist = []
    for address in flist:
        if address.stat().st_size > size:
            rlist.append(address)
    return rlist

def lt(flist:list,size:int): ### narrower the file list to the files which size is smaller(less) than the input integer
    rlist = []
    for address in flist:
        if address.stat().st_size < size:
            rlist.append(address)
    return rlist

def F(flist:list): ###this function print first line of the text file
    for address in flist:
        openf = open(address,"r")
        try:
            print(openf.readline()[0:-1])
            openf.close()
        except UnicodeDecodeError:
            print("NOT TEXT")

def D(flist:list): ### this function makes duplicate of file with ".dup" at the end
    for address in flist:
        try:
            k = Path(str(address)+".dup")
            shutil.copyfile(address,k)
        except:
            continue

def T2(flist:list):###this function modifies the files' edit time
    for address in flist:
        try:
            os.utime(address)
        except:
            continue
        
def readin1(): ### the first function for read in input
    while True:
        k = input("")
        cmdlist = k.split()
        if len(cmdlist)>2:
            print("ERROR")
            continue
        try:
            command,dirc = str(k.split()[0]),Path(k.split()[1])
            if command in ["R","D"] and dirc.is_dir():
                break
            else:
                continue
        except FileNotFoundError:
            print("ERROR")
            continue
        except IndexError:
            print("ERROR")
            continue
    if command == "D":
        r = iteronlyfile(dirc)
        printa(r)
    elif command == "R":
        r = iterfile(dirc)
        printa(r)
    return r

def readin2(flist:[Path]): ### the second function for read in input
    while True:
        k =  input("")
        cmdlist = k.split()
        if cmdlist == ["A"]:
            printa(flist)
            return flist
        elif len(cmdlist)==2 and cmdlist[0] in ["N","E",">","<"]:
            if cmdlist[0]=="N":
                r = N(flist,cmdlist[1])
                printa(r)
                return r
            elif cmdlist[0]=="E":
                r = E(flist,cmdlist[1])
                printa(r)
                return r
            elif cmdlist[0]=='>':
                if int(cmdlist[1]) < 0:
                    print("ERROR")
                    continue
                r = gt(flist,int(cmdlist[1]))
                printa(r)
                return r
            else:
                if int(cmdlist[1]) < 0 :
                    print("ERROR")
                    continue
                r = lt(flist,int(cmdlist[1]))
                printa(r)
                return r
        elif len(cmdlist)>= 2 and cmdlist[0] == "T":
            text = " ".join(cmdlist[1:])
            r =  T(flist,text)
            printa(r)
            return r
        else:
            print("ERROR")
            continue

def readin3(flist:[Path]): ### the third function for read in input
    if flist == []:
        return None
    else:
        while True:
            k = input("")
            if k in ["F","D","T"]:
                if k=="F":
                    F(flist)
                elif k=="D":
                    D(flist)
                else:
                    T2(flist)
                break
            else:
                print("ERROR")

def main():
    readin3(readin2(readin1()))

if __name__ == "__main__":
    main()
                
                
            
    
    
        
