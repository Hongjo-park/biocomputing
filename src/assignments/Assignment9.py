import re, sys, time, os

# input multiple DNA sequences
def receive_multiple_dna_sequences(argv: list) -> list:
    if len(argv) <= 1:
        print("No input file")
        quit()
    
    path = argv[1]
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
        elif len(result) < 1:
            print("No DNA seqeunce.")
            quit()

        for i, row in enumerate(result):
            if is_dna_sequence(row) == False:
                print("No DNA sequence.")
                quit()

        if len(result) <= 1:
            print("Need more sequences.")
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

# Non Trie Algorithm
# def find_longest_patterns(dna_sequences):
#     max_length = max(len(seq) for seq in dna_sequences)
#     longest_patterns = []

#     for pattern_length in range(2, max_length + 1):
#         patterns = set()

#         # Generate all possible patterns of the current length
#         for seq in dna_sequences:
#             for i in range(len(seq) - pattern_length + 1):
#                 pattern = seq[i:i+pattern_length]
#                 patterns.add(pattern)

#         # Check if all sequences contain the current patterns
#         for pattern in patterns:
#             count = 0
#             for seq in dna_sequences:
#                 if pattern not in seq:
#                     break
#                 count += 1
#             if count == len(dna_sequences):
#                 longest_patterns.append(pattern)

#     return longest_patterns

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.count = 0

def insert_pattern(root, pattern):
    node = root
    for char in pattern:
        if char not in node.children:
            node.children[char] = TrieNode()
        node = node.children[char]
        node.count += 1
    node.is_end_of_word = True

def find_longest_patterns(dna_sequences):
    root = TrieNode()
    longest_patterns = []
    pattern_length = 2

    while True:
        # Insert each DNA sequence into the trie
        for seq in dna_sequences:
            for i in range(len(seq) - pattern_length + 1):
                insert_pattern(root, seq[i:i+pattern_length])

        patterns = set()

        # Generate all possible patterns of the current length
        stack = [(node, char) for char, node in root.children.items()]
        while stack:
            node, pattern = stack.pop()
            if len(pattern) == pattern_length:
                patterns.add(pattern)
            else:
                stack.extend([(child, pattern + char) for char, child in node.children.items()])

        valid_patterns = []
        for pattern in patterns:
            count = 0
            for sequence in dna_sequences:
                if pattern not in sequence:
                    break
                count += 1
            if count == len(dna_sequences):
                valid_patterns.append(pattern) # 모든 문자열에 Pattern 존재

        if not valid_patterns:
            break

        longest_patterns.extend(valid_patterns)
        pattern_length += 1
        max_length = len(max(longest_patterns, key=len))
        longest_patterns = [pattern for pattern in longest_patterns if len(pattern) == max_length]

    return longest_patterns


def main(argv: list) -> None:
    dna_sequences = receive_multiple_dna_sequences(argv)

    start = time.process_time() # set start time
    # ================================================================================================================================================================================
    # Algorithm start
    # ================================================================================================================================================================================
    result = find_longest_patterns(dna_sequences)
    # ================================================================================================================================================================================    
    # Algorithm end
    # ================================================================================================================================================================================
    print(f"time elapsed : {(time.process_time() - start)*1000000} microseconds")

    # Write ( 알파벳 순으로 정렬되어 작성됨 )
    if len(result) < 1:
        print("No pattern fond.")
        quit()
    result.sort()
    with open("output_9_박홍조.txt", 'w') as f:
        for row in result:
            f.write(row)
            f.write('\n')

if __name__ == '__main__':
    main(sys.argv)