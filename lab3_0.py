import math
import pygame

run = True
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
angle = 0
size = width, height = 600, 600
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
#creen.fill(white)

#pygame.draw.circle(screen, blue, (300, 300), 100, 1)
while run:
    msElapsed = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.fill(white)
    x = int(math.cos(angle) * 100) + 300
    y = int(math.sin(angle) * 100) + 300
    pygame.draw.circle(screen, blue, (300, 300), 100, 1)
    pygame.draw.circle(screen, black, (x, y), 10)
    pygame.display.flip()
    angle -= 0.15

pygame.quit()