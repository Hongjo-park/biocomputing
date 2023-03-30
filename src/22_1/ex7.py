import math
import datetime
import sys
from tqdm import tqdm
BP = set()
MF = set()
BP_P = {}
MF_P = {}
BP_C = {}
MF_C = {}
BP_A = {}
MF_A = {}
BP_Direct = set()
MF_Direct = set()
MF_Direct_Term = {}
BP_Direct_Term = {}
BP_Annotation_term = {}
MF_Annotation_term = {}
BP_Inferred = {}
MF_Inferred = {}
BPA={}
MFA={}
BPrnode = ''
MFrnode = ''

def readOntology(ontologyfile):
    global BP,MF,BPrnode,MFrnode
    is_obsolate = False
    Term = False
    namespace =''
    with open(ontologyfile, 'r') as file:
        lines = file.readlines()

        for line in lines:
            read = line.split()
            if Term and not is_obsolate:
                if line.startswith('id'):
                    id = line[4:-1]
                elif line == 'is_obsolete: true\n':
                    is_obsolate = True
                elif line.startswith('namespace'):
                    namespace = read[1]
                elif line.startswith('\n'):
                    Term = False
                    if namespace == 'biological_process':
                        BP.add(id)
                    elif namespace == 'molecular_function':
                        MF.add(id)
            else:
                if line.startswith('[Term]'):
                    Term = True
                    is_obsolate = False
        for i in BP:
            BP_P[i] = set()
            BP_C[i] = set()
        for i in MF:
            MF_P[i] = set()
            MF_C[i] = set()

        is_obsolate = False
        Term = False
        data = set()
        namespace =''
        for line in lines:
            read = line.split()
            if Term and not is_obsolate:
                if line.startswith('id'):
                    id = line[4:-1]
                elif line == 'is_obsolete: true\n':
                    is_obsolate = True
                elif line.startswith('is_a'):
                    data.add(read[1])
                elif line.startswith('relationship: part_of'):
                    data.add(read[2])
                elif line.startswith('namespace'):
                    namespace = read[1]
                elif line.startswith('\n'):
                    Term = False
                    if namespace == 'biological_process':
                        for i in data:
                            if i in BP:
                                BP_P[id].add(i)
                                BP_C[i].add(id)
                        if data == set():
                            BPrnode = id
                    elif namespace == 'molecular_function':
                        for i in data:
                            if i in MF:
                                MF_P[id].add(i)
                                MF_C[i].add(id)
                        if data == set():
                            MFrnode = id
                    data = set()
            else:
                if line.startswith('[Term]'):
                    Term = True
                    is_obsolate = False
    for i in MF_P:        
        for k in MF_P[i]:
            if k in BP_P:
                if k in MF_P[i]:
                    MF_P[i].remove(k)
                    print(MF_P[i])
def Parents(go, C, P, C_A):
    if go == BPrnode or go == MFrnode:
        C_A[go] = set()
    else:
        C_A[go] = C_A[go]|P[go]
        for item in P[go]:
            C_A[go] = C_A[go]|C_A[item]
    for go_c in C[go]:
        Parents(go_c, C, P, C_A)

def Inferred(go, C, Direct,Inffered):
    for go_c in C[go]:
        Inferred(go_c, C, Direct, Inffered)
    Inffered[go] = Direct[go]
    for go_c in C[go]:
        Inffered[go] = Inffered[go]|Inffered[go_c]
def readHuman(humanfile):
    for i in BP_P:
        BP_Direct_Term[i] = set()
        BP_Inferred[i] = set()
        BP_A[i] = set()
    for i in MF_P:
        MF_Direct_Term[i] = set()
        MF_Inferred[i] = set()
        MF_A[i] = set()
    with open(humanfile, 'r') as file:
        for line in file:
            if not line.startswith('!'):
                read = line.split('\t')
                if not 'IEA' == read[6] and not read[3] == 'NOT':
                    if read[8] == 'P':
                        BP_Direct_Term[read[4]].add(read[2])
                        BP_Direct.add(read[2])
                    elif read[8] == 'F':
                        MF_Direct_Term[read[4]].add(read[2])
                        MF_Direct.add(read[2])
    for item in BP_Direct:
        BP_Annotation_term[item] = set()
    for item in MF_Direct:
        MF_Annotation_term[item] = set()

    for i, v in BP_Direct_Term.items():
        for go in v:
            BP_Annotation_term[go].add(i)

    for i, v in MF_Direct_Term.items():
        for go in v:
            MF_Annotation_term[go].add(i)

def readppi(ppifile):
    ppi = []
    MF_length = len(MF_Direct)
    BP_length = len(BP_Direct)
    with open(ppifile, 'r') as file:
        lines = file.readlines()
    for line in tqdm(lines):
        read = line.rstrip('\n').split('\t')
        bpppi = 0
        mfppi = 0
        bpflag = False
        mfflag = False
        if read[0] in BP_Direct and read[1] in BP_Direct: 
            best = []
            for i in BP_Annotation_term[read[0]]:
                data = []
                for j in BP_Annotation_term[read[1]]:
                    BP_intersect = BP_A[i]&BP_A[j]
                    if (len(BP_Inferred[i]) == 0 and len(BP_Inferred[j]) == 0) or len(BP_intersect) == 0:
                        bp = 0
                    else:
                        temp = len(BP_Direct)
                        for k in BP_intersect:
                            if temp > len(BP_Inferred[k]):
                                temp = len(BP_Inferred[k])
                        bp = 2 * math.log2(temp/BP_length) / (math.log2(len(BP_Inferred[i])/BP_length) + math.log2(len(BP_Inferred[j])/BP_length))
                    data.append(bp)
                best.append(max(data))
            for i in BP_Annotation_term[read[1]]:
                data = []
                for j in BP_Annotation_term[read[0]]:
                    BP_intersect = BP_A[i]&BP_A[j]
                    if (len(BP_Inferred[i]) == 0 and len(BP_Inferred[j]) == 0) or len(BP_intersect) == 0:
                        bp = 0
                    else:
                        temp = len(BP_Direct)
                        for k in BP_intersect:
                            if temp > len(BP_Inferred[k]):
                                temp = len(BP_Inferred[k])
                        bp = 2 * math.log2(temp/BP_length) / (math.log2(len(BP_Inferred[i])/BP_length) + math.log2(len(BP_Inferred[j])/BP_length))
                    data.append(bp)
                best.append(max(data))

            bpppi = sum(best) / len(best)
            bpflag = True
        if read[0] in MF_Direct and read[1] in MF_Direct:
            best = []
            for i in MF_Annotation_term[read[0]]:
                data = []
                for j in MF_Annotation_term[read[1]]:
                    MF_intersect = MF_A[i]&MF_A[j]
                    if len(MF_intersect) == 0:
                        mf = 0
                    else:
                        if len(MF_Inferred[i]) == 0 and len(MF_Inferred[j]) == 0:
                            mf = 0
                        else:
                            temp = len(MF_Direct)
                            for k in MF_intersect:
                                if temp > len(MF_Inferred[k]):
                                    temp = len(MF_Inferred[k])
                            mf = 2 * math.log2(temp/MF_length) / (math.log2(len(MF_Inferred[i])/MF_length) + math.log2(len(MF_Inferred[j])/MF_length))
                    data.append(mf)
                best.append(max(data))
            for i in MF_Annotation_term[read[1]]:
                data = []
                for j in MF_Annotation_term[read[0]]:
                    MF_intersect = MF_A[i]&MF_A[j]
                    if len(MF_intersect) == 0:
                        mf = 0
                    else:
                        if len(MF_Inferred[i]) == 0 and len(MF_Inferred[j]) == 0:
                            mf = 0
                        else:
                            temp = len(MF_Direct)
                            for k in MF_intersect:
                                if temp > len(MF_Inferred[k]):
                                    temp = len(MF_Inferred[k])
                            mf = 2 * math.log2(temp/MF_length) / (math.log2(len(MF_Inferred[i])/MF_length) + math.log2(len(MF_Inferred[j])/MF_length))
                    data.append(mf)
                best.append(max(data))

            mfppi = sum(best) / len(best)
            mfflag = True
        if bpflag or mfflag:
            ppi.append(max(bpppi,mfppi))
    return ppi
def main(file1,file2,file3):
    readOntology(file1)
    readHuman(file2)
    Parents(BPrnode, BP_C, BP_P, BP_A)
    Parents(MFrnode, MF_C, MF_P, MF_A)
    Inferred(BPrnode, BP_C, BP_Direct_Term,BP_Inferred)
    Inferred(MFrnode, MF_C, MF_Direct_Term,MF_Inferred)
    start = datetime.datetime.now()
    result = readppi(file3)
    end = datetime.datetime.now()
    elapsed_time = end - start
    ppicount = 0
    for i in range(11):
        count = 0
        for j in result:
            if i <= 10 * j and i + 1 > 10 * j:
                count += 1
                ppicount+=1
        print(f'{i/10} = {count}')
    print(ppicount)
    print(f'{elapsed_time.microseconds} microseconds')
    import matplotlib.pyplot as plt
    plt.hist(result, bins=[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
    plt.xlabel('Value')
    plt.ylabel('Counts')
    plt.title('Histogram Plot of Data')
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2],sys.argv[3])