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

def main(argv: list) -> None:
    results = list()
    # file read from command line argument
    # check FASTA format
    first_sequence, second_sequence = get_two_dna_sequence(argv[1])
    
    start = time.process_time() # set start time

    # Algorithm

    end = time.process_time() # set end time
    print(f"time elapsed : {(end - start)*1000}ms")

    # write


if __name__ == '__main__':
    main(sys.argv)