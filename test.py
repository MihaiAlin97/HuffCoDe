import Huffman

if __name__ == "__main__":
    huf = Huffman.Huffman()
    huf.compress(filename="test.txt",save_as="ana",debug = True)
    huf.decompress(filename="ana", save_as="test2",debug=True)