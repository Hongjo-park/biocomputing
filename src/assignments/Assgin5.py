# 2019253050 오시현 바이오컴퓨팅 assignment5

import re
import sys
import time
import os
import numpy as np
out1,out2='',''                                    #lcs를 담을 문자열

# 파일을 열어 내용을 읽어들임
try:
    with open(sys.argv[1], 'r') as f:
        lines = f.readlines()
        if os.stat(sys.argv[1]).st_size==0:         #파일이 비워져 있으면 "No DNA sequence" 출력
            print("No protein sequence")
            sys.exit()
except FileNotFoundError:
    print("No input file")
    sys.exit()
f.close()

# FASTA 형식에 맞는지 검사
if lines[0][0] != '>':
    print("No correct format")
    sys.exit()

# 내용을 pro에 읽어들임
pro1 = ''
pro2 = ''
c2f=1
for line in lines[1:]:
    if line[0] == '>':                  #fasta 내용이 3개 이상이면 두번쨰 sequence까지만 처리
        c2f+=1
        if c2f>2:break
        continue
    if c2f==1:pro1 += line.strip()
    elif c2f==2:pro2+=line.strip()
if c2f==1:
    print("Need one more sequence")     #fasta format이 1개인 경우 need one more sequence 출력
    sys.exit()
pro1=pro1.replace(' ','').upper()
pro2=pro2.replace(' ','').upper()

# 입력 서열이 protein 서열인지 검사
p=re.compile('[A-Z]+$')
check=p.match(pro1+pro2)
if check==None:
    print('No protein sequence') 
    sys.exit(0)

pro1=" "+pro1                           #비교할 pro들에 길이+1 for 계산의 용이성
pro2=" "+pro2
a,b=len(pro1),len(pro2)
global table                            #LCS탐색에 사용할 table 초기화
table = [[0 for c in range(b)] for d in range(a)]

#blosum62를 불러오는 함수
def getstable(scoreT):
    with open(scoreT) as f:
        data=f.read()
    lines=data.strip().split("\n")      
    colh=lines.pop(0)                   #첫 줄을 읽어 colum의 head로 삼는다
    cols=colh.split()
    matrix={}
    for rowline in lines:               #그 다음줄을 읽어 첫 문자를 row의 head로 삼는다
        rowh=rowline.split()
        row=rowh.pop(0)
        matrix[row]={}
        for col in cols:
            matrix[row][col]=rowh.pop(0)
    return matrix
stable=getstable("BLOSUM62.txt")      #blosum62기반 BLOSUM62.txt를 stable에 할당

#규칙에 맞게 table을 생성하는 함수
def lcs(a,b): 
    global table
    for i in range(1,a):
        for j in range(1,b):
            if pro1[i] in pro2[j]:
                table[i][j] = table[i-1][j-1] + int(stable[pro1[i]][pro2[j]])
            else:
                table[i][j] = max(0,table[i-1][j] - 5, table[i][j-1] - 5, table[i-1][j-1] + int(stable[pro1[i]][pro2[j]]))
    
#table내 주어진 위치에서 LCS를 찾는 함수
def backtroute(x, y):
    global table, out1, out2
    while table[x][y] != 0:
        if pro1[x] == pro2[y]:
            out1 += pro1[x]
            out2 += pro2[y]
            x -= 1
            y -= 1
        else:
            if table[x][y] == int(stable[f'{pro1[x]}'][f'{pro2[y]}']) + table[x-1][y-1]:
                out1 += pro1[x]
                out2 += pro2[y]
                x -= 1
                y -= 1
            elif table[x][y-1] >= table[x-1][y]:
                out1 += '-'
                out2 += pro2[y]
                y -= 1
            elif table[x][y-1] < table[x-1][y]:
                out1 += pro1[x]
                out2 += '-'
                x -= 1
    return out1[::-1], out2[::-1]

    
start_time = time.time()        
lcs(a,b)                                #a,b= pro1,pro2의 길이
x,y=0,0
for i in range(a):                      #score가 최대인 위치를 찾는다
    for j in range(b):
        if table[x][y] >= table[i][j]:
            continue
        else:
            y = j
    if table[x][y] >= table[i][j]:
        continue
    else:
        x = i
out1,out2=backtroute(x,y)
end_time=time.time()
with open("out1.txt","w") as f:
    for i in range(int(len(out1)/60+1)):
        f.write(out1[i*60:(i+1)*60]+'\n')
        f.write(out2[i*60:(i+1)*60]+'\n\n')
    f.write('Similarity Score: {}'.format(table[x][y]))
print("Elapsed time:", int((end_time - start_time) * 1000000), "microseconds")
