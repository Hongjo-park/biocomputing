import re, sys, time, os
 
def get_two_dna_sequence(path: str) -> tuple:
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
        elif f_sequence == "" or is_dna_sequence(f_sequence) == False or is_dna_sequence(s_sequence) == False: # the input file has nothting
            print("No DNA sequence.")
            quit()
        return f_sequence, s_sequence
    else:
        print("No input file.")
        quit()

def is_dna_sequence(sequence: str) -> bool:
    '''
    dna sequence and not empty file -> True / else -> False
    
    '''
    return len(sequence) >= 1 and re.fullmatch(r'[ATCG]*', sequence) != None

def main(argv: list) -> None:
    # file read from command line argument
    # check FASTA format
    first_sequence, second_sequence = get_two_dna_sequence(argv[1])
    first_sequence = ' ' + first_sequence
    second_sequence = ' ' + second_sequence

    if len(first_sequence) > len(second_sequence):
        first_sequence, second_sequence = second_sequence, first_sequence
    f_len = len(first_sequence)
    s_len = len(second_sequence)
    
    dp = [[0 for _ in range(s_len)] for _ in range(f_len)]
    result = ""

    start = time.process_time() # set start time
    # Algorithm
    for i in range(1, f_len): # LCS
        for j in range(1, s_len):
            if first_sequence[i] != second_sequence[j]:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
            else:
                dp[i][j] = dp[i - 1][j - 1] + 1
    
    
    i = f_len - 1
    j = s_len - 1
    while True: # back tracking
        cur = dp[i][j]
        if cur == 0: break
        elif cur != dp[i-1][j] and cur != dp[i][j-1]:
            result += first_sequence[i]
            i -= 1
            j -= 1
        elif cur == dp[i-1][j-1]: # 1순위 : 대각선
            i -= 1
            j -= 1
        elif cur == dp[i][j-1]: # 2순위 : 수평선
            j -= 1
        else: # 3순위 : 수직선
            i -= 1
    # end
    end = time.process_time() # set end time
    print(f"time elapsed : {(end - start)*1000}ms")

    # write
    # output_file_name = input("출력 파일 이름을 입력해주세요 : ")
    output_file_name = "output_4.txt"
    output_file = open(output_file_name, 'w')
    output_file.write(result[::-1])
    output_file.close()


if __name__ == '__main__':
    main(sys.argv)