



import string
import threading
import queue

CharQueue = queue.Queue(100)

lock = threading.Lock()

dictionary = {char: 0 for char in string.printable}

copy = {char: 0 for char in string.printable}

for char in string.printable:4
    CharQueue.put(char)
    
end_flag = False


class HuffmanTree():
    def __init__(self,filename):
        global copy
        self.start_n_threads(20,filename)
        self.ftree={key:copy[key] for key in copy.keys() if copy[key]>0}
        self.huffman_tree=[]
        self.heap=[]
        self.create_heap(list(self.ftree.values()))
        self.create_huffman_tree()


    class CountChar(threading.Thread):
        def __init__(self, name, filename):
            threading.Thread.__init__(self)
            self.name = name
            self.filename = filename

        def countChar(self, char):
            global copy
            global end_flag

            file = open(self.filename, 'r')
            text = file.read()
            count = 0
            for el in text:
                if (el == char): count = count + 1
            copy[char] = count
            if (char == '\x0c'):
                end_flag = True

        def run(self):
            global end_flag
            global CharQueue
            while (CharQueue.empty() == False):
                search = CharQueue.get()
                with lock:
                    self.countChar(search)

    def start_n_threads(self,n, filename):
        threads = []
        for i in range(0, n):
            thread = self.CountChar('Thread' + str(i), filename)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def create_heap(self,list):
        list = [''] + list
        list = self.min_heap(list, (len(list) - 1) // 2)
        self.heap = list

    def min_heap(self,list, index):
        if (index == 0): return list
        if (list[index] > list[index * 2]):
            aux = list[index]
            list[index] = list[index * 2]
            list[index * 2] = aux
        if (index * 2 < len(list) - 1):
            if (list[index] > list[index * 2 + 1]):
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
        list.append(999999999)
        for i in range(1, (len(list) - 1) // 2):
            if (list[i] > list[i * 2]): check = False
            if (list[i] > list[i * 2 + 1]): check = False
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

        if (self.heap[2] < self.heap[3]):
            minel = [self.heap[1], self.heap[2]]
            self.heap.remove(self.heap[2])
            self.heap.remove(self.heap[1])
        else:
            minel = [self.heap[1], self.heap[3]]
            self.heap.remove(self.heap[3])
            self.heap.remove(self.heap[1])

            self.heap = self.min_heap(self.heap, (len(self.heap) - 1) // 2)
        return minel

    def create_huffman_tree(self):

        min_nodes = []

        i = 0
        while (len(self.heap) > 2):

            min_nodes = self.extract2()
            last = min_nodes
            self.heap = self.heap + [min_nodes[0] + min_nodes[1]]

            self.heap = self.min_heap(self.heap, (len(self.heap) - 1) // 2)
            min_nodes.insert(0, min_nodes[0] + min_nodes[1])
            self.huffman_tree.insert(0, min_nodes)

    def print_tree(self):
        print(self.huffman_tree)

    def print_char_codes(self):
        self.print_codes('','',0)

    def print_codes(self,codel, coder, level):

        if (level == len(self.huffman_tree) - 1):
            print('Code for value ', self.huffman_tree[level][1], ' and char ', self.get_key(self.ftree, self.huffman_tree[level][1]),
                  ' is :', codel + '0')
            print('Code for value ', self.huffman_tree[level][2], ' and char ', self.get_key(self.ftree, self.huffman_tree[level][2]),
                  ' is :', codel + '1')

            return 0

        if (self.check_leaf(level, 1) == True):
            print('Code for value ', self.huffman_tree[level][1], ' and char ', self.get_key(self.ftree, self.huffman_tree[level][1]),
                  ' is :', codel + '0')
        else:
            self.print_codes(codel + '0', coder + '0', self.get_next_index(level, 1))

        if (self.check_leaf(level, 2) == True):
            print('Code for value ', self.huffman_tree[level][2], ' and char ', self.get_key(self.ftree, self.huffman_tree[level][2]),
                  ' is :', coder + '1')
        else:
            self.print_codes(codel + '1', coder + '1', self.get_next_index(level, 2))

    def check_leaf(self,level, position):

        if (level <len(self.huffman_tree) - 2):
            if (self.huffman_tree[level][position] == self.huffman_tree[level + 2][0]): return False

        if (level < len(self.huffman_tree) - 3):
            if (self.huffman_tree[level][position] == self.huffman_tree[level + 3][0]): return False

        if (level < len(self.huffman_tree) - 4):
            if (self.huffman_tree[level][position] == self.huffman_tree[level + 4][0]): return False

        if (self.huffman_tree[level][position] == self.huffman_tree[level + 1][0]): return False

        return True

    def get_next_index(self,level, position):

        if (level < len(self.huffman_tree) - 2):
            if (self.huffman_tree[level][position] == self.huffman_tree[level + 2][0]): return level + 2

        if (level < len(self.huffman_tree) - 3):
            if (self.huffman_tree[level][position] == self.huffman_tree[level + 3][0]): return level + 3

        if (level < len(self.huffman_tree) - 4):
            if (self.huffman_tree[level][position] == self.huffman_tree[level + 4][0]): return level + 4

        if (self.huffman_tree[level][position] == self.huffman_tree[level + 1][0]): return level + 1

    def get_key(self,dictio: dict, val):
        for key in dictio.keys():
            if dictio[key] == val: return key
        return 0

