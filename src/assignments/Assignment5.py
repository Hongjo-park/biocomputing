import re, sys, time, os

# C	S T P A G N D E Q H R K M I L V F Y W
def get_blosum62(path: str):
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


def get_two_protein_sequence(path: str) -> tuple:
    '''
    read file.
    Input : file path

    Check empty file, DNA sequence, FASTA format.
    Remove New line and white space.
    Replace capital letters.

    Return : first sequence
    '''
    fasta_cnt = 0
    f_sequence = ""
    s_sequence = ""

    if os.path.isfile(path):
        f = open(path, 'r')
        for line in f.readlines():
            if line.find('>') == 0: # first sequence
                fasta_cnt += 1
                continue
            if fasta_cnt == 1:
                f_sequence += "".join(line.strip().split(' ')).upper() # Remove spaces and replace capital letters
            elif fasta_cnt == 2:
                s_sequence += "".join(line.strip().split(' ')).upper() # Remove spaces and replace capital letters
        f.close()
        if fasta_cnt < 1: # the input file does not follow the FASTA format
            print("No correct format.")
            quit()
        elif fasta_cnt == 1:
            print("Need one more sequence.")
            quit()
        elif is_protein_sequence(f_sequence) == False or is_protein_sequence(s_sequence) == False: # the input file has nothting
            print("No protein sequence.")
            quit()
        return ' ' + f_sequence, ' ' + s_sequence
    else:
        print("No input file.")
        quit()

def is_protein_sequence(sequence: str) -> bool:
    '''
    dna sequence and not empty file -> True / else -> False
    
    '''
    return len(sequence) >= 1 and re.fullmatch(r'[A-Z]*', sequence) != None

def main(argv):
    # gap = -5
    first_sequence, second_sequence = get_two_protein_sequence(argv[1])
    fs_dict, ss_dict = dict(), dict()
    for i, row in enumerate(first_sequence):
        fs_dict[i] = row
    for i, row in enumerate(second_sequence):
        ss_dict[i] = row

    
    f_len = len(first_sequence)
    s_len = len(second_sequence)

    dp = [[0 for _ in range(s_len)] for _ in range(f_len)]

    protein_dict, blosum_dict = get_blosum62("BLOSUM62.txt") # blosum62 파일명 입력
    out_1, out_2 = "", ""
    start = time.process_time() # set start time
    # Algorithm
    for i in range(1, f_len): # LCS
        for j in range(1, s_len):
            fs_letter = fs_dict[i]
            ss_letter = ss_dict[j]

            diagonal = dp[i - 1][j - 1] + blosum_dict[fs_letter][protein_dict[ss_letter]]

            if fs_letter != ss_letter:
                dp[i][j] = max(0, dp[i][j - 1] - 5, dp[i - 1][j] - 5, diagonal)
            else:
                dp[i][j] = diagonal
    
    i = f_len - 1
    j = s_len - 1
    while True: # back tracking
        cur = dp[i][j]
        fs_letter = fs_dict[i]
        ss_letter = ss_dict[j]
        if cur == 0: break
        elif fs_letter == ss_letter or cur == dp[i - 1][j - 1] +blosum_dict[fs_letter][protein_dict[ss_letter]]:
            out_1 += fs_letter
            out_2 += ss_letter
            i -= 1
            j -= 1
        elif dp[i][j - 1] >= dp[i - 1][j]: 
            out_1 += '-'
            out_2 += ss_letter
            j -= 1
        else:
            out_1 += fs_letter
            out_2 += '-'
            i -= 1
    # end
    print(f"time elapsed : {(time.process_time() - start)*1000}ms")

    output_file_name = "output_5.txt"
    output_file = open(output_file_name, 'w')
    out_1, out_2 = out_1[::-1], out_2[::-1]
    for i in range(int(len(out_1)/60+1)):
        output_file.write(out_1[i*60:(i+1)*60]+'\n')
        output_file.write(out_2[i*60:(i+1)*60]+'\n\n')
    output_file.write(f'Similarity Score : {max(max(row) for row in dp)}') # Score의 최대값

if __name__ == '__main__':  
    main(sys.argv)