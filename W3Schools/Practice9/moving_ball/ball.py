import pygame

pygame.init()
W, H = 800, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Moving Ball")

x, y = W // 2, H // 2
radius = 25
step = 20

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and y - step >= radius:
                y -= step
            elif event.key == pygame.K_DOWN and y + step <= H - radius:
                y += step
            elif event.key == pygame.K_LEFT and x - step >= radius:
                x -= step
            elif event.key == pygame.K_RIGHT and x + step <= W - radius:
                x += step

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (x, y), radius)
    pygame.display.flip()
pygame.quit()