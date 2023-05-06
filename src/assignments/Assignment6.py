import re, sys, time, os

# C	S T P A G N D E Q H R K M I L V F Y W
def get_blosum62(path: str) -> tuple[dict]:
    '''
    read blosum62

    '''
    protien_dict, blosum_dict = dict(), dict()
    
    if os.path.isfile(path):
        f = open(path, 'r')
        lines = f.readlines()
        first_line = lines[0].split()[:-1]
        for i, row in enumerate(first_line):
            protien_dict[row] = i
        
        for i, line in enumerate(lines[1:-1]):
            blosum_dict[first_line[i]] = tuple(map(int, line.split()[1:-1]))

        # print(blosum_dict['C'][protien_dict['T']])
        return protien_dict, blosum_dict

def get_protein_sequences(path: str) -> tuple[str]:
    '''
    read file.
    Input : file path

    Check empty file, protein sequence, FASTA format.
    Remove New line and white space.
    Replace capital letters.

    Return : sequences
    '''
    is_fasta = False
    protein_sequence = ""
    sequences = list()

    if os.path.isfile(path):
        f = open(path, 'r')
        for line in f.readlines():
            if line.find('>') == 0: # first sequence
                is_fasta = True
                if len(protein_sequence) > 0:
                    sequences.append(protein_sequence)
                    protein_sequence = ""
                continue
            if is_fasta:
                protein_sequence += "".join(line.strip().split(' ')).upper() # Remove spaces and replace capital letters
        f.close()

        if is_fasta == False: # the input file does not follow the FASTA format
            print("No correct format.")
            quit()
        elif len(sequences) <= 1:
            print("Need one more sequence.")
            quit()

        if len(protein_sequence) > 0:
            sequences.append("".join(protein_sequence.strip().split(' ')).upper())
        for i, row in enumerate(sequences):
            if is_protein_sequence(row) == False: # the input file has nothting
                print("No protein sequence.")
                quit()
            sequences[i] = ' ' + row

        return sequences
    else:
        print("No input file.")
        quit()

def is_protein_sequence(sequence: str) -> bool:
    '''
    dna sequence and not empty file -> True / else -> False
    
    '''
    return len(sequence) >= 1 and re.fullmatch(r'[A-Z]*', sequence) != None

def get_sequence_dict(seqeunce: str) -> dict:
    result = dict()
    for i, row in enumerate(seqeunce):
        result[i] = row
    return result


def get_dp(n, m, gap) -> list:
    '''
    init dp table

    linear gap
    '''
    result = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(1, m):
        result[0][i] = result[0][i-1] + gap
    for i in range(1, n):
        result[i][0] = result[i-1][0] + gap
    return result 


def main(argv):
    # init
    protein_sequences = get_protein_sequences(argv[1])
    protein_dict, blosum_dict = get_blosum62("BLOSUM62.txt")
    sequence_dicts = [get_sequence_dict(row) for row in protein_sequences]
    len_sequences = len(protein_sequences)

    scores = [0 for _ in range(len_sequences)] # n개의 sequence에 대한 score board
    
    psa_arr = list() # PSA 쌍들의 List
    msa_arr = ["" for _ in range(len_sequences)] # n개의 MSA

    # 0, 1, 2, 3, ... , n
    # n X n 행렬
    # EX. 4개 seqeunce : (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3) => 6개

    # n개의 seqeunce에 대해 각각의 score를 구하기 위한 dp table 세팅
    # 하나의 요소는 [score, dp]를 가짐
    # init dp table
    dp = [[] for _ in range(len_sequences)]
    for i, fs in enumerate(protein_sequences):
        for j, ss in enumerate(protein_sequences):
            if i == j:
                dp[i].append([])
                continue

            f_l, s_l = len(fs), len(ss)
            dp[i].append(get_dp(f_l, s_l, -5))

    # ================================================================================================================================================================================
    # Algorithm start
    # ================================================================================================================================================================================
    start = time.process_time() # set start time
    
    # dp table 채우기, PSA 구하기
    for i, i_row in enumerate(dp):
        psa_set = list()
        for j, j_row in enumerate(i_row):
            if i == j: 
                psa_set.append(protein_sequences[i][1:])
                continue

            f_len = len(protein_sequences[i])
            s_len = len(protein_sequences[j])
            for k in range(1, f_len):
                for w in range(1, s_len):
                    j_row[k][w] = max(j_row[k][w - 1] - 5, j_row[k - 1][w] - 5, j_row[k - 1][w - 1] + blosum_dict[sequence_dicts[i][k]][protein_dict[sequence_dicts[j][w]]])
            scores[i] += j_row[k][w]

            # back tracking
            first_sequence = sequence_dicts[i]
            second_sequence = sequence_dicts[j]
            out_1, out_2 = "", ""
            y, x = f_len -1, s_len - 1
            while True:
                fs_letter = first_sequence[y]
                ss_letter = second_sequence[x]

                if y == 0 and x == 0: break
                elif y == 0: # 
                    out_1 += '-'
                    out_2 += ss_letter
                    x -= 1
                elif x == 0:
                    out_1 += fs_letter
                    out_2 += '-'
                    y -= 1
                elif j_row[y][x] == j_row[y - 1][x - 1] + blosum_dict[fs_letter][protein_dict[ss_letter]] or fs_letter == ss_letter:
                    out_1 += fs_letter
                    out_2 += ss_letter
                    y -= 1
                    x -= 1
                elif j_row[y][x - 1] >= j_row[y - 1][x]:
                    out_1 += '-'
                    out_2 += ss_letter
                    x -= 1
                else:
                    out_1 += fs_letter
                    out_2 += '-'
                    y -= 1

            psa_set.append(out_1[::-1])
        psa_arr.append(psa_set)

    
    # get psa max score
    ct_seq_index = scores.index(max(scores))

    # PSA to MSA
    s_i = 0 # start position

    # init MSA
    if ct_seq_index == 0:
        msa_arr[0] = psa_arr[0][1]
        msa_arr[1] = psa_arr[1][0]
        s_i = 2
    else:
        msa_arr[ct_seq_index] = psa_arr[ct_seq_index][0]
        msa_arr[0] = psa_arr[0][ct_seq_index]
        s_i = 1
    
    p_l = len(psa_arr)
    for i in range(s_i, p_l):
        if i == ct_seq_index: continue

        msa_arr[i] = psa_arr[i][ct_seq_index]
        insert_s = ""
        j, w = 0, 0 # gap이 있을 때 IndexError를 막기 위한 index 변수

        while True:
            psa_index = j - w
            ct_len = len(msa_arr[ct_seq_index])
            psa_len = len(psa_arr[i][ct_seq_index])
            if j >= ct_len or psa_index >= psa_len: # msa와 psa 중 하나가 마지막까지 검사를 완료한 경우
                if j >= ct_len and psa_index >= psa_len: break # 둘 다 검사 완료 => 종료
                elif j >= ct_len: # msa만 검사 완료 => 남은 psa letter 수만큼 msa에 gap 추가
                    insert_s += msa_arr[i][psa_index]
                    msa_gaps = ''
                    for k in range(psa_len - ct_len): msa_gaps += '-'
                    for k in range(i): msa_arr[k] += msa_gaps
                    break
                elif psa_index >= len(psa_arr[i]): # psa만 검사 완료 => 남은 msa 수만큼 psa에 gap 추가
                    for k in range(ct_len - j): insert_s += '-'
                    break
            elif msa_arr[ct_seq_index][j] == psa_arr[ct_seq_index][i][j-w]: # 둘 다 동일한 letter일 경우 그대로 삽입
                insert_s += msa_arr[i][j-w]
            elif msa_arr[ct_seq_index][j] == '-': # msa만 gap => psa에 gap 추가
                insert_s += '-'
                w += 1
            else: # psa만 gap => psa는 그대로 삽입, msa는 gap 모두 추가
                insert_s += msa_arr[i][j-w]
                for k in range(i):
                    msa_arr[k] = msa_arr[k][:j] + '-' + msa_arr[k][j:]
            j += 1
        msa_arr[i] = insert_s

    # ================================================================================================================================================================================    
    # Algorithm end
    # ================================================================================================================================================================================
    print(f"time elapsed : {(time.process_time() - start)*1000000}ms")


    # write output
    with open('output_6_박홍조.txt', 'w') as f:
        msa_arr[0], msa_arr[ct_seq_index] = msa_arr[ct_seq_index], msa_arr[0]
        len_m = len(msa_arr[ct_seq_index])
        compare_list = list()
        if len_m < 60:
            for row in msa_arr:
                f.write(row + '\n')
                compare_list.append(list(row))
            f.write(''.join("*" if len(set(row)) == 1 else " " for row in list(map(list, zip(*compare_list)))))
            f.write('\n\n')
        else:
            for i in range(0, len_m, 60):
                for row in msa_arr:
                    s = row[i:i+60]
                    compare_list.append(list(s))
                    if len(s) < 60: continue
                    f.write(s + '\n')
                # write star
                f.write(''.join("*" if len(set(row)) == 1 else " " for row in list(map(list, zip(*compare_list)))))
                f.write('\n\n')
            if i < len_m:
                for row in msa_arr:
                    s = row[i:-1]
                    compare_list.append(list(s))
                    f.write(s + '\n')
                f.write(''.join("*" if len(set(row)) == 1 else " " for row in list(map(list, zip(*compare_list)))))
                f.write('\n\n')


if __name__ == '__main__':
    main(sys.argv)