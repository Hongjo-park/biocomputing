import re, sys, time, os

# input multiple DNA sequences

def receive_multiple_dna_sequences(path: str) -> list:
    if os.path.isfile(path):
        result = list()
        dna_sequence = ""
        is_fasta = False
        f = open(path, 'r')
        lines = f.readlines()
        for line in lines:
            if line.find('>') == 0:
                is_fasta = True
                if len(dna_sequence) > 0:
                    result.append(dna_sequence)
                    dna_sequence = ""
                continue
            if is_fasta:
                dna_sequence += "".join(line.strip().split(' ')).upper()
        f.close()
        if len(dna_sequence) > 0:
            result.append("".join(dna_sequence.strip().split(' ')).upper())

        if is_fasta == False:
            print("No correct format.")
            quit()
        elif len(result) <= 1:
            print("Need more sequences.")
            quit()
        
        for i, row in enumerate(result):
            if is_dna_sequence(row) == False:
                print("No DNA sequence.")
                quit()

        return result
    else:
        print("No input file.")
        quit()

def is_dna_sequence(sequence: str) -> bool:
    '''
    dna sequence and not empty file -> True / else -> False
    
    '''
    return len(sequence) >= 1 and re.fullmatch(r'[ATCG]*', sequence) != None




def main(argv: list) -> None:
    dna_sequences = receive_multiple_dna_sequences(argv[1])

    start = time.process_time() # set start time
    
    # ================================================================================================================================================================================
    # Algorithm start
    # ================================================================================================================================================================================
    common_patterns = set()
    shortest_sequence = min(dna_sequences, key=len)
    length_shortest_sequence = len(shortest_sequence)


    for pattern_length in range(2, length_shortest_sequence + 1):
        patterns = set()
        for i in range(length_shortest_sequence - pattern_length + 1):
            pattern = shortest_sequence[i:i + pattern_length]
            patterns.add(pattern)

        for sequence in dna_sequences[1:]:
            updated_patterns = set()
            for pattern in patterns:
                if all(pattern in seq for seq in dna_sequences[:dna_sequences.index(sequence)]):
                    if pattern in sequence:
                        updated_patterns.add(pattern)
            patterns = updated_patterns

        common_patterns.update(patterns)

    longest_patterns = [pattern for pattern in common_patterns if all(pattern in sequence for sequence in dna_sequences)]

    
    # ================================================================================================================================================================================    
    # Algorithm end
    # ================================================================================================================================================================================
    print(f"time elapsed : {(time.process_time() - start)*1000000} microseconds")



if __name__ == '__main__':
    main(sys.argv)