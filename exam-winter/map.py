import sys

CAN_GO = '.'
VISITED = '☺'
BOUND = '☒'
DESTINATION = '☼'

class labyrinth():
    def __init__(self, filename):
        self.map = []
        with open(filename, "r") as f:
            for i, line in enumerate(f):
                nline = []
                j = 0
                for element in line.rstrip():
                    nline.append(element)
                    if element == VISITED:
                        self.start = (i,j)
                    elif element == BOUND:
                        self.finale = (i,j)
                    j += 1
                self.map.append(nline)

    def __repr__(self):
        result = ""
        for i, line in enumerate(self.map):
            for char in line:
                result += char
            if i < len(self.map) - 1:
                result += "\n"
        return result

def main():
    given_filename = sys.argv[1]
    a = labyrinth(filename=given_filename)
    print(a)

main()