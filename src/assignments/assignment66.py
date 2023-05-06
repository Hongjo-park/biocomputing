import re
import sys
import time
import os
import numpy as np
table=[]

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

c2f=-1#lines.count('>')
prolist=[]
pro=''
for line in lines[1:]:
    if line[0] == '>': 
        if pro!='':
            prolist.append(pro)                
        c2f+=1
        pro=''
        continue
    pro+=line.strip()
prolist.append(pro)
if c2f==0:
    print("Need one more sequence")     #fasta format이 1개인 경우 need one more sequence 출력
    sys.exit()

# 입력 서열이 protein 서열인지 검사
for seq in prolist:
    p=re.compile('[a-zA-Z]+$')
    check=p.match(seq)
    if check==None:
        print('No protein sequence') 
        sys.exit(0)
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

def mkgloT(seq1,seq2):
    global table,stable
    seq1=' '+seq1
    seq2=' '+seq2
    table=[[0 for c in range(len(seq2))] for d in range(len(seq1))]
    for i in range(len(seq1)):table[i][0]=i*(-5)
    for j in range(len(seq2)):table[0][j]=j*(-5)
    for i in range(1,len(seq1)):
            for j in range(1,len(seq2)):
                table[i][j] = max(table[i-1][j-1] + int(stable[seq1[i]][seq2[j]]),table[i-1][j] - 5, table[i][j-1] - 5)

pair_set=[]
score_set=[0 for i in range(len(prolist))]

def backtroute(seq1,seq2):
    global table
    seq1=' '+seq1
    seq2=' '+seq2
    out1, out2='',''
    x,y=len(seq1)-1,len(seq2)-1  
    while x>=0 or y>=0:
        if seq1[x] == seq2[y]:
            out1 += seq1[x]
            out2 += seq2[y]
            x -= 1
            y -= 1
        elif x!=0 and y!=0:
            if table[x][y] == int(stable[f'{seq1[x]}'][f'{seq2[y]}']) + table[x-1][y-1]:
                out1 += seq1[x]
                out2 += seq2[y]
                x -= 1
                y -= 1
            elif table[x][y-1] >= table[x-1][y]:
                out1 += '-'
                out2 += seq2[y]
                y -= 1
            elif table[x][y-1] < table[x-1][y]:
                out1 += seq1[x]
                out2 += '-'
                x -= 1
        elif x==0 or y==0:
            if table[x][y-1] >= table[x-1][y]:
                out1 += '-'
                out2 += seq2[y]
                y -= 1
            elif table[x][y-1] < table[x-1][y]:
                out1 += seq1[x]
                out2 += '-'
                x -= 1
    return out1[::-1]

def pairwise(seq1, seq2):
    mkgloT(seq1, seq2)
    score=table[len(seq1)][len(seq2)]
    p1=backtroute(seq1, seq2)
    return p1[1:],score

def center(plist):
    global pair_set,score_set
    for i in range(len(plist)):
        pair_rows=[]
        score=0
        for j in range(len(plist)):
            pairbuf,point=pairwise(plist[i], plist[j]) #i-j비교시 i의 결과를 저장
            if i==j:point=0
            pair_rows.append(pairbuf)
            score+=point
        score_set[i]=score
        pair_set.append(pair_rows)
    return score_set.index(max(score_set))

mset=['0' for i in range(len(prolist))]
def msa(plist,ct):
    global mset,pair_set
    pstr=''
    if ct==0:
        mset[ct]=pair_set[ct][1]
        mset[1]=pair_set[1][0]
        start=2
    else:
        mset[ct]=pair_set[ct][0]
        mset[0]=pair_set[0][ct]
        start=1
    for i in range(start,len(plist)):
            if i==ct:continue
            mset[i]=pair_set[i][ct]
            pstr=''
            adj=0
            j=0
            while True:
                if j==len(mset[ct]) or j-adj==len(pair_set[i][ct]):
                    if j==len(mset[ct]) and j-adj==len(pair_set[i][ct]): break
                    elif j==len(mset[ct]):
                        pstr+=mset[i][j-adj]
                        msagaps=''
                        for k in range(len(pair_set[i][ct])-len(mset[ct])): msagaps+='-'
                        for k in range(i): mset[k]+=msagaps
                        break
                    elif j-adj==len(pair_set[i]):
                        psagaps=''
                        for k in range(len(mset[ct])-j):psagaps+='-'
                        pstr+=psagaps
                        break
                else:
                    if (mset[ct][j]!='-' and pair_set[ct][i][j-adj]!='-') or (mset[ct][j]=='-' and pair_set[ct][i][j-adj]=='-'):
                        pstr+=mset[i][j-adj]
                    elif mset[ct][j]=='-' and pair_set[ct][i][j-adj]!='-':
                        pstr+='-'
                        adj+=1
                    elif mset[ct][j]!='-' and pair_set[ct][i][j-adj]=='-':
                        pstr+=mset[i][j-adj]
                        mstr=''
                        for k in range(i):
                            mstr=mset[k][:j]+'-'+mset[k][j:]
                            if i>ct: mset[ct][:j] + '-' + mset[ct][j:]
                            mset[k]=mstr
                j+=1
            mset[i]=pstr

def addStar(msaset,ct):
    ctlen=len(mset[ct])
    starline=''
    for i in range(ctlen):
        check=0
        while check<len(mset):
            if mset[ct][i]!=mset[check][i]:
                starline+=' '
                break
            check+=1
        if check==len(mset):
            starline+="*"
    return starline
    
start_time = time.time()
ct=center(prolist)
msa(prolist,ct)
starline=addStar(mset,ct)
end_time=time.time()
print("Elapsed time:", int((end_time - start_time) * 1000000), "microseconds")

with open("out.txt", "w") as f:
    m=0
    while True:
        for i in range(len(mset)):
            f.write(mset[i][m:m+60]+'\n')
        f.write(starline[m:m+60]+'\n')
        f.write('\n')
        m+=60
        if m>=len(mset[ct]):
            break