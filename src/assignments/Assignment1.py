import re

# convert all 'T's in the DNA sequence to 'U's
# s : \n

# If the input file does not have a DNA sequence, then print "No DNA sequence".

# input file : case-insensitive ( upper or lower ) Ex. Attcg
# t, T -> u, U

if __name__ == '__main__':
    # file open 
    # Input file path Ex. src/assignments/input.txt
    f = open(input("파일 경로를 입력해주세요 (ex. ./input.txt ): "), 'r')
    # read lines
    lines = [line.strip() for line in f.readlines()]
    # remove first line(comment)
    dna_sequence = ''.join(lines[1:])
    
    # check DNA sequence
    if re.fullmatch('(A|T|C|G|a|t|c|g)*', dna_sequence) == None:
        print("No DNA sequence.")
    else:
        # replace 'T' or 't' to 'U' and file output ( any file name ) Ex. output.txt
        output = open("output.txt", "w")
        output.write(re.sub('T|t', 'U', dna_sequence))
        output.close()