import sys, time, os

# patterns는 multiple lines로 나타난다.
# 이는 newline으로 구분된다.
# 모든 파일은 end까지 읽는다.

# 이 때 newline으로 구분된 text가 여러개라면 patterns로 구분된다.

# output
# pattern : positions

def get_text_and_pattern(argv: list) -> tuple:
    if len(argv) != 2: 
        print("No input file")
        quit()
    def get_str_from_file(path: str) -> str:
        if os.path.isfile(path):
            with open(path, 'r') as f:
                lines = f.readlines()
                if len(lines) < 1:
                    print("No string found")
                    quit()
                return [line.strip().upper() for line in lines]
        else:
            print("No input file")
            quit()
    
    f_sequence, s_sequence = [get_str_from_file(argument) for argument in argv]
    f_l, s_l = len(f_sequence), len(s_sequence)

    if f_l > 1 and s_l > 1:
        print("No text found.")
        quit()
    elif f_l == 1 and s_l == 1:
        print("No multiple patterns found.")
        quit()

    # return patterns, text ( tuple )
    return (f_sequence, s_sequence[0]) if f_l > s_l else (s_sequence, f_sequence[0])


class TrieNode:
    def __init__(self):
        self.children = {}
        self.fail = None
        self.word = None
class AhoCorasick:
    def __init__(self):
        self.root = TrieNode()
        
    def add_word(self, word): # add pattern
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.word = word
        
    def build_failure(self): # BFS로 failure setting
        queue = []
        for node in self.root.children.values():
            node.fail = self.root
            queue.append(node)
            
        while queue:
            curr = queue.pop(0)
            for char, child in curr.children.items():
                fail_node = curr.fail
                while fail_node is not None and char not in fail_node.children:
                    fail_node = fail_node.fail
                child.fail = fail_node.children[char] if fail_node else self.root
                queue.append(child)
                
    def find_matches(self, text): # return : position, pattern
        matches = []
        curr = self.root
        for i, char in enumerate(text):
            while curr is not None and char not in curr.children:
                curr = curr.fail
            if curr is None:
                curr = self.root
                continue
            curr = curr.children[char]
            if curr.word:
                matches.append((i - len(curr.word) + 1, curr.word))
        return matches


def main(argv: list) -> None:
    # get text, pattern
    patterns, text = get_text_and_pattern(argv[1:])
    ac = AhoCorasick()

    start = time.process_time() # set start time
    # ================================================================================================================================================================================
    # Algorithm start
    # ================================================================================================================================================================================
    for pattern in patterns:
        ac.add_word(pattern)
    ac.build_failure()
    matches = ac.find_matches(text)
    # ================================================================================================================================================================================    
    # Algorithm end
    # ================================================================================================================================================================================
    print(f"time elapsed : {(time.process_time() - start)*1000000} microseconds")


    # write
    if len(matches) < 1:
        print("No match found.")
        quit()

    def get_write_dict(matches) -> dict:
        match_dict = dict()
        for position, word in matches:
            if word in match_dict:
                match_dict[word].append(position)
            else:
                match_dict[word] = [position]
        return match_dict
    
    with open("output_8_박홍조.txt", 'w') as f:
        for pattern, positions in get_write_dict(matches).items():
            f.write(f"{pattern} : {' '.join(map(str, positions))}")
            f.write('\n')


if __name__ == '__main__':
    main(sys.argv)