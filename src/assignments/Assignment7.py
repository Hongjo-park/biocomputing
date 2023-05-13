import re, sys, time, os
import datetime

# Except : n, m is length of two Text File 
# 더 긴 file -> Text, 짧은 file -> patterns
# 첫 줄에 newline이 나오면 no string found

# 처음부터 읽어서 newline이 나올 때까지 읽는다. 이것은 Text or pattern이 된다.
# newline 이후는 무시하고 수행한다.

# if newline이 없다면 end까지 읽고 수행한다.

def get_text_and_pattern(argv: list):
    if len(argv) != 2: 
        print("No input file")
        quit()
    def get_str_from_file(path: str) -> str:
        if os.path.isfile(path):
            lines = open(path, 'r').read().split('\n')[0].upper()

            if len(lines) < 1:
                print("No string found")
                quit()
            return lines
        else:
            print("No input file")
            quit()
    
    def convert_text_pattern(str_list: list) -> tuple:
        '''
        first : text, second : pattern
        '''
        if len(str_list) < 2: quit()
        s1, s2 = str_list[0], str_list[1]
        s1_len, s2_len = len(s1), len(s2)
        return (s1, s2, s1_len, s2_len) if s1_len > s2_len else (s2, s1, s2_len, s1_len)
    
    return convert_text_pattern([get_str_from_file(argm) for argm in argv])

def PrefixFunction(pattern, p_l):
    m = [0]*p_l
    k = 0
    for i in range(1, p_l):
        while k > 0 and pattern[k] != pattern[i]:
            k = m[k-1]
        if pattern[k] == pattern[i]:
            k += 1
            m[i] = k
    return m


def KMP_Matching(text, pattern, t_l, p_l):
    result = list() 
    q = 0
    pref = PrefixFunction(pattern, p_l)

    for i in range(t_l):
        while q > 0 and pattern[q] != text[i]:
            q = pref[q - 1]
        if pattern[q] == text[i]:
            if q == p_l - 1:
                result.append(i - p_l + 1)
                q = pref[q]
            else:
                q += 1
    return result

def main(argv: list) -> None:
    text, pattern, t_l, p_l = get_text_and_pattern(argv[1:])
    result = list()

    start = time.process_time() # set start time
    # ================================================================================================================================================================================
    # Algorithm start
    # ================================================================================================================================================================================
    result = KMP_Matching(text, pattern, t_l, p_l)
    # ================================================================================================================================================================================    
    # Algorithm end
    # ================================================================================================================================================================================
    print(f"time elapsed : {(time.process_time() - start)*1000000} microseconds")

    with open("output_7_박홍조.txt", 'w') as f:
        if len(result) == 0: print("No match found.")
        else: f.write(' '.join(map(str, result)))

if __name__ == '__main__':
    main(sys.argv)