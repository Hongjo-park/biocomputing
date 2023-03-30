import re, sys

# return the reverse complement sequence of a DNA sequence
# A <-> T, C <-> G
# Ex. ACCTGG -> CCAGGT

# def get_file_lines(path: str) -> list:
#     '''
#     read file.
#     remove new line and white-space
#     '''
#     return [line.strip().replace(' ', '') for line in open(path, 'r').readlines()]

# def is_dna_sequence(sequence: str) -> bool:
#     '''
#     dna sequence -> True / else -> False
#     '''
#     return re.fullmatch('(A|T|C|G|a|t|c|g)*', sequence) != None and len(sequence) >= 1

# def convert_dna_sequence(sequence: str) -> str:
#     '''
#     convert all 'A's, 'T's, 'C's, 'G's in the DNA sequence to 'T's, 'A's, 'G's, 'C's
#     '''
#     return sequence.translate(str.maketrans('ATCGatcg', 'TAGCtagc'))

# def output_reverse_complement(sequence: str, file_name='output.txt') -> None:
#     output = open(file_name, "w")
#     output.write(convert_dna_sequence(sequence[::-1]))
#     output.close()

# def main(argv):
#     '''
#     python Assignment2.py "Fill your file name or path"
#     '''
#     lines = get_file_lines(argv[1])
#     sequence = ''.join(lines[1:])

#     if is_dna_sequence(sequence):
#         output_reverse_complement(sequence, input("출력 파일 경로를 입력해주세요(ex. ./output.txt ): "))
#     else:
#         print("No DNA sequence.")


# if __name__ == '__main__':
#     main(sys.argv)

result = list()

def postprocessing_index_results(arr: list) -> list:
    res = list()
    end = 0
    for row in arr:
        res.append(row[0] + end)
        end += row[1] + 1

    return res

def get_low_complexity_region(sequence: str, n: int, l: int, leng: int) -> int:
    '''
    n : sequence 중에 현재 인덱스
    l : length of the sequence segment
    leng : length of sequence
    ''' 
    start_index = n + l
    if start_index + l > leng:
        return -1
    cnt = 1
    seg = sequence[n:n+l]
    for i in range(start_index, leng, l):
        t = sequence[i:i+l]
        if seg == t:
            cnt += 1
        elif cnt >= 3:
            return i
        else:
            return 0
    if cnt >= 3: return i + l # sequence 마지막까지 이어지는 low-complexity에 대한 예외
    return -1

while True:
    length = len(data)
    if length < 6: break # low-complexity region의 최소 조건

    end_index = 0
    for i in range(length):
        eds = set()
        for row in range(2, 6):
            ed = get_low_complexity_region(data, i, row, length)
            if ed != 0 and ed != None: 
                end_index = ed
                break
        
        if ed == -1: break
        elif end_index > 0:
            result.append((i, end_index - 1))
            data = data[end_index:]
            print(end_index)
            break

    if end_index == -1: break

print(postprocessing_index_results(result))


# def overlap(st,tst,lowcom): # overlap for another sequence length
#     for i in range(lowcom):
#         if st[i]+6 > tst:
#             return False
#     return True


# startpoint = []
# lowcom = 0

# for i in range (2,6):
#         for j in range(len(data)):
#             ed = j-i*3
#             # print(data[j-i:j], data[j-i-i:j-i], data[j-i-i:j-i], data[ed:j-i-i])
#             if data[j-i:j] == data[j-i-i:j-i] and data[j-i-i:j-i] == data[ed:j-i-i]: #check low-complexity region
#                 if overlap(startpoint,ed,lowcom):
#                     print(data[j-i:j], data[j-i-i:j-i], data[j-i-i:j-i], data[ed:j-i-i])
#                     startpoint.append(ed)
#                     lowcom += 1
#                     if ed != 0:
#                         print(ed + 1)
#                     else:
#                         print(ed)