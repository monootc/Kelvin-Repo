# COMP 157 Project 3: Compression
# Author: Kelvin Hu
# Date: 12/4/16

import queue
from math import log2, ceil
import pickle
import io


# class to hold the Node in a tree structure
class Node(object):
    def __init__(self, left=None, right=None, letter=None, freq=0):
        self.left = left
        self.right = right
        self.letter = letter
        self.freq = freq
    def __lt__(self, other):
        return(self.freq < other.freq)
    def setChildren(self):
        return([self.left, self.right])


# open file and strip all newlines
# input: filename
# output: a string with all newlines stripped
def openFile(filename):
    try:
        with io.open(filename, 'r', encoding='utf-8') as f:
            myStr = f.read().replace('\n', '')  # strip newline
        f.close()
        return myStr
    except OSError:
        print("cannot open file")
        exit()



# build a frequency table based on number of occurance of each char
# input: string
# output: a table, key = all char, value = # of occurance
def buildFreqTable(myStr):
    freqTable = {}
    for char in myStr:
        if char in freqTable:   # increment value if key already in the table
            freqTable[char]=freqTable.get(char)+1
        else:
            freqTable[char]=1   # set value to 1 if it's a new key
    total = sum(freqTable.values())
    for key, value in freqTable.items():
        freq = value / total
        freqTable[key] = freq
    return freqTable


# create a huffman tree
# input: freqTable
# output: the root node of huffman tree
def create_tree(freq):
    p_queue = queue.PriorityQueue()
    #print(freq)
    for value in freq:
        new_node = Node(letter=value, freq=freq.get(value))
        p_queue.put(new_node)               # set each node as leaf and store in P queue

    while p_queue.qsize() > 1:
        l, r = p_queue.get(), p_queue.get() # pop 2 smallest values
        node = Node(left=l, right=r, letter=None, freq=l.freq + r.freq) # create an internal node and set its freq to
        p_queue.put(node)                                               # the sum of 2 smallest node
    return p_queue.get()    # return the root node


# tree traversal preorder
# input: node object, prefix, secret_code
# output: secret_code_table
def treeTraverse(node, prefix="", secret_code={}):
    if isinstance(node.left, Node):
        treeTraverse(node.left,prefix+"0", secret_code)     # append 0 when going left
    else:
        secret_code[node.letter]=prefix
    if isinstance(node.right ,Node):
        treeTraverse(node.right,prefix+"1", secret_code)    # append 1 when going right
    else:
        secret_code[node.letter]=prefix
    return(secret_code)


# cancatenate the sequence
# input: string, code
# output: string sequence
def formSequence(myStr, code):
    sequence=""
    for char in myStr:
        sequence += code.get(char)
    return sequence


# decompress the code back to original string
# input: string, node (root)
# output: original string
def decompress(fileString, node):
    root = node
    decode=[]
    l = len(fileString)
    index = 0
    while index < l:
        while node.letter is None:
            if fileString[index]=="1":
                node = node.right; index+=1
            else:
                node = node.left; index+=1
        decode.append(node.letter)
        node = root
    return "".join(decode)


# calculate compression ratio
# input: input string, freq table, code table
# output: using the formula: ratio = (input-compress)/input
def compressionRatio(input_string, freq_table, code_table):
    str_len = len(input_string)
    if str_len>1:           # check for special case when input is only 1 char, log2(1) = 0
        string_bits = ceil(log2(str_len))
    else:
        string_bits = 1
    compressed_bits = 0
    index = 0
    code_length = []
    for value in code_table.values():       # get the bit length in code table for each char
        code_length.append(len(value))
    for value in freq_table.values():       # compressed bits = freq * bit length
        compressed_bits = compressed_bits + code_length[index]*value
        index+=1
    return ((string_bits-compressed_bits)/string_bits)*100


# print menu
def menu():
    print("Welcome to Huffman Decoder:" \
          "\n1. Encode a file" \
          "\n2. Decode a file" \
          "\n3. Quit\n")


def main():
    menu()
    choice = input("Enter your choice (1-3):")
    if choice.isdigit():
        choice = int(choice)
    while choice != 3:
        if choice == 1:
            filename = input("Enter file name:")
            input_string = openFile(filename)
            freq_table = buildFreqTable(input_string)
            root = create_tree(freq_table)
            code = treeTraverse(root)
            seq = formSequence(input_string, code)
            print("\nThe input string:")
            print(input_string)
            print("\nThe Code Table:")
            print(code)
            print("\nEncode sequence:")
            print(seq)
            print("\ncompressed size = ", end="")
            print(str(len(seq)))
            with io.open(filename[:-4] + ".pkl", 'wb') as outfile: # save the tree object using pickle lib
                pickle.dump(root, outfile)
            outfile.close()
            file = open(filename[:-4] + "_encode.txt", "w") # save the code to filename_encode.txt file
            file.write(seq)
            file.close()
            ratio = compressionRatio(input_string, freq_table, code)
            print('\nCompression ratio is {:04.2f}%'.format(ratio))
            menu()
            choice = input("Enter your choice (1-3):")
            if choice.isdigit():
                choice = int(choice)

        elif choice == 2:
            filename = input("Enter file name:")
            try:
                with io.open(filename[:-11] + ".pkl", 'rb') as infile: # load the tree object stored in .pkl file
                    root = pickle.load(infile)
            except OSError:
                print("cannot open file")
                exit()

            infile.close()
            seq = openFile(filename)
            print('\nInput encoded string:')
            print(seq)
            decode = decompress(seq, root)
            print('\nDecoded string:')
            print(decode)
            menu()
            choice = input("Enter your choice (1-3):")
            if choice.isdigit():
                choice = int(choice)
        elif choice == 3:
            exit()
        else:
            print("Invalid choice")
            choice = input("Enter your choice (1-3):")
            if choice.isdigit():
                choice = int(choice)

# There's a bug in the program: It works when encode a non-English file, such as test5.txt, but if you encode another file
# right after, it does not produce the right output for other files. You have to restart the program.


if __name__=='__main__':
    main()
