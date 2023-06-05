import os
import random
import time
from enum import Enum, IntEnum
from queue import PriorityQueue
from threading import Thread
from recognition_v1 import proverka

import pygame
#from recognition_v1.proverka import *

from IC3 import tree

pygame.init()
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
BLUE = (46, 34, 240)
WINDOW_DIMENSIONS = 900
BLOCK_SIZE = 60
ROCKS_NUMBER = 20
VEGETABLES_NUMBER = 20
VEGETABLES = ('Potato', 'Broccoli', 'Carrot', 'Capsicum')
BOARD_SIZE = int(WINDOW_DIMENSIONS / BLOCK_SIZE)
WATER_TANK_CAPACITY = 10
GAS_TANK_CAPACITY = 250
SPAWN_POINT = (0, 0)
SKLEP_POINT = (14, 14)
TIMEOUT = 1

uio = proverka.VegebatlesRecognizer()

tractor_image = pygame.transform.scale(pygame.image.load("images/tractor_image.png"), (BLOCK_SIZE, BLOCK_SIZE))
rock_image = pygame.transform.scale(pygame.image.load("images/rock_image.png"), (BLOCK_SIZE, BLOCK_SIZE))
potato_image = pygame.transform.scale(pygame.image.load("images/potato.png"), (BLOCK_SIZE, BLOCK_SIZE))
carrot_image = pygame.transform.scale(pygame.image.load("images/carrot.png"), (BLOCK_SIZE, BLOCK_SIZE))
broccoli_image = pygame.transform.scale(pygame.image.load("images/broccoli.png"), (BLOCK_SIZE, BLOCK_SIZE))
onion_image = pygame.transform.scale(pygame.image.load("images/onion.png"), (BLOCK_SIZE, BLOCK_SIZE))
capsicum_image = pygame.transform.scale(pygame.image.load("images/capsicum.png"), (BLOCK_SIZE, BLOCK_SIZE))
unknown_image = pygame.transform.scale(pygame.image.load("images/unknown.png"), (BLOCK_SIZE, BLOCK_SIZE))
gas_station_image = pygame.transform.scale(pygame.image.load("images/gas_station.png"), (BLOCK_SIZE, BLOCK_SIZE))
gas_station_closed_image = pygame.transform.scale(pygame.image.load("images/gas_station_closed.png"),
                                                  (BLOCK_SIZE, BLOCK_SIZE))
sklep_station_image = pygame.transform.scale(pygame.image.load("images/storage_open.png"), (BLOCK_SIZE, BLOCK_SIZE))
sklep_closed_station_image = pygame.transform.scale(pygame.image.load("images/storage_closed.png"),
                                                    (BLOCK_SIZE, BLOCK_SIZE))
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
    def returnFun():
        for y, row in enumerate(grid.grid):
            for x, col in enumerate(row):
                if grid.grid[tractor.x][tractor.y] in vegetables:
                    if tractor.collected_vegetables[grid.grid[tractor.x][tractor.y]] < 5:
                        tractor.collected_vegetables[grid.grid[tractor.x][tractor.y]] += 1
                        grid.remove_object(tractor.x, tractor.y)
                    else:
                        print("tractor storage is full")
                        return
        if (tractor.x, tractor.y) == SPAWN_POINT:
            tractor.water = WATER_TANK_CAPACITY
            tractor.gas = GAS_TANK_CAPACITY
        if (tractor.x, tractor.y) == SKLEP_POINT:
            tractor.collected_vegetables = {vegetables.POTATO: 0, vegetables.BROCCOLI: 0, vegetables.CARROT: 0,
                                            vegetables.CAPSICUM: 0}

    global sc
    sc = pygame.display.set_mode((WINDOW_DIMENSIONS, WINDOW_DIMENSIONS))
    pygame.display.set_caption("Pole i ciągnik")
    pygame.display.set_icon(pygame.image.load("images/icon.png"))

    sc.fill(BLACK)

    (x, y) = SPAWN_POINT
    tractor = Tractor(x, y, Direction.RIGHT)

    grid = Grid(BOARD_SIZE, BOARD_SIZE, BLOCK_SIZE)
    graph1 = Graph(grid)
    t2 = Thread(target=close_open, args=(grid,))
    t2.setDaemon(True)
    t2.start()
    fl_running = True
    determine_thread = Thread(target=grid.determine)
    determine_thread.setDaemon(True)
    determine_thread.start()
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
                    returnFun()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                startpoint = (tractor.x, tractor.y, tractor.direction)
                endpoint = get_click_mouse_pos()
                decisionTree(startpoint, endpoint, tractor, grid, graph1)
                # a, c = graph1.a_star(startpoint, endpoint)
                # b = getRoad(startpoint, c, a)
                # movement(tractor, grid, b)
        updateDisplay(tractor, grid)

    # graph1.initialize_graph(grid)


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class vegetables(Enum):
    POTATO = 3
    BROCCOLI = 4
    CARROT = 5
    CAPSICUM = 6
    UNKNOWN = 7


class types(Enum):
    EMPTY = 0
    ROCK = 1
    POTATO = 3
    BROCCOLI = 4
    CARROT = 5
    CAPSICUM = 6
    UNKNOWN = 7


class Grid:
    def __init__(self, width, height, block_size):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.grid = [[types.EMPTY for col in range(BOARD_SIZE)] for row in range(BOARD_SIZE)]
        self.photo_paths = [['' for col in range(BOARD_SIZE)] for row in range(BOARD_SIZE)]
        self.vegetables_locations = []
        self.initialize_grid()
        self.is_gas_station_closed = False
        self.is_storage_closed = False

    def add_object(self, x, y, type_of_object):
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
                if self.add_object(x, y, vegetables.UNKNOWN):  # random.choice(list(vegetables)))
                    self.vegetables_locations.append((x, y))
                self.photo_paths[x][y] = get_random_photo_path()
            else:
                i -= 1
        for i in range(ROCKS_NUMBER):
            x, y = random.randrange(0, BOARD_SIZE - 1), random.randrange(0, BOARD_SIZE - 1)
            if self.grid[x][y] == types.EMPTY and (x, y) != (0, 0):
                self.add_object(x, y, types.ROCK)
            else:
                i -= 1

    def determine(self):

        for x, y in self.vegetables_locations:
            if self.grid[x][y] == vegetables.UNKNOWN:
                timeout = time.time() + 0.5
                while True:
                    sc.blit(pygame.transform.scale(pygame.image.load(self.photo_paths[x][y]), (BLOCK_SIZE*2, BLOCK_SIZE*2)),
                        ((x * BLOCK_SIZE) - BLOCK_SIZE/2, (y * BLOCK_SIZE) - BLOCK_SIZE/2))
                    # time.sleep(1/63)
                    if time.time() > timeout:
                        break
                # time.sleep(1)
                random_veg = random.choice(list(vegetables))
                while random_veg == vegetables.UNKNOWN:
                    random_veg = random.choice(list(vegetables))
                # self.grid[x][y] = random_veg
                # self.grid[x][y] = uio.recognize(self.photo_paths[x][y])
                aiResult = uio.recognize(self.photo_paths[x][y])
                if aiResult == 'Broccoli':
                    self.grid[x][y] = vegetables.BROCCOLI
                if aiResult == 'Capsicum':
                    self.grid[x][y] = vegetables.CAPSICUM
                if aiResult == 'Carrot':
                    self.grid[x][y] = vegetables.CARROT
                if aiResult == 'Potato':
                    self.grid[x][y] = vegetables.POTATO


class Graph:
    def __init__(self, grid: Grid):
        self.graph = {}
        # self.initialize_graph(grid)

    # def initialize_graph(self, grid: Grid):
    #     for y, row in enumerate(grid.grid):
    #         for x, col in enumerate(row):
    #             for direction in Direction:
    #                 self.graph[(x, y, direction)] = get_next_nodes(x, y, direction, grid)

    def a_star(self, start, goal, grid: Grid):
        # not finished yet https://www.youtube.com/watch?v=abHftC1GU6w
        queue = PriorityQueue()
        queue.put((0, start))
        cost_visited = {start: 0}
        visited = {start: None}

        returnGoal = goal
        h = lambda start, goal: abs(start[0] - goal[0]) + abs(
            start[1] - goal[1])  # heuristic function (manhattan distance)

        while not queue.empty():
            cur_cost, cur_node = queue.get()
            if cur_node[0] == goal[0] and cur_node[1] == goal[1]:
                returnGoal = cur_node
                break

            next_nodes = get_next_nodes(cur_node[0], cur_node[1], cur_node[2], grid)
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
                                     vegetables.CAPSICUM: 0}
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

    # print(x,y, direction, next_nodes, '/n')
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


def getCost(tractor: Tractor, grid: Grid, road):
    n = len(road)
    cost = 0
    for i in range(n - 1):
        aA = road[i]
        bB = road[i + 1]
        if aA[0] != bB[0]:
            if grid.grid[bB[0]][bB[1]] == types.ROCK:
                cost += 12
            else:
                cost += 2
        if aA[1] != bB[1]:
            if grid.grid[bB[0]][bB[1]] == types.ROCK:
                cost += 12
            else:
                cost += 2
        if aA[2] != bB[2]:
            if (bB[2].value - aA[2].value == 1) or (bB[2].value - aA[2].value == -3):
                cost += 1
            else:
                cost += 1
    return cost


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
            elif grid.grid[x][y] == vegetables.CAPSICUM:
                sc.blit(capsicum_image, (x * BLOCK_SIZE + 5, y * BLOCK_SIZE + 5))
            elif grid.grid[x][y] == vegetables.UNKNOWN:
                sc.blit(unknown_image, (x * BLOCK_SIZE + 5, y * BLOCK_SIZE + 5))
            elif grid.grid[x][y] == types.ROCK:
                sc.blit(rock_image, (x * BLOCK_SIZE, y * BLOCK_SIZE))
    sc.blit(gas_station_image, (SPAWN_POINT[0] * BLOCK_SIZE, SPAWN_POINT[1] * BLOCK_SIZE))
    if grid.is_storage_closed:
        sc.blit(sklep_closed_station_image, (SKLEP_POINT[0] * BLOCK_SIZE, SKLEP_POINT[1] * BLOCK_SIZE))
    else:
        sc.blit(sklep_station_image, (SKLEP_POINT[0] * BLOCK_SIZE, SKLEP_POINT[1] * BLOCK_SIZE))
    if grid.is_gas_station_closed:
        sc.blit(gas_station_closed_image, (SPAWN_POINT[0] * BLOCK_SIZE, SPAWN_POINT[1] * BLOCK_SIZE))
    else:
        sc.blit(gas_station_image, (SPAWN_POINT[0] * BLOCK_SIZE, SPAWN_POINT[1] * BLOCK_SIZE))

    # region text
    vegetables_text = font.render(
        'Potato: ' + str(tractor.collected_vegetables[vegetables.POTATO]) + ' Broccoli: ' + str(
            tractor.collected_vegetables[vegetables.BROCCOLI]) + ' Carrot: ' + str(
            tractor.collected_vegetables[vegetables.CARROT]) + ' Capsicum: ' + str(
            tractor.collected_vegetables[vegetables.CAPSICUM]), True, WHITE, BLACK)
    vegetables_textrect = vegetables_text.get_rect()
    vegetables_textrect.center = (WINDOW_DIMENSIONS // 2, WINDOW_DIMENSIONS - 30)
    sc.blit(vegetables_text, vegetables_textrect)

    gas_text = font.render('Gas tank: ' + str(tractor.gas), True, WHITE, BLACK)
    gas_textrect = gas_text.get_rect()
    gas_textrect.center = (WINDOW_DIMENSIONS // 4 * 3.5, 20)
    sc.blit(gas_text, gas_textrect)
    # endregion

    sc.blit(tractor.image, (tractor.x * BLOCK_SIZE + 5, tractor.y * BLOCK_SIZE + 5))
    pygame.display.update()

    pygame.time.Clock().tick(60)


def decisionTree(startpoint, endpoint, tractor, grid, graph1):
    one = "can it get to the next point"
    two = "will it be able to get to the gas station"
    three = "will it be able to get to the gas station after arriving at the next point"
    four = "will it be able to take the next vegetable to the tractor storage"
    five = "will it be able to get to the vegetable warehouse"
    six = "will it be able to get to the gas station after it arrives at the vegetable warehouse"
    seven = "is the vegetable warehouse closed"
    eight = "is the gas station closed"
    arr = []
    arr.append(one)
    arr.append(two)
    arr.append(three)
    arr.append(four)
    arr.append(five)
    arr.append(six)
    arr.append(seven)
    arr.append(eight)

    a1, c1 = graph1.a_star(startpoint, endpoint, grid)
    b1 = getRoad(startpoint, c1, a1)
    cost1 = getCost(tractor, grid, b1)

    a2, c2 = graph1.a_star(startpoint, (SPAWN_POINT[0], SPAWN_POINT[1], Direction.RIGHT), grid)
    b2 = getRoad(startpoint, c2, a2)
    cost2 = getCost(tractor, grid, b2)

    a3, c3 = graph1.a_star(startpoint, (SKLEP_POINT[0], SKLEP_POINT[1], Direction.RIGHT), grid)
    b3 = getRoad(startpoint, c3, a3)
    cost3 = getCost(tractor, grid, b3)

    a4, c4 = graph1.a_star(c1, (SPAWN_POINT[0], SPAWN_POINT[1], Direction.RIGHT), grid)
    b4 = getRoad(c1, c4, a4)
    cost4 = getCost(tractor, grid, b4)

    a5, c5 = graph1.a_star(c3, (SPAWN_POINT[0], SPAWN_POINT[1], Direction.RIGHT), grid)
    b5 = getRoad(c3, c5, a5)
    cost5 = getCost(tractor, grid, b5)

    if tractor.gas - cost1 > 0:
        can_it_get_to_the_next_point = 1
    else:
        can_it_get_to_the_next_point = 0

    if tractor.gas - cost2 > 0:
        will_it_be_able_to_get_to_the_gas_station = 1
    else:
        will_it_be_able_to_get_to_the_gas_station = 0

    if tractor.gas - cost1 - cost4 > 0:
        will_it_be_able_to_get_to_the_gas_station_after_arriving_at_the_next_point = 1
    else:
        will_it_be_able_to_get_to_the_gas_station_after_arriving_at_the_next_point = 0

    if grid.grid[endpoint[0]][endpoint[1]] in vegetables:
        if tractor.collected_vegetables[grid.grid[endpoint[0]][endpoint[1]]] < 5:
            will_it_be_able_to_take_the_next_vegetable_to_the_tractor_storage = 1
        else:
            will_it_be_able_to_take_the_next_vegetable_to_the_tractor_storage = 0
    else:
        will_it_be_able_to_take_the_next_vegetable_to_the_tractor_storage = 1

    if tractor.gas - cost3 > 0:
        will_it_be_able_to_get_to_the_vegetable_warehouse = 1
    else:
        will_it_be_able_to_get_to_the_vegetable_warehouse = 0

    if tractor.gas - cost3 - cost5 > 0:
        will_it_be_able_to_get_to_the_gas_station_after_it_arrives_at_the_vegetable_warehouse = 1
    else:
        will_it_be_able_to_get_to_the_gas_station_after_it_arrives_at_the_vegetable_warehouse = 0

    is_the_vegetable_warehouse_closed = grid.is_storage_closed
    is_the_gas_station_closed = grid.is_gas_station_closed

    brr = []
    brr.append(can_it_get_to_the_next_point)
    brr.append(will_it_be_able_to_get_to_the_gas_station)
    brr.append(will_it_be_able_to_get_to_the_gas_station_after_arriving_at_the_next_point)
    brr.append(will_it_be_able_to_take_the_next_vegetable_to_the_tractor_storage)
    brr.append(will_it_be_able_to_get_to_the_vegetable_warehouse)
    brr.append(will_it_be_able_to_get_to_the_gas_station_after_it_arrives_at_the_vegetable_warehouse)
    brr.append(is_the_vegetable_warehouse_closed)
    brr.append(is_the_gas_station_closed)

    def predict(tree):
        if not isinstance(tree, dict):
            return tree
        else:
            root_node = next(iter(tree))
            feature_value = brr[arr.index(root_node)]
            if feature_value in tree[root_node]:
                return predict(tree[root_node][feature_value])
            else:
                return None

    decision = predict(tree)
    print(decision)
    if decision == 1:
        movement(tractor, grid, b1)
    if decision == 2:
        movement(tractor, grid, b2)
    if decision == 3:
        movement(tractor, grid, b3)
    if decision == 4:
        print("waiting")
    if decision == 5:
        print("GAME OVER")


def close_open(grid: Grid):
    while True:
        time.sleep(TIMEOUT)
        grid.is_gas_station_closed = bool(random.getrandbits(1))
        grid.is_storage_closed = bool(random.getrandbits(1))


def get_random_photo_path():
    dir_num = random.randint(1, 4)
    image_dir = "C:/Users/KimD/PycharmProjects/sztin_gr.234798/Vegetable Images/train"
    if dir_num == 1:
        image_dir = "C:/Users/KimD/PycharmProjects/sztin_gr.234798/Vegetable Images/train/Broccoli"
    if dir_num == 2:
        image_dir = "C:/Users/KimD/PycharmProjects/sztin_gr.234798/Vegetable Images/train/Capsicum"
    if dir_num == 3:
        image_dir = "C:/Users/KimD/PycharmProjects/sztin_gr.234798/Vegetable Images/train/Carrot"
    if dir_num == 4:
        image_dir = "C:/Users/KimD/PycharmProjects/sztin_gr.234798/Vegetable Images/train/Potato"

    return image_dir + '/' + random.choice(os.listdir(image_dir))
