import sys
import os


class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
    else:
        fp = sys.argv[1]
        current_dir: str = os.getcwd()

        with open(os.path.join(current_dir, fp), 'r') as f:
            text_in = f.read()
        print(text_in)
