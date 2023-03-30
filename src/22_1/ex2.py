import re
import os
import datetime
import numpy as np

seqA = ""
seqB = ""
count = 0
input_file = input() # input file name

if os.path.isfile(input_file):
    file = open(input_file, 'r')    
    for line in file.readlines():
        if not line.find('>'): # Find first sequence
            if count <= 2:
                count = count +1
                continue
        if count == 1:
            seqA += "".join(line.strip().split(' ')).upper() # Remove spaces and replace capital letters
        elif count == 2:
            seqB += "".join(line.strip().split(' ')).upper() # Remove spaces and replace capital letters
    file.close()
    if seqA == "":
        print("No protein sequence")
        quit()
    if count < 1:
        print("No correct format")
        quit()    
    elif count == 1:
        print("Need one more sequence")
        quit()
else:
    print("No input file")
    quit()

p = re.compile(r'^[A-Z]*$') # Check DNA sequence
find = p.match(seqA+seqB)
if find == None:
    print("No protein sequence")
    quit()

seqA, seqB= ' ' + seqA, ' ' + seqB
a, b = len(seqA), len(seqB)
C = [[0 for c in range(b)] for d in range(a)]
seqC = ''

def LCSS(n,m): # Craete LCS matrix 
    global C
    for i in range(1,n):
        for j in range(1,m):
            if seqA[i] in seqB[j]:
                C[i][j] = C[i - 1][j - 1] + 1
            else:
                C[i][j] = max(C[i - 1][j], C[i][j - 1])
       
def backtrack(i,j): # Backtracking LCS matrix
    if i == 0 or j == 0:
        return ''
    elif seqA[i] in seqB[j]:
        return backtrack(i - 1, j - 1) + seqA[i]
    elif C[i][j-1] >= C[i-1][j]:
        return backtrack(i, j - 1)
    else:
        return backtrack(i - 1, j)

# def backtrack(i,j): # Backtracking LCS matrix
#     global seqC
#     while (1):
#         if i == 0 or j == 0:
#             return seqC
#         elif seqA[i] == seqB[j]:
#             i -= 1
#             j -= 1
#             seqC += seqA[i]
#         elif C[i][j-1] >= C[i-1][j]:
#             j -= 1
#         else:
#             i -= 1

start = datetime.datetime.now()
LCSS(a,b)
backtrack(a-1,b-1)
print(seqC)
end = datetime.datetime.now()
elapsed_time = end - start
print(f'{elapsed_time.microseconds} microseconds')
