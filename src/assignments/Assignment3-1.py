import re, sys, time

def read_file(path: str) -> list:
    '''
    read file.
    remove new line and white-space
    '''
    return [line.strip().replace(' ', '') for line in open(path, 'r').readlines()]

def is_dna_sequence(sequence: str) -> bool:
    '''
    dna sequence and not empty file -> True / else -> False
    
    '''
    return re.fullmatch('(A|T|C|G|a|t|c|g)*', sequence) != None and len(sequence) >= 1

def is_fasta(lines: list) -> bool:
    pass

def main(argv: list) -> None:
    # file read from command line argument\
    # check FASTA format
    lines = read_file(argv[1])
    
    # check file and dna sequence



if __name__ == '__main__':
    main(sys.argv)