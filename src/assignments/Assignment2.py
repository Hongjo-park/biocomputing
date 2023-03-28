import re, sys

# return the reverse complement sequence of a DNA sequence
# A <-> T, C <-> G
# Ex. ACCTGG -> CCAGGT

def get_file_lines(path: str) -> list:
    '''
    read file.
    remove new line and white-space
    '''
    return [line.strip().replace(' ', '') for line in open(path, 'r').readlines()]

def is_dna_sequence(sequence: str) -> bool:
    '''
    dna sequence -> True / else -> False
    '''
    return re.fullmatch('(A|T|C|G|a|t|c|g)*', sequence) != None

def convert_dna_sequence(sequence: str) -> str:
    '''
    convert all 'A's, 'T's, 'C's, 'G's in the DNA sequence to 'T's, 'A's, 'G's, 'C's
    '''
    return sequence.translate(str.maketrans('ATCG', 'TAGC'))


def output_reverse_complement(sequence: str, file_name='output.txt') -> None:
    output = open(file_name, "w")
    output.write(convert_dna_sequence(sequence[::-1]))
    output.close()

def main(argv):
    '''
    python Assignment2.py "Fill your file name or path"
    '''
    lines = get_file_lines(argv[1])
    sequence = ''.join(lines[1:])

    if is_dna_sequence(sequence):
        output_reverse_complement(sequence, input("출력 파일 경로를 입력해주세요(ex. ./output.txt ): "))
    else:
        print("No DNA sequence.")


if __name__ == '__main__':
    main(sys.argv)