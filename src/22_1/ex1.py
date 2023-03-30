import os
import time 
import re

def overlap(st,tst,lowcom): # overlap for another sequence length
    for i in range(lowcom):
        if st[i]+6 > tst:
            return False
    return True

input_file = input() #input file name
start = time.perf_counter() 
data = "" #file data
form = False #festa format check
lowcom = 0 #low-complexity region check
startpoint = [] #startpoint list for overlap check 

if os.path.isfile(input_file):
    file = open(input_file, 'r')    
    for line in file.readlines():
        if line.find('>')==0:#Find first sequence
            if form:
                break
            else:
                form = True
                continue
        else:
            data += "".join(line.strip().split(' ')).upper()# Remove spaces and replace capital letters
    file.close()
    if form == False:
        print("No correct format")
        quit()
    if data == "":
        print("No DNA sequence")
        quit()
else:
    print("No input file")
    quit()

p = re.compile(r'^[ATCG]*$') #check DNA sequence

if p.match(data) == None:
    print("No DNA sequence")
    quit()
else:
    for i in range (2,5):
        for j in range(len(data)):
            ed = j-i*3
            if data[j-i:j] == data[j-i-i:j-i] and data[j-i-i:j-i] == data[ed:j-i-i]:#check low-complexity region
                if overlap(startpoint,ed,lowcom):
                    startpoint.append(ed)
                    lowcom += 1
                    print(ed)
    if lowcom == 0:
        print("No low-complexity region found")
        quit()
    end = time.perf_counter()
    print(f"time elapsed : {(end - start)*1000}ms")