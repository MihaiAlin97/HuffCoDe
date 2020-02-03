import math

from copy import copy

class MinHeapNode:
    def __init__(self,node):
        self.value = node

class MinHeap:
    def __init__(self):
        self.heap = []

    def heapify(self,index):

##assume root is the smallest of the subtree
        smallest = index
##left child index
        left = index * 2 + 1
##right child index
        right = index * 2 + 2

        n = len(self.heap)

##check if left child is smaller than parent -> store the index if true
        if left < n and (self.heap[smallest]).value > (self.heap[left]).value:

            smallest = left

##check if right child is smaller than parent -> store tbe index if true
        if right < n and (self.heap[smallest]).value > (self.heap[right]).value:

            smallest = right

##if the root is not smaller than it's children , do the swapping and apply the same rules to its children
        if smallest != index :
            aux = copy(self.heap[index])
            self.heap[index] = copy(self.heap[smallest])
            self.heap[smallest] = copy(aux)

            self.heapify(smallest)

    def build_heap(self,list):

        ##discard nodes that are not instances of MinHeapNode
        self.heap = [node for node in list if isinstance(node,MinHeapNode)]

##last non - leaf node in the heap from root to bottom

        start = math.floor((len(self.heap))/2) - 1

        for index in range(start, -1, -1):

            self.heapify(index)

    def delete_nodes(self, *nodes):

        for node in nodes:

            if isinstance(node, list):

                for subnode in node:
                    self.heap.remove(subnode)
            else:

                self.heap.remove(node)

        start = math.floor((len(self.heap)) / 2) - 1

        for index in range(start, -1, -1):
            self.heapify(index)

    def insert_nodes(self, *nodes):

        for node in nodes:

            if isinstance(node, list):

                for subnode in node:
                    if isinstance(subnode,MinHeapNode):
                        self.heap.append(subnode)
            else:
                if isinstance(node,MinHeapNode):
                    self.heap.append(node)

        start = math.floor((len(self.heap)) / 2) - 1

        for index in range(start, -1, -1):
            self.heapify(index)

    def extract(self):

        root = self.heap[0]

        self.delete_nodes(root)

        return root

    def print_heap(self):
        l = [node.value for node in self.heap]
        print("Created Min heap is ",l,sep=" ")



if __name__ == '__main__':
    arr = [8,9,5,6,1,3]
    arr = [MinHeapNode(element) for element in arr]
    print(arr)
    hp = MinHeap()
    hp.build_heap(arr)
    hp.print_heap()

