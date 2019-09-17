import CountChars
class Huffman():

    def __init__(self):
        self.reached_end = False
        self.tree = []
        self.table = {}
        self.heap = []
    def compress(self,filename):
        self.reached_end = False
        self.tree = []
        self.table ={}
        self.heap = []

        self.frequencies = CountChars.get_frequencies(filename)
        self.dictionary_of_frequencies={x[0]:x[1] for x in self.frequencies}
        self.create_heap(self.frequencies)
        self.create_tree()
        self.create_table('','',0)

        self.write_file(filename)


    def write_file(self,filename):
        filename=filename[:-3]+'huff'
        self.no_chars_uncompressed = self.tree[0][0][1]
        self.no_chars_table = len(self.table) * 2

        total_no_bits = 0
        for key in self.table.keys():
            total_no_bits = total_no_bits + self.dictionary_of_frequencies[self.table[key]] * len(key)

        self.no_chars_compressed = total_no_bits // 8 + 1

        "init the three ints"

        reversed_table={y:x for x,y in self.table.items()}
        print(reversed_table)

        with open(filename, "wb") as f:
            f.write((self.no_chars_uncompressed).to_bytes(4, 'big'))
            f.write((self.no_chars_table).to_bytes(4, 'big'))
            f.write((self.no_chars_compressed).to_bytes(4, 'big'))

            for key in self.table.keys():
                f.write(bytes(self.table[key],encoding='ascii'))
                f.write(int(self.add_leading_zeros(key),2).to_bytes(1,'big'))

            char=''
            bit_supply=''
            end_flag=False
            compression_done=False
            with open(filename[:-4]+'txt','r')as g:
                while(compression_done==False):
                    if(end_flag==False):
                        before = g.tell()
                        char = g.read(1)
                        after = g.tell()

                    if (before == after): end_flag=True
                    if (end_flag==False):
                        bit_supply = bit_supply + reversed_table[char]

                    if len(bit_supply)>8 and end_flag==False:
                        print(bit_supply[:8])
                        f.write(int(bit_supply[:8], 2).to_bytes(1, 'big'))
                        bit_supply=bit_supply[8:]

                    if len(bit_supply)<=8 and end_flag==True:
                        print(self.add_final_zeros(bit_supply))
                        f.write(int(self.add_final_zeros(bit_supply),2).to_bytes(1,'big'))
                        compression_done = True

                    if len(bit_supply)>8 and end_flag==True:
                        while(compression_done==False):
                            if(len(bit_supply)<=8):
                                print(self.add_final_zeros(bit_supply))
                                f.write(int(self.add_final_zeros(bit_supply), 2).to_bytes(1, 'big'))
                                compression_done = True
                                break
                            print(bit_supply[:8])
                            bit_supply = bit_supply[8:]

    def decompress(self,filename):

        with open(filename, "rb") as f:
            bytes=f.read(4)
            no_chars_uncompressed=int(bin(bytes[0])[2:]+bin(bytes[1])[2:]+bin(bytes[2])[2:]+bin(bytes[3])[2:],2)
            print(no_chars_uncompressed)

            bytes = f.read(4)
            no_chars_table = int(bin(bytes[0])[2:] + bin(bytes[1])[2:] + bin(bytes[2])[2:] + bin(bytes[3])[2:],2)
            print(no_chars_table)

            bytes = f.read(4)
            no_chars_compressed = int(bin(bytes[0])[2:] + bin(bytes[1])[2:] + bin(bytes[2])[2:] + bin(bytes[3])[2:],2)
            print(no_chars_compressed)

            chars_table=f.read(no_chars_table)



    def add_leading_zeros(self,string):
        leading_zeros = ''
        for i in range(0, 8 - len(string)):
            leading_zeros = '0' + leading_zeros
        string = leading_zeros + string
        return string
    def add_final_zeros(self,string):
        zeros = ''
        for i in range(0, 8 - len(string)):
            zeros = zeros+'0'
        string = string+zeros
        return string

    def create_heap(self,list):
        list = [' '] + list
        list = self.min_heap(list, (len(list) - 1) // 2)
        self.heap = list

    def min_heap(self,list, index):
        if (index == 0): return list
        if (list[index][1] > list[index * 2][1]):
            aux = list[index]
            list[index] = list[index * 2]
            list[index * 2] = aux
        if (index * 2 < len(list) - 1):
            if (list[index][1] > list[index * 2 + 1][1]):
                aux = list[index]
                list[index] = list[index * 2 + 1]
                list[index * 2 + 1] = aux

        if (index == 1):
            if (self.checkheap(list) == True): return list
            if (self.checkheap(list) == False): return self.min_heap(list, ((len(list) - 1) // 2))

        else:
            return self.min_heap(list, index - 1)

    def checkheap(self,list):
        check = True
        list.append(['notchar',999999999])
        for i in range(1, (len(list) - 1) // 2):
            if (list[i][1] > list[i * 2][1]): check = False
            if (list[i][1] > list[i * 2 + 1][1]): check = False
        del (list[-1])
        return check

    def extract2(self):
        if (len(self.heap) == 2):
            last = self.heap[1]
            self.heap.remove(self.heap[1])

            return [0, last]
        if (len(self.heap) == 3):
            minel = [self.heap[1], self.heap[2]]
            self.heap.remove(self.heap[2])
            self.heap.remove(self.heap[1])
            return minel

        if (self.heap[2][1] < self.heap[3][1]):
            minel = [self.heap[1], self.heap[2]]
            self.heap.remove(self.heap[2])
            self.heap.remove(self.heap[1])
        else:
            minel = [self.heap[1], self.heap[3]]
            self.heap.remove(self.heap[3])
            self.heap.remove(self.heap[1])

            self.heap = self.min_heap(self.heap, (len(self.heap) - 1) // 2)
        return minel

    def create_tree(self):
        while (len(self.heap) > 2):

            min_nodes = self.extract2()

            self.heap = self.heap + [[min_nodes[0][0] + min_nodes[1][0],min_nodes[0][1] + min_nodes[1][1]]]

            self.heap = self.min_heap(self.heap, (len(self.heap) - 1) // 2)

            min_nodes.insert(0, [min_nodes[0][0] + min_nodes[1][0], min_nodes[0][1] + min_nodes[1][1]])
            self.tree.insert(0,min_nodes)




    def create_table(self,codel, coder, level):


        if ((level == len(self.tree) - 1)and(self.reached_end==False)):
            self.table[codel+'0']=self.tree[level][1][0]

            self.table[codel + '1'] = self.tree[level][2][0]

            self.reached_end=True
            return 0

        if((level == len(self.tree) - 1)and(self.reached_end == True)):
            return 0

        if (self.check_leaf(level, 1) == True):

            self.table[codel + '0'] = self.tree[level][1][0]
        else:
            self.create_table(codel + '0', coder + '0', self.get_next_index(level, 1))

        if (self.check_leaf(level, 2) == True):

            self.table[coder + '1'] = self.tree[level][2][0]
        else:
            self.create_table(codel + '1', coder + '1', self.get_next_index(level, 2))

    def check_leaf(self,level, position):
        "check if the same char appears in the next 4 levels"
        "if it does appear,return False,meaning it's not a leaf in the tree"
        "otherwise return True"

        for i in range(2,len(self.tree)//3):
            if (level < len(self.tree) - i):
                if (self.tree[level][position][0] == self.tree[level + i][0][0]): return False

        if (level < len(self.tree) - 2):
            if (self.tree[level][position][0] == self.tree[level + 2][0][0]): return False

        if (level < len(self.tree) - 3):
            if (self.tree[level][position][0] == self.tree[level + 3][0][0]): return False

        if (level < len(self.tree) - 4):
            if (self.tree[level][position][0] == self.tree[level + 4][0][0]): return False

        if (self.tree[level][position][0] == self.tree[level + 1][0][0]): return False

        return True

    def get_next_index(self,level, position):
        "check if the same char appears in the next 4 levels;if it appears,return the index"

        for i in range(2,len(self.tree)//3):
            if (level < len(self.tree) - i):
                if (self.tree[level][position][0] == self.tree[level + i][0][0]): return level + i

        if (level < len(self.tree) - 2):
            if (self.tree[level][position][0] == self.tree[level + 2][0][0]): return level + 2

        if (level < len(self.tree) - 3):
            if (self.tree[level][position][0] == self.tree[level + 3][0][0]): return level + 3

        if (level < len(self.tree) - 4):
            if (self.tree[level][position][0] == self.tree[level + 4][0][0]): return level + 4

        if (self.tree[level][position][0] == self.tree[level + 1][0][0]): return level + 1

