import re, sys, time, os
from itertools import zip_longest

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
    
    psa_arr = [[] for _ in range(len_sequences)] # PSA 쌍들의 List
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
            if i < j:
                f_l, s_l = len(fs), len(ss)
                dp[i].append(get_dp(f_l, s_l, -5))
            else:
                dp[i].append([])


    # score는 dp table의 가장 마지막 value
    # Algorithm
    start = time.process_time() # set start time
    
    # dp table 채우기, PSA 구하기
    for i, i_row in enumerate(dp):
        for j, j_row in enumerate(i_row):
            if i < j:
                f_len = len(protein_sequences[i])
                s_len = len(protein_sequences[j])
                for k in range(1, f_len):
                    for w in range(1, s_len):
                        j_row[k][w] = max(j_row[k][w - 1] - 5, j_row[k - 1][w] - 5, j_row[k - 1][w - 1] + blosum_dict[sequence_dicts[i][k]][protein_dict[sequence_dicts[j][w]]])

                scores[i] += j_row[k][w]
                scores[j] += j_row[k][w]


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
                    elif j_row[y][x] == j_row[y - 1][x - 1] + blosum_dict[fs_letter][protein_dict[ss_letter]]:
                        out_1 += fs_letter
                        out_2 += ss_letter
                        y -= 1
                        x -= 1
                    elif j_row[y][x - 1] >= j_row[y - 1][x]:
                        out_1 += '-'
                        out_2 += ss_letter
                        x -= 1
                    elif j_row[y][x - 1] < j_row[y - 1][x]:
                        out_1 += fs_letter
                        out_2 += '-'
                        y -= 1

                out_1 = out_1[::-1]
                out_2 = out_2[::-1]
                psa_arr[i].append([out_1, out_2])
                psa_arr[j].append([out_2, out_1])
            elif i == j:
                psa_arr[i].append([])

    # get psa from max score
    max_score_sequence_index = scores.index(max(scores))
    psa_arr = psa_arr[max_score_sequence_index]
    del psa_arr[max_score_sequence_index]


    # PSA to MSA
    msa_arr[0] = psa_arr[0][0]
    msa_arr[1] = psa_arr[0][1]
    del psa_arr[0]

    for i, row in enumerate(psa_arr):
        x, p = row[0], row[1]
        m_i, p_i = 0, 0
        while True:
            p_l = len(x)
            m_l = len(msa_arr[0])
            if m_i >= m_l or p_i >= p_l:
                if m_i >= m_l and p_i >= p_l: break
                elif m_i >= m_l:
                    msa_arr[i+2] += p[p_i]
                    msa_gaps = ''
                    for k in range(p_l - m_l): msa_gaps += '-'
                    for k in range(i+2): msa_arr[k] += msa_gaps
                    break
                elif p_i >= len(psa_arr[i]):
                    for k in range(m_l - p_i): msa_arr[i+2] += '-'
                    break
            elif msa_arr[0][m_i] == x[p_i]:
                msa_arr[i+2] += x[p_i]
                m_i += 1
                p_i += 1
            elif msa_arr[0][m_i] == '-':
                msa_arr[i+2] += '-'
                m_i += 1
            else:
                msa_arr[i + 2] += x[p_i]
                for k in range(i):
                    msa_arr[k] = msa_arr[k][:m_i] + '-' + msa_arr[k][m_i:]
                p_i += 1
            

            # if m_i >= m_l and p_i < p_l:
            #     for k in range(0, p_l - p_i):
            #         msa_arr[k] += '-'
            #         msa_arr[i+2] += p[p_i + k]
            #         p_i += 1
            # elif m_i < m_l and p_i >= x_l:
            #     for k in range(0, m_l - m_i):
            #         msa_arr[i+2] += '-'
            #         m_i +=1

            # if m_i >= m_l and p_i >= x_l: break
            # elif x[p_i] == msa_arr[0][m_i]: # both no gap or gap
            #     msa_arr[i+2] += p[p_i]
            #     m_i += 1
            #     p_i += 1
            # elif x[p_i] == '-': # PSA gap and MSA no gap
            #     # insert gap to MSA
            #     for j in range(0, i+2):
            #         msa_arr[j] = msa_arr[j][:m_i] + '-' + msa_arr[j][m_i:]
            #     msa_arr[i+2] += p[p_i]
            #     p_i += 1
            # elif msa_arr[0][m_i] == '-': # PSA no gap and MSA gap
            #     msa_arr[i+2] += '-'
            #     m_i += 1
            # print(msa_arr, p_i, m_i)

    # end
    print(f"time elapsed : {(time.process_time() - start)*1000000}ms")

    # write output
    with open('output_6_박홍조.txt', 'w') as f:
        len_m = len(msa_arr[0])
        compare_list = list()
        if len_m < 60: 
            for row in msa_arr:
                f.write(row + '\n')
                compare_list.append(list(row))
            f.write(''.join("*" if len(set(row)) == 1 else " " for row in list(map(list, zip(*compare_list)))))
        for i in range(0, len_m, 60):
            compare_list = list()
            for row in msa_arr:
                s = row[i:i+60]
                compare_list.append(list(s))
                if len(s) < 60: continue
                f.write(s + '\n')
            # write star
            f.write(''.join("*" if len(set(row)) == 1 else " " for row in list(map(list, zip(*compare_list)))))
            f.write('\n\n')
        if i < len_m: # 남는 글자
            compare_list = list()
            for row in msa_arr:
                s = row[i:-1]
                compare_list.append(list(s))
                f.write(s + '\n')
            f.write(''.join("*" if len(set(row)) == 1 else " " for row in list(map(list, zip(*compare_list)))))
            f.write('\n\n')


if __name__ == '__main__':
    main(sys.argv)