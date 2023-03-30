is_obsolate = False
Term = False
flag_part = False
flag_is = False
data = {}
part_of = []
is_a = []
BP = {}
MF = {}
count3 = 0
namespace =''
MFrnode = ''
BPrnode = ''
four = []

def cal_depth(key,root,data):
    length = 0
    parent = list(set(data[key]['is_a']+data[key]['part_of']))
    while(1):
        if key is root:
            break
        elif root in parent:
            length += 1
            break
        else:
            length += 1
            next = set()
            for i in parent:
                next.update(list(set(data[i]['is_a']+data[i]['part_of'])))
            parent = next
    return length

def depth(root,data):
    depth = []
    for key in data.keys():
        i = cal_depth(key,root,data)
        depth.append(i)
    return depth

with open('ontology.obo', 'r') as file:
    lines = file.readlines()
for line in lines:
    read = line.split()
    if Term and not is_obsolate:
        if line.startswith('id'):
            id = line[4:-1]
        elif line == 'is_obsolete: true\n':
            is_obsolate = True
        elif line.startswith('is_a'):
            is_a.append(read[1])
        elif line.startswith('relationship: part_of'):
            part_of.append(read[2])
        elif line.startswith('namespace'):
            namespace = read[1]
        elif line.startswith('\n'):
            Term = False
            data['is_a'] = is_a
            data['part_of'] = part_of
            if namespace == 'biological_process':
                BP[id] = data
                if not is_a and not part_of:
                    BPrnode = id
            elif namespace == 'molecular_function':
                MF[id] = data
                if not is_a and not part_of:
                    MFrnode = id
            is_a = []
            part_of = []
            data ={}
    else:
        if line.startswith('[Term]'):
            Term = True
            is_obsolate = False
BPid = []
for i in MF:        
    for k in MF[i]['is_a']+MF[i]['part_of']:
        if k in BP:
            count3 += 1
            if k in MF[i]['part_of']:
                MF[i]['part_of'].remove(k)
            if k in MF[i]['is_a']:
                MF[i]['is_a'].remove(k)

for i in MF:
    if set(MF[i]['is_a']) & set(MF[i]['part_of']):
        four.append(set(MF[i]['is_a'] + MF[i]['part_of']))
for i in BP:
    if set(BP[i]['is_a']) & set(BP[i]['part_of']):
        four.append(set(BP[i]['is_a'] + BP[i]['part_of']))
configure = []
configure1 = []
id = []
id1 = []
for i in BP:
    configure += BP[i]['is_a'] + BP[i]['part_of']
    id.append(i)
for i in MF:
    configure1 += MF[i]['is_a'] + MF[i]['part_of']
    id1.append(i)

print(f'The number of Terms : MF = {len(MF)} BP = {len(BP)}')
print('RootNode ID : MF = {} BP = {}'.format(MFrnode,BPrnode))
print(f'The number of error : {count3}')
print(f'The Pair of Terms : {four}')
print(f'The number of Leaf terms : MF = {len(set(id1) - set(configure1))} BP = {len(set(id) - set(configure))}')

BPdepth = depth(BPrnode,BP)
for i in range(max(BPdepth)+1):
    print(f'{i} = {BPdepth.count(i)}')

MFdepth = depth(MFrnode,MF)
for i in range(max(MFdepth)+1):
    print(f'{i} = {MFdepth.count(i)}')