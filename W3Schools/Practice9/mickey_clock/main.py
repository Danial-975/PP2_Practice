import pygame
import datetime

pygame.init()
screen = pygame.display.set_available_data = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Mickey's Clock")
clock = pygame.time.Clock()

bg = pygame.image.load('images/clock.png')
shand = pygame.image.load('images/shorthand.png')
lhand = pygame.image.load('images/longhand.png') 

def rotate_hand(image, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=(400, 400))
    
    return rotated_image, new_rect

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = datetime.datetime.now()
    minute = now.minute
    second = now.second

    angle_sec = -second * 6
    angle_min = -minute * 6

    screen.fill((255, 255, 255))
    screen.blit(bg, (0, 0))

    img_sec, rect_sec = rotate_hand(shand, angle_sec)
    img_min, rect_min = rotate_hand(lhand, angle_min)

    screen.blit(img_min, rect_min)
    screen.blit(img_sec, rect_sec)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()