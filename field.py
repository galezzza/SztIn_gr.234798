import random
from enum import Enum

import pygame

pygame.init()
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
BLUE = (46, 34, 240)
WINDOW_DIMENSIONS = 900
BLOCK_SIZE = 60
ROCKS_NUMBER = 15
VEGETABLES_NUMBER = 20
VEGETABLES = ('Potato', 'Broccoli', 'Carrot', 'Onion')
BOARD_SIZE = int(WINDOW_DIMENSIONS / BLOCK_SIZE)
WATER_TANK_CAPACITY = 10
GAS_TANK_CAPACITY = 100
SPAWN_POINT = (0, 0)


def generate_locations(number, flag=False, rocks=[]):
    locations = []
    if flag:
        for i in range(number):
            x = random.randrange(0, BOARD_SIZE)
            y = random.randrange(0, BOARD_SIZE)
            if (x, y) not in rocks and (x, y, 'Potato') not in locations and (x, y, 'Broccoli') not in locations and (
            x, y, 'Carrot') not in locations and (x, y, 'Onion') not in locations:
                locations.append((x, y, VEGETABLES[random.randrange(0, len(VEGETABLES))]))
            else:
                i -= 1
        return locations
    else:
        for i in range(number):
            x = random.randrange(0, BOARD_SIZE - 1)
            y = random.randrange(0, BOARD_SIZE - 1)
            if (x, y) not in locations and (x, y) != (0, 0):
                locations.append((x, y))
            else:
                i -= 1
        return locations


def draw_grid():
    # Set the size of the grid block
    wei = pygame.transform.scale(pygame.image.load("images/wet_earth_tile.jpg"), (BLOCK_SIZE, BLOCK_SIZE))
    dei = pygame.transform.scale(pygame.image.load("images/dry_earth_tile.jpg"), (BLOCK_SIZE, BLOCK_SIZE))
    for x in range(0, BOARD_SIZE):
        for y in range(0, BOARD_SIZE):
            if (x, y) in wet_tiles_coordinates:
                sc.blit(wei, (x * BLOCK_SIZE, y * BLOCK_SIZE))
            else:
                sc.blit(dei, (x * BLOCK_SIZE, y * BLOCK_SIZE))
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(sc, WHITE, rect, 1)


def draw_interface():
    global sc
    sc = pygame.display.set_mode((WINDOW_DIMENSIONS, WINDOW_DIMENSIONS))
    pygame.display.set_caption("Pole i ciągnik")
    pygame.display.set_icon(pygame.image.load("images/icon.png"))

    clock = pygame.time.Clock()
    sc.fill(BLACK)
    FPS = 60

    # region Images import
    # bg = pygame.image.load("images/field_image.jpg")
    tractor_image= pygame.transform.scale(pygame.image.load("images/tractor_image.png"), (BLOCK_SIZE, BLOCK_SIZE))
    rock_image = pygame.transform.scale(pygame.image.load("images/rock_image.png"), (BLOCK_SIZE, BLOCK_SIZE))
    potato_image = pygame.transform.scale(pygame.image.load("images/potato.png"), (BLOCK_SIZE, BLOCK_SIZE))
    carrot_image = pygame.transform.scale(pygame.image.load("images/carrot.png"), (BLOCK_SIZE, BLOCK_SIZE))
    broccoli_image = pygame.transform.scale(pygame.image.load("images/broccoli.png"), (BLOCK_SIZE, BLOCK_SIZE))
    onion_image = pygame.transform.scale(pygame.image.load("images/onion.png"), (BLOCK_SIZE, BLOCK_SIZE))
    gas_station_image = pygame.transform.scale(pygame.image.load("images/gas_station.png"), (BLOCK_SIZE, BLOCK_SIZE))
    font = pygame.font.Font('freesansbold.ttf', BLOCK_SIZE // 2)
    # endregion

    (x, y) = SPAWN_POINT

    rocks = generate_locations(ROCKS_NUMBER)
    vegetables = generate_locations(VEGETABLES_NUMBER, flag=True, rocks=rocks)
    water_left = WATER_TANK_CAPACITY
    gas_left = GAS_TANK_CAPACITY
    collected_vegetables = [0, 0, 0, 0]
    global wet_tiles_coordinates
    wet_tiles_coordinates = []

    fl_running = True
    while fl_running:
        draw_grid()

        #region events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                fl_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if x > 0:
                        x -= 1
                        if (x - 1, y) not in rocks:
                            gas_left -= 1
                        else:
                            print('Rock')
                            gas_left -= 5
                elif event.key == pygame.K_RIGHT:
                    if x < BOARD_SIZE - 1:
                        x += 1
                        if (x + 1, y) not in rocks:
                            gas_left -= 1
                        else:
                            gas_left -= 5
                            print("Rock")
                elif event.key == pygame.K_DOWN:
                    if y < BOARD_SIZE - 1:
                        y += 1
                        if (x, y + 1) not in rocks:
                            gas_left -= 1
                        else:
                            gas_left -= 5
                            print("Rock")
                elif event.key == pygame.K_UP:
                    if y > 0:
                        y -= 1
                        if (x, y - 1) not in rocks:
                            gas_left -= 1
                        else:
                            gas_left -= 5
                            print("Rock")
                elif event.key == pygame.K_SPACE:
                    wet_tiles_coordinates.append((x, y))
                elif event.key == pygame.K_RETURN:
                    for vegetable in vegetables:
                        if vegetable[0] == x and vegetable[1] == y:
                            water_left -= 1
                            if vegetable[2] == 'Potato':
                                print("Potato collected")
                                collected_vegetables[0] += 1
                            elif vegetable[2] == 'Broccoli':
                                print("Broccoli collected")
                                collected_vegetables[1] += 1
                            elif vegetable[2] == 'Carrot':
                                print("Carrot collected")
                                collected_vegetables[2] += 1
                            elif vegetable[2] == 'Onion':
                                print("Onion collected")
                                collected_vegetables[3] += 1
                            vegetables.remove(vegetable)
                            break
                        else:
                            print("No vegetable here")
                    if (x, y) == SPAWN_POINT:
                        water_left = WATER_TANK_CAPACITY
                        gas_left = GAS_TANK_CAPACITY

        #endregion

        for rock in rocks:
            sc.blit(rock_image, (rock[0] * BLOCK_SIZE, rock[1] * BLOCK_SIZE))
        for vegetable in vegetables:
            if vegetable[2] == 'Potato':
                sc.blit(potato_image, (vegetable[0] * BLOCK_SIZE + 5, vegetable[1] * BLOCK_SIZE + 5))
            elif vegetable[2] == 'Carrot':
                sc.blit(carrot_image, (vegetable[0] * BLOCK_SIZE + 5, vegetable[1] * BLOCK_SIZE + 5))
            elif vegetable[2] == 'Broccoli':
                sc.blit(broccoli_image, (vegetable[0] * BLOCK_SIZE + 5, vegetable[1] * BLOCK_SIZE + 5))
            elif vegetable[2] == 'Onion':
                sc.blit(onion_image, (vegetable[0] * BLOCK_SIZE + 5, vegetable[1] * BLOCK_SIZE + 5))
        sc.blit(gas_station_image, (SPAWN_POINT[0] * BLOCK_SIZE, SPAWN_POINT[1] * BLOCK_SIZE))

        # region text
        vegetables_text = font.render('Potato: ' + str(collected_vegetables[0]) + ' Broccoli: ' + str(
            collected_vegetables[1]) + ' Carrot: ' + str(collected_vegetables[2]) + ' Onion: ' + str(
            collected_vegetables[3]), True, WHITE, BLACK)
        vegetables_textRect = vegetables_text.get_rect()
        vegetables_textRect.center = (WINDOW_DIMENSIONS // 2, WINDOW_DIMENSIONS - 30)
        sc.blit(vegetables_text, vegetables_textRect)

        water_text = font.render('Waterd tank: ' + str(water_left), True, WHITE, BLACK)
        water_textRect = water_text.get_rect()
        water_textRect.center = (WINDOW_DIMENSIONS // 4, 20)
        sc.blit(water_text, water_textRect)

        gas_text = font.render('Gas tank: ' + str(gas_left), True, WHITE, BLACK)
        gas_textRect = gas_text.get_rect()
        gas_textRect.center = (WINDOW_DIMENSIONS // 4 * 3, 20)
        sc.blit(gas_text, gas_textRect)
        # endregion

        sc.blit(tractor_image, (x * BLOCK_SIZE + 5, y * BLOCK_SIZE + 5))
        pygame.display.update()

        clock.tick(FPS)


class types(Enum):
    EMPTY = 0
    ROCK = 1
    TRACTOR = 2
    POTATO = 3
    BROCCOLI = 4
    CARROT = 5
    ONION = 6


class objectOnField:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type


class Grid:
    def __init__(self, width, height, block_size):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.grid = []
        self.vegetables = []
        self.rocks = []
        self.tractor = None
        self.wet_tiles = []
        self.generate_grid()
