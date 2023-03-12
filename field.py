import pygame
pygame.init()

BLUE = (46, 34, 240)
WHITE = (255, 255, 255)
W = 600
H = 400
sc = pygame.display.set_mode((W, H))
pygame.display.set_caption("Pole i ciągnik")
pygame.display.set_icon(pygame.image.load("icon.png"))

clock = pygame.time.Clock()
FPS = 60

x = W // 2
y = H // 2
speed = 20

flRunning = True
while flRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            flRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= speed
            elif event.key == pygame.K_RIGHT:
                x += speed
            elif event.key == pygame.K_DOWN:
                y += speed
            elif event.key == pygame.K_UP:
                y -= speed
    sc.fill(WHITE)
    pygame.draw.rect(sc, BLUE, (x, y, 20, 20))
    pygame.display.update()

    clock.tick(FPS)