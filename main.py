import pygame
import math
from queue import PriorityQueue


SIDE = 800
WIN = pygame.display.set_mode((SIDE, SIDE))
pygame.display.set_caption("A* path visualizer")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
    def __init__(self, row, col, width, total_row):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.side = width
        self.color = WHITE
        self.neighbor = []
        self.total_rows = total_row

    def get_pos(self):
        return self.row, self.col
    def is_closed(self):
        return self.color == RED
    def is_open(self):
        return self.color == GREEN
    def is_barrier(self):
        return self.color == BLACK
    def is_start(self):
        return self.color == ORANGE
    def is_end(self):
        return self.color == TURQUOISE
    def reset(self):
        self.color = WHITE
    def make_start(self):
        self.color = ORANGE
    def make_closed(self):
        self.color = RED
    def make_barrier(self):
        self.color = BLACK
    def make_end(self):
        self.color = TURQUOISE
    def make_open(self):
        self.color = GREEN
    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.side, self.side))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

def huristic_val(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstract_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def make_grid(rows, width):
    grid = []
    gap = width// rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid

def draw_grid(win, rows, width):
    gap = width // rows

    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j*gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_mouse_pos(pos, rows, width):
    gap = width// rows
    x, y = pos

    row = x // gap
    col = y // gap
    return row, col

def AstarAlgo(draw, grid, start, end):
    count = 0
    open = PriorityQueue()
    open.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf")for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf")for row in grid for node in row}
    f_score[start] = huristic_val(start.get_pos(), end.get_pos())

    open_hash = {start}

    while not open.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        cur = open.get()[2]
        open_hash.remove(cur)

        if cur == end:
            reconstract_path(came_from, cur, draw)
            end.make_end()
            return True

        for n in cur.neighbors:
            temp_g = g_score[cur] + 1

            if temp_g < g_score[n]:
                came_from[n] = cur
                g_score[n] = temp_g
                f_score[n] = temp_g + huristic_val(n.get_pos(), end.get_pos())
                if n not in open_hash:
                    count +=1
                    open.put((f_score[n], count, n))
                    open_hash.add(n)
                    n.make_open()
        draw()

        if cur != start:
            cur.make_closed()

    return False
def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = end = None
    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    AstarAlgo(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c or event.key == pygame.K_ESCAPE:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)


    pygame.quit()

main(WIN, SIDE)













