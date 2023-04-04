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


# low-complexity region이 가장 긴 것을 우선으로 찾는다.
# ex : AAAAAAAAATCG -> AAAAAAAAA | TCG
def main(argv: list) -> None:
    # file read from command line argument
    # check FASTA format
    dna_sequence = get_dna_sequence(argv[1])
    
    start = time.process_time() # set start time

    # find low-complexity regions on RE
    p = re.compile(r'(\w{2,5})\1{2,}')
    fi = list(p.finditer(dna_sequence))
    end = time.process_time() # set end time
    print(f"time elapsed : {(end - start)*1000}ms")
    
    if len(fi) > 0: # If the input sequence does not include any low-complexity region
        # write index
        output_file_name = input("출력 파일 이름을 입력해주세요 : ")
        output_file = open(output_file_name, 'w')
        for row in fi:
            output_file.write(str(row.start()) + '\n')
        output_file.close()
    else:
        print("No low-complexity region found")

    
if __name__ == '__main__':
    main(sys.argv)