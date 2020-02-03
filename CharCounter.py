import string
import threading
import queue


class CharCounter(threading.Thread):
    def __init__(self,filename ,char_queue , characters , end_flag , lock):
        threading.Thread.__init__(self)
        self.filename = filename
        self.char_queue = char_queue
        self.characters = characters
        self.end_flag = end_flag
        self.lock = lock

    def count(self, char):

        file = open(self.filename, 'r')
        text = file.read()
        count = 0

        for el in text:
            if (el == char): count = count + 1
        self.characters[char] = count
        if (char == '\x0c'):
            self.end_flag = True

    def run(self):
        while (self.char_queue.empty() == False):
            search = self.char_queue.get()
            with self.lock:
                self.count(search)

##function for getting frequence of each distinct char inside a file
def get_frequencies(filename):
    threads = []

    ##here each distinct char is stored
    char_queue = queue.Queue(100)

    lock = threading.Lock()

    ##create a dict of frequence for each unique char - > char:frequence
    characters = {char: 0 for char in string.printable}

    for char in string.printable:
        char_queue.put(char)

    ##when counting each char , if the end is reached end_flag is set on true
    end_flag = False

    ##spawn threads
    for i in range(0, 30):
        thread = CharCounter(filename , char_queue , characters , end_flag , lock)
        threads.append(thread)
        thread.start()
    ##join threads
    for thread in threads:
        thread.join()

    result = {key:[characters[key],0] for key in characters.keys() if characters[key] > 0}

    return result

if __name__ == "__main__":
    print(get_frequencies("test.txt"))

