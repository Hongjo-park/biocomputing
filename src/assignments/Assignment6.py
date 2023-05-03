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


def get_protein_sequences(path: str) -> tuple:
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
    # init
    protein_sequences = get_protein_sequences(argv[1])
    protein_dict, blosum_dict = get_blosum62("BLOSUM62.txt") 


    # Algorithm
    start = time.process_time() # set start time




    # end
    print(f"time elapsed : {(time.process_time() - start)*1000}ms")
    

    # write output











if __name__ == '__main__':
    main(sys.argv)