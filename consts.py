import pygame

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
BLUE = (46, 34, 240)
WINDOW_DIMENSIONS = 900
BLOCK_SIZE = 60
ROCKS_NUMBER = 30
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

