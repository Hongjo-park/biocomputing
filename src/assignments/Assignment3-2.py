import re, sys, time, os
 
def get_dna_sequence(path: str) -> str:
    '''
    read file.
    Input : file path

    Check empty file, DNA sequence, FASTA format.
    Remove New line and white space.
    Replace capital letters.

    Return : first sequence
    '''
    is_fasta = False
    sequence = ""
    if os.path.isfile(path):
        f = open(path, 'r')
        for line in f.readlines():
            if line.find('>') == 0: # first sequence
                if is_fasta: 
                    break
                else:
                    is_fasta = True
                    continue
            else:
                sequence += "".join(line.strip().split(' ')).upper()
        f.close()

        if is_fasta == False:
            print("No correct format.")
            quit()
        if sequence == "" or is_dna_sequence(sequence) == False:
            print("No DNA sequence")
            quit()
        return sequence
    else:
        print("No input file.")
        quit()

def is_dna_sequence(sequence: str) -> bool:
    '''
    dna sequence and not empty file -> True / else -> False
    
    '''
    return len(sequence) >= 1 and re.fullmatch(r'[ATCG]*', sequence) != None

def postprocessing_index_results(arr: list) -> list:
    '''
    전체 Sequence 길이에 맞는 index로 변환
    '''
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

# low-complexity region이 가장 긴 것을 우선으로 찾는다.
# ex : AAAAAAAAATCG -> AAAAAAAAA | TCG
def main(argv: list) -> None:
    results = list()
    # file read from command line argument
    # check FASTA format
    dna_sequence = get_dna_sequence(argv[1])

    start = time.process_time() # set start time

    # find low-complexity regions on RE
    while True:
        length = len(dna_sequence)
        if length < 6: break # low-complexity region의 최소 조건

        end_index = 0
        for i in range(length):
            eds = set()
            for row in range(2, 6):
                ed = get_low_complexity_region(dna_sequence, i, row, length)
                if ed != 0 and ed != None: 
                    end_index = ed
                    break
            
            if ed == -1: break
            elif end_index > 0:
                results.append((i, end_index - 1))
                dna_sequence = dna_sequence[end_index:]
                break

        if end_index == -1: break
    results = postprocessing_index_results(results)

    end = time.process_time() # set end time
    print(f"time elapsed : {(end - start)*1000}ms")


    if len(results) > 0: # If the input sequence does not include any low-complexity region
        # write index
        # output_file_name = input("출력 파일 이름을 입력해주세요 : ")
        output_file_name = "output3-2.txt"
        output_file = open(output_file_name, 'w')
        for row in results:
            output_file.write(str(row) + '\n')
        output_file.close()
    else:
        print("No low-complexity region found")


if __name__ == '__main__':
    main(sys.argv)
