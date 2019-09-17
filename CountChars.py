import string
import threading
import queue

CharQueue = queue.Queue(100)

lock = threading.Lock()

characters = {char: 0 for char in string.printable}

for char in string.printable:
    CharQueue.put(char)

end_flag = False


class CountChars(threading.Thread):
    def __init__(self, name, filename):
        threading.Thread.__init__(self)
        self.name = name
        self.filename = filename

    def count(self, char):

        global characters
        global end_flag

        file = open(self.filename, 'r')
        text = file.read()
        count = 0

        for el in text:
            if (el == char): count = count + 1
        characters[char] = count
        if (char == '\x0c'):
            end_flag = True

    def run(self):
        global end_flag
        global CharQueue
        while (CharQueue.empty() == False):
            search = CharQueue.get()
            with lock:
                self.count(search)


def get_frequencies(filename):
    threads = []
    global characters
    global CharQueue
    for i in range(0, 30):
        thread = CountChars('Thread' + str(i), filename)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

    result = [[key, characters[key]] for key in characters.keys() if characters[key] > 0]
    characters = {char: 0 for char in string.printable}
    for char in string.printable:
        CharQueue.put(char)

    return result

