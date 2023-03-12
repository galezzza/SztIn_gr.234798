import pygame
pygame.init()
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
BLUE = (46, 34, 240)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600
BLOCK_SIZE = 40



def drawGrid():
     #Set the size of the grid block
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(sc, WHITE, rect, 1)
def draw_interface():
    global sc
    sc = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pole i ciągnik")
    pygame.display.set_icon(pygame.image.load("icon.png"))

    clock = pygame.time.Clock()
    sc.fill(BLACK)
    FPS = 60

    x = BLOCK_SIZE / 4
    y = BLOCK_SIZE / 4

    flRunning = True
    while flRunning:
        sc.fill(BLACK)
        drawGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                flRunning = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x -= BLOCK_SIZE
                elif event.key == pygame.K_RIGHT:
                    x += BLOCK_SIZE
                elif event.key == pygame.K_DOWN:
                    y += BLOCK_SIZE
                elif event.key == pygame.K_UP:
                    y -= BLOCK_SIZE
        pygame.draw.rect(sc, BLUE, (x, y, BLOCK_SIZE / 2, BLOCK_SIZE / 2))
        pygame.display.update()

        clock.tick(FPS)