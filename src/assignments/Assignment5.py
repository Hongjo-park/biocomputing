import re, sys, time, os


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
    first_sequence, second_sequence = get_two_protein_sequence(argv[1])
    f_len = len(first_sequence)
    s_len = len(second_sequence)

    dp = [[0 for _ in range(s_len)] for _ in range(f_len)]

    start = time.process_time() # set start time
    
    # Algorithm

    # end
    end = time.process_time() # set end time
    print(f"time elapsed : {(end - start)*1000}ms")


if __name__ == '__main__':
    main(sys.argv)