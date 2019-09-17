import test
import CountChars

hf=test.Huffman()
hf.compress('text.txt')
print(hf.tree)
print(hf.table)
print(hf.no_chars_uncompressed," ",hf.no_chars_table," ",hf.no_chars_compressed)

hf.decompress('text.huff')