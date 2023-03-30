import sys
import datetime
import os
from typing import Pattern

string={}

def findString(file1,file2):
    global string
    i=0
    for j in [f'{file1}',f'{file2}']:
        count = 0
        if os.path.isfile(j):
            j = open(j, 'r')
            for line in j.readlines():
                if count == 2: # Find first sequence
                    break
                else:
                    string[i] = line.upper().strip('\n').split('\t')
                    if string[i][0] == '':
                        print('No string found')
                        quit()
                    i += 1
                count += 1
            j.close()
        else:
            print("No input file")
            quit()

def makeTable(P):
    table = [0]*len(P)
    i = 0
    for j in range(1,len(P)):
        while i > 0 and P[i] != P[j]:
            i = table[i-1]
        if P[i] == P[j]:
            i += 1
            table[j] = i
    return table

def KMP(P,T):
    result = []
    table = makeTable(P)
    i = 0
    for j in range(len(T)):
        while i > 0 and P[i] != T[j]:
            i = table[i-1]
        if P[i] == T[j]:
            if i == len(P)-1:
                result.append(j-len(P)+1)
                i = table[i]
            else:
                i += 1
    return result

def main(file1,file2):
    global string
    findString(file1,file2)
    if len(string[0][0]) > len(string[1][0]):
        T = string[0][0]
        P = string[1][0]
    else:
        T = string[1][0]
        P = string[0][0]
    start = datetime.datetime.now()
    result = KMP(P,T)
    end = datetime.datetime.now()
    if result == []:
        print('No match found')
        quit()
    else:
        print(*result)
    elapsed_time = end - start
    print(f'{elapsed_time.microseconds} microseconds')

if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2])