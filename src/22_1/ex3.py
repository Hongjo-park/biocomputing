import re
import os
import datetime
import sys
seqA = ""
seqB = ""
seqC = ""
seqD = ""
matrix =[]
C = []
a=0
b=0
def read_file(input_file):
    global seqA,seqB,matrix,C,a,b
    count = 0
    if os.path.isfile(input_file):
        file = open(input_file, 'r')    
        for line in file.readlines():
            if not line.find('>'): # Find first sequence
                if count <= 2:
                    count = count +1
                    continue
            if count == 1:
                seqA += "".join(line.strip().split(' ')).upper() # Remove spaces and replace capital letter
            elif count == 2:
                seqB += "".join(line.strip().split(' ')).upper() # Remove spaces and replace capital letters
        file.close()
        if seqA == "" or seqB == "":
            print("No protein sequence")
            quit()
        if count < 1:
            print("No correct format")
            quit()    
        if count == 1:
            print("Need one more sequence")
            quit()
    else:
        print("No input file")
        quit()
    matrix = populate_matrix('blosum62.txt')
    p = re.compile(r'^[A-Z]*$') # Check DNA sequence 
    find = p.match(seqA+seqB)
    if find == None:
        print("No protein sequence")
        quit()
    seqA, seqB = ' ' + seqA, ' ' + seqB
    a, b = len(seqA), len(seqB)
    C = [[0 for c in range(b)] for d in range(a)]

def populate_matrix(matrix_filename):
    with open(matrix_filename) as matrix_file:
      matrix = matrix_file.read()
    lines = matrix.strip().split('\n')
    header = lines.pop(0)
    columns = header.split()
    matrix = {}
    for row in lines:
      entries = row.split()
      row_name = entries.pop(0)
      matrix[row_name] = {}
      for column_name in columns:
        matrix[row_name][column_name] = entries.pop(0)
    return matrix


def LCSS(n,m): # Craete LCS matrix 
    global C
    for i in range(1,n):
        for j in range(1,m):
            if seqA[i] in seqB[j]:
                C[i][j] = C[i-1][j-1] + int(matrix[f'{seqA[i]}'][f'{seqB[j]}'])
            else:
                C[i][j] = max(C[i-1][j] - 5, C[i][j-1] - 5, C[i-1][j-1] + int(matrix[f'{seqA[i]}'][f'{seqB[j]}']))
    
def backtrack(i,j): # Backtracking LCS matrix
    global seqC,seqD
    if C[i][j] == 0:
        return ''
    if seqA[i] == seqB[j]:
        seqC += seqA[i]
        seqD += seqB[j]
        return backtrack(i-1,j-1)
    else:
        if C[i][j] == int(matrix[f'{seqA[i]}'][f'{seqB[j]}']) + C[i-1][j-1]:
            seqC += seqA[i]
            seqD += seqB[j]
            return backtrack(i-1,j-1)

        elif C[i][j-1] >= C[i-1][j]:
            seqC += '-'
            seqD += seqB[j]
            return backtrack(i,j-1)
        elif C[i][j-1] < C[i-1][j]:
            seqC += seqA[i]
            seqD += '-'
            return backtrack(i-1,j)

def main(filename):
    x=0
    y=0
    j=0
    global seqC,seqD
    read_file(filename)
    start = datetime.datetime.now()
    LCSS(a,b)
    for i in range(a):
        for j in range(b):
            if C[x][y] >= C[i][j]:
                continue
            else:
                y = j
        if C[x][y] >= C[i][j]:
            continue
        else:
            x = i
    backtrack(x,y)
    seqC = seqC[::-1]
    seqD = seqD[::-1]
    end = datetime.datetime.now()
    for i in range(int(len(seqC)/60+1)):
        print(seqC[i*60:(i+1)*60])
        print(seqD[i*60:(i+1)*60])
        print()
    print(f'Local Alignment Score: {C[x][y]}')
    elapsed_time = end - start
    print(f'{elapsed_time.microseconds} microseconds')

if __name__ == '__main__':
    main(sys.argv[1])