from pathlib import Path
import os
import shutil

def sortlbd(flist:list):
    return sorted(flist,key = lambda x:(str(x).count("\\"),str(x).count("/"),str(x)))
    

def iteronlyfile(k:Path):
    d = Path(k)
    flist = []
    for element in d.iterdir():
        if element.is_file():
            flist.append(Path(element))
        else:
            pass
    return sortlbd(flist)

def iterfile(dirc:Path):
    d = Path(dirc)
    flist = []
    for element in d.iterdir():
        if element.is_file():
            flist.append(Path(element))
        else:
            flist += iterfile(element)
    return sortlbd(flist)

def A(flist):
    return flist

def N(flist:list,filename:str):
    rlist = []
    for address in flist:
        fname = str(address).split("\\")[-1]
        if fname == filename:
            rlist.append(address)
    return rlist

def E(flist:list,ext:str):
    rlist =[]
    if ext[0]==".":
        ext = ext[1:]
    for address in flist:
        fext = str(address).split(".")[-1]
        if fext == ext:
            rlist.append(address)
    return rlist

def T(flist:list,txt:str):
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

def gt(flist:list,size:int):
    rlist = []
    for address in flist:
        if address.stat().st_size > size:
            rlist.append(address)
    return rlist

def lt(flist:list,size:int):
    rlist = []
    for address in flist:
        if address.stat().st_size < size:
            rlist.append(address)
    return rlist

def F(flist:list):
    for address in flist:
        openf = open(address,"r")
        try:
            print(openf.readline()[0:-1])
            openf.close()
        except UnicodeDecodeError:
            print("NOT TEXT")

def D(flist:list):
    for address in flist:
        k = Path(str(address)+".dup")
        shutil.copyfile(address,k)

def T2(flist:list):
    for address in flist:
        os.utime(address)

def readin1():
    while True:
        k = input("")
        cmdlist = k.split()
        if len(cmdlist)>2:
            print("ERROR")
            continue
        try:
            command,dirc = str(k.split()[0]),Path(k.split[1])
            openf = open(dirc,"r")
            openf.close()
            if command in ["R","D"]:
                break
            else:
                continue
        except FileNotFoundError or command not in ["R","D"] or IndexError:
            print("ERROR")
    if command == "D":
        r = iteronlyfile(dirc)
        for address in r:
            print(address)
    elif command == "R":
        r = iterfile(dirc)
        for address in r:
            print(address)
    return r

def readin2(flist:[Path]):
    while True:
        k =  input("")
        if k == "A":
            return flist
        cmdlist = k.split()
        elif len(cmdlist)==2 and cmdlist[0] in ["N","E",">","<"]:
            if cmdlist[0]=="N":
                return N(flist,cmdlist[1])
            elif cmdlist[0]=="E":
                return E(flist,cmdlist[1])
            elif cmdlist[0]=='>':
                return gt(flist,int(cmdlist[1]))
            else:
                return lt(flist,int(cmdlist[1]))
        elif len(cmdlist)>= 2 and cmdlist[0] == "T":
            text = " ".join(cmdlist[1:])
            return T(flist,text)
        else:
            print("ERROR")
            continue

def readin3(flist:[Path]):
    if flist == []:
        return None
    else:
        while True:
            k = input("")
            if k in (i for i in "FDT"):
                if k=="F":
                    F(flist)
                elif k=="D":
                    D(flist)
                else:
                    T2(flist)
                break
            else:
                print("ERROR")
            
                
                
            
    
    
        
