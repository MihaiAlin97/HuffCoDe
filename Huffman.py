
from MinHeap import MinHeap,MinHeapNode
from copy import copy
from CharCounter import get_frequencies
import logging

class HuffmanNode(MinHeapNode):

    def __init__(self,node,left,right):
        super().__init__(node)
        self.left = left
        self.right = right
        self.code = ''
        self.char = ''

class Huffman:

    def __init__(self):
        self.heap = MinHeap()
        self.root = None
        self.frequencies = {}
        self.translation_dict = {}

    def compress(self,filename,save_as = None,debug = None):

        self.obtain_frequencies(filename)

        ##create a list of Huffman nodes
        node_values = [HuffmanNode(value[0],0,0) for value in self.frequencies.values()]

        ##build a min heap of that list
        self.heap.build_heap(node_values)

        self.heap.print_heap()

        ##create the huffman tree
        self.create_huffman_tree()


        ##obtain codes and corresponding letter of each leaf node
        self.assign_codes_and_chars(self.root)
        self.print_tree(self.root)

        ##create a dictionary of structure char:prefix code
        self.setup_translation_dict(self.root)
        self.translate(filename,)


    def decompress(self,filename,save_as = None, debug = None):
        ##function to decompress a .huf file
        ## first take one char -> obtain ascii integer value ->convert to binary and pad it with 0 until you have a 8-lenght string -
        ##do that for all chars in text then put all 8 bit strings together
        ##init node with the root -> if value is 0 go to root's left , if it is 1 go to root's right
        ##do that until a leaf node is reach,then return to root

        if self.check_extension(filename, '.huf') == True:
            pass
        else:
            strip = filename.strip()
            if strip.isspace():
                logging.error(f"The filename is empty")
                return
            else:
                logging.warning(f"Filename{filename} does not have .huf extension.")

        if save_as == None:
            pass

        file = open(filename, 'r',encoding="utf-8")
        text = file.read()

        translated_text = ''

        for i,char in enumerate(text):
            if char == '\x0c':
                break
            integer_value = ord(char)
            binary_value = bin(integer_value)
            binary_value = binary_value[2:]

            if i != len(text) - 1:
                string_representation = self.add_leading_zeros(binary_value)
                print(f"Decompression: UTF-8 char: {char}, integer value: {integer_value}, bin value: {binary_value}, padded bin value: {string_representation}")


            else:
                string_representation = binary_value
                print("last")
                print(f"Decompression: UTF-8 char: {char}, integer value: {integer_value}, bin value: {binary_value}, padded bin value: {string_representation}")

            translated_text = translated_text + string_representation



        print(f"Decompression: Original text {text}")
        print(f"Decompression: Translated text {translated_text}")

        decompressed_text = ''

        node = self.root

        ##add one additional char that signals the end
        translated_text = translated_text + 'e'

        for char in translated_text:
            #print(char)
            #print(node.char,node.code, node.left, node.right)

            if node.right == 0 :
                print("reached leaf node ",node.char," node is back at root")
                decompressed_text = decompressed_text + node.char
                node = self.root
            if char == '0':
                print("at 0 going left")
                node = node.left
            if char == '1':
                print("at 1 going right")
                node = node.right

        print(decompressed_text)
        file = open(save_as, 'w', encoding="utf-8")
        file.write(decompressed_text)




    def add_leading_zeros(self,byte):
        if(len(byte)<8):
            no = 8 - len(byte)
            for i in range(0, no):
                byte = '0' + byte
            return byte
        return byte

    def translate(self,filename,save_as = None, debug = None):
        print(f"Translation dict {self.translation_dict}")


        filename2 = filename.split(".")[0] + ".huf"

        print(filename2)

        file = open(filename, 'r')
        text = file.read()

        translated_text = ''

        ##we take each char from original file and replace it with its prefix code
        for char in text:
            if char == '\x0c':
                break
            translated_text = translated_text + self.translation_dict[char]
        print(f"Compression: Original text {text}")
        print(f"Compression:   Translated text {translated_text}")

        ##we break the text into 8 value strings
        byte_array = self.bytes(translated_text, 8)

        ##we convert the 8 value string into integer, then into char (int value represents the ascii value)

        with open(filename2, "w",encoding="utf-8") as f:

            for byte in byte_array:
                int_val = int(byte, 2)
                char_val = chr(int_val)

                f.write(char_val)

                print(f"Compression: bin value: {byte}, integer value: {int_val}, UTF-8 char: {char_val}")


    def bytes(self,list, size):
        ##helper function to separate binary string into bytes
        return (list[pos:pos + size] for pos in range(0, len(list), size))

    def check_extension(self,filename, extension):
        ##helper function to check if a string has last chars in the extension
        if extension == (filename[len(filename) - len(extension):len(filename)]):
            return True
        else:
            return False
    def replace_extension(self,filename,ext1,ext2):

        return filename.replace(ext1,ext2)



    def obtain_frequencies(self,filename):
        ##the count of each distinct symbol in the file

        result = get_frequencies(filename)
        self.frequencies = copy(result)
        print(self.frequencies)

    def assign_char(self, node ):
        ##this function is used to add char value to Huffman node
        for key in self.frequencies.keys():

            ##the vaalue of key in dict is a list with 2 elems consisting of char frequence and : 1 if char was already assigned, 1 otherwise

            ##print(f"debug assign char  {node.value} {key} {self.frequencies[key][0]} {self.frequencies[key][1]}")

            if self.frequencies[key][0] == node.value and self.frequencies[key][1] == 0:
                node.char = key
                self.frequencies[key][1] = 1
                return

    def create_huffman_tree(self):


        while( len(self.heap.heap) > 1 ):

            ##we extract two values from MinHeap and create two nodes
            ##all leaf nodes have their children 0

            l = self.heap.extract()
            r = self.heap.extract()

            parent_node = HuffmanNode(l.value + r.value,l,r)

            ##push node's value into MinHeap
            self.heap.insert_nodes(parent_node)

            ##print(f"created node {parent_node.value} of {l.value} and {r.value} extracted")


        self.root = self.heap.extract()
        self.root.left = l
        self.root.right = r

    def assign_codes_and_chars(self,node):

        if node.right == 0:
            self.assign_char(node)

            ##print(f"debug {node.value} {node.char}")

        if hasattr(node.left, 'value'):
            node.left.code = node.code + '0'
            self.assign_codes_and_chars(node.left)

        if hasattr(node.right,'value'):
            node.right.code = node.code + '1'
            self.assign_codes_and_chars(node.right)

    def setup_translation_dict(self,node):

        if node.right == 0:
            self.translation_dict[node.char] = node.code

        if hasattr(node.left, 'value'):
            self.setup_translation_dict(node.left)

        if hasattr(node.right,'value'):
            self.setup_translation_dict(node.right)



    def print_tree(self,node):

        print(f"node: {node.value} , code : {node.code}")

        if hasattr(node.left, 'value') and hasattr(node.right, 'value'):

            print(f" children :{node.left.value},{node.right.value}")

        if node.right == 0:
            print(f"reached end at {node.value} {node.char}")

        if hasattr(node.left, 'value'):
            self.print_tree(node.left)

        if hasattr(node.right,'value'):
            self.print_tree(node.right)

if __name__ == "__main__":
    huf = Huffman()
    huf.compress  (filename="test.txt", debug=True,save_as="test.huf")
    huf.decompress(filename="test.huf", save_as="test2",debug=True)

