import random

import pygame
pygame.init()
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
BLUE = (46, 34, 240)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600
BLOCK_SIZE = 40
ROCKS_NUMBER = 10
VEGETABLES_NUMBER = 20
VEGETABLES = ('Potato', 'Broccoli', 'Carrot', 'Onion')



def generate_locations(number, flag=False, rocks=[]):
    locations = []
    if flag:
        for i in range(number):
            x = random.randrange(0, WINDOW_WIDTH, BLOCK_SIZE)
            y = random.randrange(0, WINDOW_HEIGHT, BLOCK_SIZE)
            if (x, y) not in rocks and (x, y) not in locations:
                locations.append((x, y, VEGETABLES[random.randrange(0, len(VEGETABLES))]))
            else:
                i -= 1
        return locations
    else:
        for i in range(number):
            x = random.randrange(0, WINDOW_WIDTH, BLOCK_SIZE)
            y = random.randrange(0, WINDOW_HEIGHT, BLOCK_SIZE)
            if (x, y) not in locations:
                locations.append((x, y))
            else:
                i -= 1
        return locations



def draw_grid():
     #Set the size of the grid block
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(sc, WHITE, rect, 1)
def draw_interface():
    global sc
    sc = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pole i ciągnik")
    pygame.display.set_icon(pygame.image.load("images/icon.png"))

    clock = pygame.time.Clock()
    sc.fill(BLACK)
    FPS = 60

    #region Images import
    bg = pygame.image.load("images/field_image.jpg")
    tractor_image = pygame.image.load("images/tractor_image.png")
    rock_image = pygame.image.load("images/rock_image.png")
    potato_image = pygame.image.load("images/potato.png")
    carrot_image = pygame.image.load("images/carrot.png")
    broccoli_image = pygame.image.load("images/broccoli.png")
    onion_image = pygame.image.load("images/onion.png")
    #endregion

    x = BLOCK_SIZE / 4
    y = BLOCK_SIZE / 4

    rocks = generate_locations(ROCKS_NUMBER)
    vegetables = generate_locations(VEGETABLES_NUMBER, flag=True, rocks=rocks)

    flRunning = True
    while flRunning:
        #sc.fill(BLACK)
        sc.blit(bg, (0, 0))
        draw_grid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                flRunning = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if x > BLOCK_SIZE/2:
                        x -= BLOCK_SIZE
                elif event.key == pygame.K_RIGHT:
                    if x < WINDOW_WIDTH - BLOCK_SIZE/2:
                        x += BLOCK_SIZE
                elif event.key == pygame.K_DOWN:
                    if y < WINDOW_HEIGHT - BLOCK_SIZE/2:
                        y += BLOCK_SIZE
                elif event.key == pygame.K_UP:
                    if y > BLOCK_SIZE/2:
                        y -= BLOCK_SIZE
        #pygame.draw.rect(sc, BLUE, (x, y, BLOCK_SIZE / 2, BLOCK_SIZE / 2))
        sc.blit(tractor_image, (x-5, y-5))
        for rock in rocks:
            sc.blit(rock_image, (rock[0], rock[1]))
        for vegetable in vegetables:
            if vegetable[2] == 'Potato':
                sc.blit(potato_image, (vegetable[0], vegetable[1]))
            elif vegetable[2] == 'Carrot':
                sc.blit(carrot_image, (vegetable[0], vegetable[1]))
            elif vegetable[2] == 'Broccoli':
                sc.blit(broccoli_image, (vegetable[0], vegetable[1]))
            elif vegetable[2] == 'Onion':
                sc.blit(onion_image, (vegetable[0], vegetable[1]))

        pygame.display.update()

        clock.tick(FPS)