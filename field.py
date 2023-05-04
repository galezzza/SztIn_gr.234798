import random
import time
from heapq import *
from enum import Enum, IntEnum
from queue import PriorityQueue
from collections import deque

import pygame

pygame.init()
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
BLUE = (46, 34, 240)
WINDOW_DIMENSIONS = 900
BLOCK_SIZE = 60
ROCKS_NUMBER = 20
VEGETABLES_NUMBER = 20
VEGETABLES = ('Potato', 'Broccoli', 'Carrot', 'Onion')
BOARD_SIZE = int(WINDOW_DIMENSIONS / BLOCK_SIZE)
WATER_TANK_CAPACITY = 10
GAS_TANK_CAPACITY = 250
SPAWN_POINT = (0, 0)

tractor_image = pygame.transform.scale(pygame.image.load("images/tractor_image.png"), (BLOCK_SIZE, BLOCK_SIZE))
rock_image = pygame.transform.scale(pygame.image.load("images/rock_image.png"), (BLOCK_SIZE, BLOCK_SIZE))
potato_image = pygame.transform.scale(pygame.image.load("images/potato.png"), (BLOCK_SIZE, BLOCK_SIZE))
carrot_image = pygame.transform.scale(pygame.image.load("images/carrot.png"), (BLOCK_SIZE, BLOCK_SIZE))
broccoli_image = pygame.transform.scale(pygame.image.load("images/broccoli.png"), (BLOCK_SIZE, BLOCK_SIZE))
onion_image = pygame.transform.scale(pygame.image.load("images/onion.png"), (BLOCK_SIZE, BLOCK_SIZE))
gas_station_image = pygame.transform.scale(pygame.image.load("images/gas_station.png"), (BLOCK_SIZE, BLOCK_SIZE))
font = pygame.font.Font('freesansbold.ttf', BLOCK_SIZE // 2)


def draw_grid():
    # Set the size of the grid block
    wei = pygame.transform.scale(pygame.image.load("images/wet_earth_tile.jpg"), (BLOCK_SIZE, BLOCK_SIZE))
    dei = pygame.transform.scale(pygame.image.load("images/dry_earth_tile.jpg"), (BLOCK_SIZE, BLOCK_SIZE))
    for x in range(0, BOARD_SIZE):
        for y in range(0, BOARD_SIZE):
            sc.blit(wei, (x * BLOCK_SIZE, y * BLOCK_SIZE))
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(sc, WHITE, rect, 1)


def get_click_mouse_pos():
    x, y = pygame.mouse.get_pos()
    grid_x, grid_y = x // BLOCK_SIZE, y // BLOCK_SIZE
    pygame.draw.rect(sc, BLUE, (grid_x * BLOCK_SIZE, grid_y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
    click = pygame.mouse.get_pressed()
    return (grid_x, grid_y, Direction.RIGHT) if click[0] else False


def draw_interface():
    global sc
    sc = pygame.display.set_mode((WINDOW_DIMENSIONS, WINDOW_DIMENSIONS))
    pygame.display.set_caption("Pole i ciągnik")
    pygame.display.set_icon(pygame.image.load("images/icon.png"))

    sc.fill(BLACK)

    (x, y) = SPAWN_POINT
    tractor = Tractor(x, y, Direction.RIGHT)

    grid = Grid(BOARD_SIZE, BOARD_SIZE, BLOCK_SIZE)
    graph1 = Graph(grid)
    graph1.initialize_graph(grid)

    fl_running = True
    while fl_running:
        draw_grid()
        # region events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                fl_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tractor.rot_center(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    tractor.rot_center(Direction.RIGHT)
                elif event.key == pygame.K_UP:
                    tractor.move(grid=grid)
                elif event.key == pygame.K_RETURN:
                    for y, row in enumerate(grid.grid):
                        for x, col in enumerate(row):
                            if col in [item.value for item in vegetables] and (x, y) == (tractor.x, tractor.y):
                                tractor.collected_vegetables[vegetables(col)] += 1
                                grid.remove_object(x, y)
                                break
                    if (tractor.x, tractor.y) == SPAWN_POINT:
                        tractor.water = WATER_TANK_CAPACITY
                        tractor.gas = GAS_TANK_CAPACITY
            elif event.type == pygame.MOUSEBUTTONDOWN:
                startpoint = (tractor.x, tractor.y, tractor.direction)
                endpoint = get_click_mouse_pos()
                a, c = graph1.a_star(startpoint, endpoint)
                b = getRoad(startpoint, c, a)
                movement(tractor, grid, b)
        updateDisplay(tractor, grid)


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class vegetables(Enum):
    POTATO = 3
    BROCCOLI = 4
    CARROT = 5
    ONION = 6


class types(Enum):
    EMPTY = 0
    ROCK = 1
    POTATO = 3
    BROCCOLI = 4
    CARROT = 5
    ONION = 6


class Grid:
    def __init__(self, width, height, block_size):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.grid = [[types.EMPTY for col in range(BOARD_SIZE)] for row in range(BOARD_SIZE)]
        self.initialize_grid()

    def add_object(self, x, y, type_of_object: types):
        if self.grid[x][y] == types.EMPTY:
            self.grid[x][y] = type_of_object
            return True
        else:
            return False

    def remove_object(self, x, y):
        if self.grid[x][y] != types.EMPTY:
            self.grid[x][y] = types.EMPTY
            return True
        else:
            return False

    def initialize_grid(self):
        for i in range(VEGETABLES_NUMBER):
            x, y = random.randrange(0, BOARD_SIZE), random.randrange(0, BOARD_SIZE)
            if self.grid[x][y] == types.EMPTY and (x, y) != (0, 0):
                self.add_object(x, y, random.choice(list(vegetables)))
            else:
                i -= 1
        for i in range(ROCKS_NUMBER):
            x, y = random.randrange(0, BOARD_SIZE - 1), random.randrange(0, BOARD_SIZE - 1)
            if self.grid[x][y] == types.EMPTY and (x, y) != (0, 0):
                self.add_object(x, y, types.ROCK)
            else:
                i -= 1


class Graph:
    def __init__(self, grid: Grid):
        self.graph = {}
        self.initialize_graph(grid)

    def initialize_graph(self, grid: Grid):
        for y, row in enumerate(grid.grid):
            for x, col in enumerate(row):
                for direction in Direction:
                    self.graph[(x, y, direction)] = get_next_nodes(x, y, direction, grid)

    def a_star(self, start, goal):
        # not finished yet https://www.youtube.com/watch?v=abHftC1GU6w
        queue = PriorityQueue()
        queue.put((0, start))
        cost_visited = {start: 0}
        visited = {start: None}

        returnGoal = goal
        h = lambda start, goal: abs(start[0] - goal[0]) + abs(start[1] - goal[1]) #heuristic function (manhattan distance)

        while not queue.empty():
            cur_cost, cur_node = queue.get()
            if cur_node[0] == goal[0] and cur_node[1] == goal[1]:
                returnGoal=cur_node
                break

            next_nodes = self.graph[cur_node]
            for next_node in next_nodes:
                neigh_cost, neigh_node = next_node

                new_cost = cost_visited[cur_node] + neigh_cost + h(neigh_node, goal)

                if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                    queue.put((new_cost, neigh_node))
                    cost_visited[neigh_node] = new_cost - h(neigh_node, goal)
                    visited[neigh_node] = cur_node
        # print(visited, returnGoal)
        return visited, returnGoal


class Tractor:
    def __init__(self, x, y, direction: Direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.gas = GAS_TANK_CAPACITY
        self.water = WATER_TANK_CAPACITY
        self.collected_vegetables = {vegetables.POTATO: 0, vegetables.BROCCOLI: 0, vegetables.CARROT: 0,
                                     vegetables.ONION: 0}
        self.image = pygame.transform.scale(pygame.image.load("images/tractor_image.png"), (BLOCK_SIZE, BLOCK_SIZE))

    def rot_center(self, direc: Direction):
        self.image = pygame.transform.rotate(self.image, - int(direc) * 90)
        self.direction = Direction(((int(self.direction) + int(direc)) % 4))
        self.gas -= 1
        # print(self.direction)
        return

    def move(self, grid: Grid):
        if self.direction == Direction.UP:
            if self.y > 0:
                self.y -= 1
        elif self.direction == Direction.RIGHT:
            if self.x < BOARD_SIZE - 1:
                self.x += 1
        elif self.direction == Direction.DOWN:
            if self.y < BOARD_SIZE - 1:
                self.y += 1
        elif self.direction == Direction.LEFT:
            if self.x > 0:
                self.x -= 1

        if grid.grid[self.x][self.y] == types.ROCK:
            self.gas -= 12
        else:
            self.gas -= 2
        return


def get_next_nodes(x, y, direction: Direction, grid: Grid):
    check_next_node = lambda x, y: True if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE else False
    way = [0, -1] if direction == Direction.UP else [1, 0] if direction == Direction.RIGHT else [0,
                                                                                                 1] if direction == Direction.DOWN else [
        -1, 0]
    next_nodes = []
    for new_direction in Direction:
        if new_direction != direction:
            if (new_direction - direction != 2) and (new_direction - direction != -2):
                next_nodes.append((1, (x, y, new_direction)))
        else:
            if check_next_node(x + way[0], y + way[1]):
                if grid.grid[x + way[0]][y + way[1]] == types.ROCK:
                    # print(x, y, "to", x + way[0], y + way[1], 'costs 5')
                    next_nodes.append((12, (x + way[0], y + way[1], new_direction)))
                else:
                    next_nodes.append((2, (x + way[0], y + way[1], new_direction)))

    # print(x,y, direction, next_nodes, '\n')
    return next_nodes


def movement(tractor: Tractor, grid: Grid, road):
    n = len(road)
    for i in range(n - 1):
        aA = road[i]
        bB = road[i + 1]
        if aA[0] != bB[0]:
            tractor.move(grid=grid)
        if aA[1] != bB[1]:
            tractor.move(grid=grid)
        if aA[2] != bB[2]:
            if (bB[2].value - aA[2].value == 1) or (bB[2].value - aA[2].value == -3):
                tractor.rot_center(Direction.RIGHT)
            else:
                tractor.rot_center(Direction.LEFT)
        updateDisplay(tractor, grid)
        time.sleep(0.3)


def getRoad(start, goal, visited):
    arr = []
    aFrom = goal
    while aFrom != start:
        arr.append(aFrom)
        aFrom = visited[aFrom]
    arr.append(start)
    brr = arr[::-1]
    # print(brr)
    return brr


def updateDisplay(tractor: Tractor, grid: Grid):
    for y, row in enumerate(grid.grid):
        for x, col in enumerate(row):
            if grid.grid[x][y] == vegetables.POTATO:
                sc.blit(potato_image, (x * BLOCK_SIZE + 5, y * BLOCK_SIZE + 5))
            elif grid.grid[x][y] == vegetables.CARROT:
                sc.blit(carrot_image, (x * BLOCK_SIZE + 5, y * BLOCK_SIZE + 5))
            elif grid.grid[x][y] == vegetables.BROCCOLI:
                sc.blit(broccoli_image, (x * BLOCK_SIZE + 5, y * BLOCK_SIZE + 5))
            elif grid.grid[x][y] == vegetables.ONION:
                sc.blit(onion_image, (x * BLOCK_SIZE + 5, y * BLOCK_SIZE + 5))
            elif grid.grid[x][y] == types.ROCK:
                sc.blit(rock_image, (x * BLOCK_SIZE, y * BLOCK_SIZE))
    sc.blit(gas_station_image, (SPAWN_POINT[0] * BLOCK_SIZE, SPAWN_POINT[1] * BLOCK_SIZE))

    # region text
    vegetables_text = font.render(
        'Potato: ' + str(tractor.collected_vegetables[vegetables.POTATO]) + ' Broccoli: ' + str(
            tractor.collected_vegetables[vegetables.BROCCOLI]) + ' Carrot: ' + str(
            tractor.collected_vegetables[vegetables.CARROT]) + ' Onion: ' + str(
            tractor.collected_vegetables[vegetables.ONION]), True, WHITE, BLACK)
    vegetables_textrect = vegetables_text.get_rect()
    vegetables_textrect.center = (WINDOW_DIMENSIONS // 2, WINDOW_DIMENSIONS - 30)
    sc.blit(vegetables_text, vegetables_textrect)

    gas_text = font.render('Gas tank: ' + str(tractor.gas), True, WHITE, BLACK)
    gas_textrect = gas_text.get_rect()
    gas_textrect.center = (WINDOW_DIMENSIONS // 4 * 3, 20)
    sc.blit(gas_text, gas_textrect)
    # endregion

    sc.blit(tractor.image, (tractor.x * BLOCK_SIZE + 5, tractor.y * BLOCK_SIZE + 5))
    pygame.display.update()

    pygame.time.Clock().tick(60)

