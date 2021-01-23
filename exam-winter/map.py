import sys
import typing as tp

CAN_GO = "."
IS_VISITED = "☺"
BOUND = "☒"
DESTINATION = "☼"


class labyrinth:
    def __init__(self, filename):
        self.map = []
        with open(filename, "r") as f:
            for i, line in enumerate(f):
                nline = []
                j = 0
                for element in line.rstrip():
                    nline.append(element)
                    if element == IS_VISITED:
                        self.start = (i, j)
                    elif element == BOUND:
                        self.finale = (i, j)
                    j += 1
                self.map.append(nline)
        self.rows = len(self.map)
        self.cols = len(self.map[0])

    def __repr__(self):
        result = ""
        for i, line in enumerate(self.map):
            for char in line:
                result += char
            if i < len(self.map) - 1:
                result += "\n"
        return result

    def isSafe(self, visited, x, y):
        if self.map[x][y] == BOUND or visited[x][y] == True:
            return False
        return True

    def isValid(self, x, y):
        if x < self.rows and y < self.cols and x >= 0 and y >= 0:
            return True
        return False

    def solve(self):
        visited = []
        for i in range(self.rows):
            visited.append([])
            for j in range(self.cols):
                visited[i].append(False)

        self.print_solved(
            self.step(visited, self.start[1], self.start[0], cur_path=[], min_path=[], min_dist=-1)
        )

    def step(
        self,
        visited: tp.List[tp.List[bool]],
        i: int,
        j: int,
        cur_path,
        min_path,
        min_dist: int,
    ):
        if (i, j) == self.finale:
            if len(cur_path) <= min_dist or min_dist == -1:
                min_path.clear()
                min_path.extend(cur_path)
                min_path.append((j, i))
                min_dist = len(min_path)
            return min_path

        visited[i][j] = True
        cur_path.append((j, i))

        possible_paths = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
        for path in possible_paths:
            if self.isValid(path[0], path[1]) and self.isSafe(visited, path[0], path[1]):
                self.step(visited, path[0], path[1], cur_path, min_path, min_dist)
        visited[i][j] = False
        cur_path.pop()

    def print_solved(self, min_path):
        new_lab = self.map.copy()
        for path in min_path:
            new_lab[path[0]][path[1]] = IS_VISITED
        result = ""
        for i, line in enumerate(new_lab):
            for char in line:
                result += char
            if i < len(new_lab) - 1:
                result += "\n"
        print(result)


if __name__ == "__main__":
    given_filename = sys.argv[1]
    a = labyrinth(filename=given_filename)
    a.solve()
